'''
fit_analysis.py
fit_analysis.py analyzes a spectrum and creates an energy calibration.
It uses the function energy_calibration to calibrate an energy spectrum.
Two points are needed for this linear calibration.

Before starting it is important to have some understanding of the spectrum
you are going to fit the calibration with. There is clean_left and clean_right
that will trim the beginning of the spectrum to remove noise and other
spurious results.
'''

import numpy as np
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
#from modelling import gauss
from gamma_energies import gamma_energies
'''
Enter the isotope spectrum to be calibrated. The calibration sources
will be entered next
'''
energy_spectrum = gamma_energies('Ba133')
'''
Enter in your calibration sources into energy_calibration
energy_calibration('Co60', 'Cs137')
'''
energy_list = gamma_energies('Cs137', 'Am241')
energy_list = sorted(energy_list, key=int)

channel_width = 10
clean_left = 0
clean_right = 150

'''
The file is generated from the make file.
'''

fname = '../lab0_spectral_data.txt'
with open(fname, 'r') as f:
    first_line = f.readline()
    length = float(len(first_line.split()))
    length = np.arange(0, length)

data = np.genfromtxt(fname, delimiter='', skip_header=1)
#parse the CSV data into fields we can use easily:
Am241 = data[:,0]
Ba133 = data[:,1]
Cs137 = data[:,2]
Co60 = data[:,3]
Eu152 = data[:,4]
'''
merging the data for the calibration
Also converting merged data into a list so channels can be
removed easier.
'''
data_2_calibrate = data[:,0] + data[:,2]
data_2_calibrate = np.array(data_2_calibrate).tolist()

'''
Calibrating the new spectrum with the slope and intercept produced
from the energy calibration.
'''

from calibration import spectrum_calibration
slope, intercept = spectrum_calibration(channel_width, energy_list, data_2_calibrate)
calibrated_channel = []
for i in range(0,len(Ba133)):
    calibrated_channel += [i*slope+ intercept]
calibrated_channel = np.array(calibrated_channel, 'float')

'''
Attempting to iterate through the peaks and identify all of the peaks
for plotting purposes. Some a priori knowledge is neeeded about the spectrum
beforehand. The data needs to be cleaned before running this section.
Remove all of the peaks that are a result of noise or compton continuum.
'''
i = 0; channel_max_list = []
list_data = np.array(Ba133).tolist()
del list_data[clean_left:clean_right]
while i < len(energy_spectrum):
    channel_max = np.argmax(list_data)
    data_left = channel_max - channel_width
    data_right = channel_max + channel_width
    del list_data[data_left:data_right]
    channel_max_list.append(channel_max)
    i += 1
channel_number = sorted(channel_max_list, key=int)
fig = plt.figure()
for x, y in zip(energy_spectrum, channel_number):
    y_limit = Ba133[y]
    x1 = np.linspace(x,x, 10000) #plotting a horizontal line
    y1 = np.linspace(0, max(Ba133),10000) #plotting a horizontal line
    plt.plot(x1,y1, 'b', linestyle = '--', label = 'Actual Energy')
    plt.xlim(0, max(energy_spectrum)+50)
plt.plot(calibrated_channel, Ba133, 'k')
plt.ylabel("Counts")
plt.xlabel("Energy(keV)")
plt.title("Calibrated Energy Plot")
#plt.legend()
plt.savefig('../images/Ba133_calibrated.png')
#argmax returns the position in the array where maximum occurs
