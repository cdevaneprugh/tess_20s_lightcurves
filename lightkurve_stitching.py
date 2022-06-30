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

# target and sector should both be strings/list of strings
# crop should be an int or float to remove from either end of a sectors

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

        # mask to remove quality issues at beginning and end of sector
        # crop removes input value from either end of sector (unit=days)
        mask = np.where( (t > t[0]+crop) & (t < t[-1]-crop))
        lc = lc[mask]

        # normalize sector
        lc = lc.normalize()

        # add sector to lightcurve list
        lc_list.append(lc)

    # stitch into single lightcurve object
    stitched_lc = lk.LightCurveCollection.stitch(lc_list)

    return(stitched_lc)
