'''
fit_analysis.py
fit_analysis.py analyzes a spectrum and creates an energy calibration.
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from modelling import gauss
import statsmodels.api as sm

fname = '../lab0_spectral_data.txt'
data = np.genfromtxt(fname, delimiter='', skip_header=1)
#parse the CSV data into fields we can use easily:
Am241 = data[:,0]
Ba133 = data[:,1]
Cs137 = data[:,2]
Co60 = data[:,3]
Eu152 = data[:,4]

#from adc2kev import calibration
#slope, intercept = calibration(Cs137)
plt.plot(Cs137)
plt.plot(Am241)
Am241_max = np.argmax(Am241)
print(Am241_max)
Cs137_max = np.argmax(Cs137)
counts = [Am241_max, Cs137_max]
energy = [59.541, 661.657]
results = sm.OLS(energy,sm.add_constant(counts)).fit()

slope, intercept = np.polyfit(counts, energy, 1)

abline_values = [slope * i + intercept for i in counts]
plt.plot(counts,energy, 'ro')
plt.plot(counts, abline_values, 'b')
plt.xlabel('ADC Val')
plt.ylabel('Energy [keV]')
plt.title('Best Fit Line')
Cs = []
print(slope, intercept)
for i in range(0,len(Am241)):
    Cs += [i*slope+ intercept]
Cs = np.array(Cs, 'float')
plt.figure(2)
plt.plot(Cs, Am241)
plt.show()
#argmax returns the position in the array where maximum occurs
