import numpy as np
import lightkurve as lk
from astropy.io import fits
from astropy import units as u
import glob
import os
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

###########################################################################

# function should stitch make lightcurve objects for a target
# it should skip bad sectors
# it should stitch all sectors together and normalize
# target and sector should both be strings/list of strings

def stitch(target, sectors):
    # create path list to target and desired sectors
    # path list of sectors to create lightcurves from
    l = []

    for sector in sectors:
        path = f'tess_fastlc_data/{target}/{sector}_{target}_fast-lc.fits'
        l.append(path)
    
    # create lightcurves for each sector in list l
    lc_list = []

    for i in l:
        lc = lk.read(i)
    
        # remove nans, outliers, & remove points with a quality flag
        lc = lc.remove_nans()
        lc = lc.remove_outliers(sigma=4.0)
        qual_mask = np.where(lc.quality == 0)
        lc = lc[qual_mask]
    
        # normalize sector
        lc = lc.normalize()
    
        lc_list.append(lc)
    
    # create lightcurve collection
    lcc = lk.LightCurveCollection.stitch(lc_list)
    
    return(lcc)

###########################################################################

# test target
target = '25132314'

# create list of sectors
# probably a better way to do this, just hardcode for now
sectors = np.arange(27,40,1)
# remove unwanted sectors
sectors = sectors[np.where(sectors != 35)]
# convert sectors to list of strings
sectors = [str(i) for i in sectors]

# run test function
lcc_stitched = stitch(target, sectors)

