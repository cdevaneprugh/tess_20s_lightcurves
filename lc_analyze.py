import numpy as np
import lightkurve as lk
import lightkurve_stitching as lks
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# set our target and sectors
target = '349902873'
sectors = np.arange(27,40,1)
sectors = [str(i) for i in sectors]

# stitch light curves
lc = lks.prep_data(target, sectors, 1)

#-------------------------------------------------------------------------------

# turn this into a function that takes a stitched light curve as an input
# take max frequency, window size, and window movement amount (n) as inputs

# list of frequencies and periods at max power within each window
f = []
p = []
pwr = []

# start values of the frequency window
min_f = 0
max_f = 2

# value to move frequency window by
n = 2

while max_f <= 30:
    # create periodogram within window
    pg = lc.to_periodogram(min_frequency = min_f, max_frequency = max_f)

    # calculate frequency and period at max power
    F = pg.frequency_at_max_power
    P = pg.period_at_max_power

    # append frequency and period to list
    if pg.max_power > 0.00015:
        f.append(F.value)
        p.append(P.value)
        pwr.append(pg.max_power.value)

        # increase window by amount n
        min_f += n
        max_f += n
    else:

        # increase window by amount n
        min_f += n
        max_f += n


# plot of periodogram with interesting frequencies indicated
pg = lc.to_periodogram(minimum_frequency=0, maximum_frequency = 30)
ax = pg.plot()

for i in range(len(f)):
    ax.annotate('',
                xy=(f[i], 0.0007),
                xytext=(f[i], 0.0009),
                arrowprops=dict(arrowstyle='->', color='red', linewidth=1.5))
