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

from calibration import energy_calibration
energy_list = energy_calibration('Cs137', 'Am241')
energy_list = sorted(energy_list, key=int)
print(energy_list)
merged_data = data[:,0] + data[:,2]
plt.plot(merged_data)
#from adc2kev import calibration
#slope, intercept = calibration(Cs137)
#largest_integers = heapq.nlargest(1, Cs137)
Am241_max = np.argmax(Am241)
Cs137_max = np.argmax(Cs137)
channel_number = [Am241_max, Cs137_max]
energy = energy_list
results = sm.OLS(energy,sm.add_constant(channel_number)).fit()

slope, intercept = np.polyfit(channel_number, energy, 1)

abline_values = [slope * i + intercept for i in channel_number]
plt.plot(channel_number,energy, 'ro')
plt.plot(channel_number, abline_values, 'b')
plt.xlabel('ADC Val')
plt.ylabel('Energy [keV]')
plt.title('Best Fit Line')
Cs = []
for i in range(0,len(Cs137)):
    Cs += [i*slope+ intercept]
Cs = np.array(Cs, 'float')
plt.figure(2)
plt.plot(Cs, Cs137, 'g')
x1 = np.linspace(661.657,661.657, 100) #plotting a horizontal line
y1 = np.linspace(0,50000,100) #plotting a horizontal line
plt.plot(x1,y1, 'b', linestyle = '--', label = 'Desired')
plt.ylabel("Counts")
plt.xlabel("Energy(keV)")
plt.title("Calibrated Energy Plot")
plt.show()
#argmax returns the position in the array where maximum occurs
