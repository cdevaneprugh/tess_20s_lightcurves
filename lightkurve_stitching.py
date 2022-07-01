import numpy as np
import lightkurve as lk
import glob
import warnings
warnings.filterwarnings('ignore')

###########################################################################
# stitch function takes the target and desired sectors as inputs
# creates a lightcurve object for each sector, removes nans, outliers and normalizes
# returns a single stitched lightcurve object
# target and sector should both be strings/list of strings

def simple_stitch(target, sectors):
    # path list of sectors to create lightcurves objects
    l = []

    # create paths to target and desired sectors
    for sector in sectors:
        # this path is completely dependent on how the data is named and organized
        # using fast_lc_sorting.py should ensure everything is sorted properly
        path = f'tess_fastlc_data/{target}/{sector}_{target}_fast-lc.fits'

        # append to path list l
        l.append(path)

    # lightcurve list for stitching
    lc_list = []

    # create lightcurves for each sector in list l
    for i in l:
        lc = lk.read(i)

        # remove nans, outliers, & remove points with a quality flag
        lc = lc.remove_nans()
        lc = lc.remove_outliers(sigma=4.0)
        qual_mask = np.where(lc.quality == 0)
        lc = lc[qual_mask]

        # normalize sector
        lc = lc.normalize()

        # add sector to lightcurve list
        lc_list.append(lc)

    # stitch into single lightcurve object
    stitched_lc = lk.LightCurveCollection.stitch(lc_list)

    return(stitched_lc)

###########################################################################

# preps data for fourier analysis using same foundation as above
# target and sector should both be strings/list of strings
# crop should be an int or float to remove from breakpoints of sectors
# breakpoints are anywhere part of the data needs to be removed (discontinuities, sector beginnings/ends)

def prep_data(target, sectors, crop):
    # path list of sectors to create lightcurves objects
    l = []

    # create paths to target and desired sectors
    for sector in sectors:
        # this path is completely dependent on how the data is named and organized
        # using fast_lc_sorting.py should ensure everything is sorted properly
        path = f'tess_fastlc_data/{target}/{sector}_{target}_fast-lc.fits'

        # append to path list l
        l.append(path)

    # lightcurve list for stitching
    lc_list = []

    # create lightcurves for each sector in list l
    for i in l:
        lc = lk.read(i)

        # remove nans, outliers, & remove points with a quality flag
        lc = lc.remove_nans()
        lc = lc.remove_outliers(sigma=4.0)
        qual_mask = np.where(lc.quality == 0)
        lc = lc[qual_mask]

        # define time array
        t = lc.time.value

        # loop to find discontinuity (break point) in middle of sector
        # finds difference between two consecutive time stamps, compares to set 'break time'
        # break time is set as 0.5 days, anything longer must be the middle discontinuity
        for i in range(len(t)-1):
            if t[i+1]-t[i] > 0.5:
                break
            # i will remain saved as the array index where discontinuity begins

        # mask to remove data around break points
        # crop is the input given for how much to remove for each break points
        break1 = t[0]+crop
        break2 = t[i]-crop
        break3 = t[i+1]+crop
        break4 = t[-1]-crop

        tm0 = np.where( (t > break1) & (t < break2) )
        tm1 = np.where( (t > break3) & (t < break4) )

        mask = np.concatenate( (tm0[0], tm1[0]) )
        lc = lc[mask]

        # normalize sector
        lc = lc.normalize()

        # add sector to lightcurve list
        lc_list.append(lc)

    # stitch into single lightcurve object
    stitched_lc = lk.LightCurveCollection.stitch(lc_list)

    return(stitched_lc)
