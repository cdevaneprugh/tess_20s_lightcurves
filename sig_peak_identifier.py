"""This scans through a periodogram of a stitched target and picks out
significant peaks within use defined windows. It does this by creating many
periodograms in a loop. Masking is a more efficient way to do this. But this
function does provide a bit of built in 'smoothing' if used carefully."""

#-------------------------------------------------------------------------------

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
print("Light Curve Stitched")
#-------------------------------------------------------------------------------

# find dominant frequencies by moving a window through the periodogram and finding the max power within
# list of frequencies and periods at max power within each window
f = []
p = []
pwr = []

# frequency to stop analyzing at
end = 35

# minimum power to be considered significant
min_pwr = 0.0001

# start values of the frequency window
min_f = 0
max_f = 1

# value to move frequency window by
n = 1

while max_f <= end:
    # create periodogram within window
    pg = lc.to_periodogram(min_frequency = min_f, max_frequency = max_f)

    # calculate frequency and period at max power
    F = pg.frequency_at_max_power
    P = pg.period_at_max_power

    # append frequency and period to list
    if pg.max_power > min_pwr:
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

print("Significant Peaks Identified")

# Calculate change in f and p per point
delta_f = []
delta_p = []

for i in range(len(f) - 1):
    n = f[i+1] - f[i]
    delta_f.append(n)

for i in range(len(p) - 1):
    n = p[i] - p[i+1]
    delta_p.append(n)

#-------------------------------------------------------------------------------

# plot the periodograms and spcaing in frequency & period space

# highest power
h = max(pwr)

# plot periodogram plus significant frequencies
pg = lc.to_periodogram(minimum_frequency=0, maximum_frequency = 35)

# define frequency arrays
freq = pg.frequency.value
power = pg.power.value

# create and save figure
fig, axs = plt.subplots(3,1, figsize=(15,20))

# plot periodogram
axs[0].plot(freq, power, color = 'k')
axs[0].axhline(y=min_pwr, color = 'b', label = 'Minimum Power Measured')
axs[0].set_xlabel('Frequency')
axs[0].set_ylabel('Power')
# add labels of significant frequencies
for i in range(len(f)):
    axs[0].annotate('',
                xy=(f[i], h),
                xytext=(f[i], h + 0.0001),
                arrowprops=dict(arrowstyle='->', color='red', linewidth=1.5),
                label='Peaks of Interest')
axs[0].legend()

# plot frequency vs change in frequency
axs[1].plot(f[1:20], delta_f, marker='o', color='red')
axs[1].set_title('Frequency vs Frequency Spacing')
axs[1].set_xlabel('Frequency [1/d]')
axs[1].set_ylabel('Frequency Spacing')

# plot period vs change in period
axs[2].plot(p[1:20], delta_p, marker='o', color='b')
axs[2].set_title('Period vs Period Spacing')
axs[2].set_yscale('log')
axs[2].set_xlabel('Period [d]')
axs[2].set_ylabel('Period Spacing (Log Scaled)')

plt.savefig('PG Significant Peaks')
