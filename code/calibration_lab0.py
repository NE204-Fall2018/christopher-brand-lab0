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
import pylab as P
#from scipy.optimize import curve_fit
#from modelling import gauss
from gamma_energies import gamma_energies
import operator
import matplotlib.transforms as mtransforms
from matplotlib.transforms import offset_copy
'''
Enter the isotope spectrum to be calibrated. The calibration sources
will be entered next
'''
energy_spectrum = gamma_energies('Ba133')
energy_spectrum = sorted(energy_spectrum, key=int)
'''
Enter in your calibration sources into energy_calibration
energy_calibration('Co60', 'Cs137')
'''
energy_list = gamma_energies('Cs137', 'Am241')
energy_list = sorted(energy_list, key=int)

channel_width = 20
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
Some a priori knowledge is neeeded about the spectrum
beforehand. The data needs to be cleaned before running this section.
Remove all of the peaks that are a result of noise or compton continuum.
'''
list_data = np.array(Ba133).tolist()
del list_data[clean_left:clean_right]

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
for plotting purposes. All of the peaks are found from the trimmed data
and the corresponding count rates are found. A list is created and then the
list is sorted based by the position of the counts.
'''
i = 0; channel_max_list = []; energy_list_2 =[]

while i < len(energy_spectrum):
    channel_max = np.argmax(list_data)
    channel_max_list.append(channel_max)
    energy_list_2.append(list_data[channel_max])
    print(energy_list_2)
    data_left = channel_max - channel_width
    data_right = channel_max + channel_width
    del list_data[data_left:data_right]
    i += 1
energy_channel = list(zip(channel_max_list, energy_list_2))
print(energy_channel)
energy_channel.sort(key=operator.itemgetter(0))
print(energy_channel)

'''
This sequence plots the energy of the peaks and with their corresponding
energies.
'''

fig = plt.figure()
energy_list_2 =[]
for channel, energy in energy_channel:
    energy_list_2.append(float(energy))
for x, y in zip(energy_spectrum, energy_list_2):
    x1 = np.linspace(x,x, 10000) #plotting a horizontal line
    y1 = np.linspace(0, y,10000) #plotting a horizontal line
    plt.plot(x1,y1, 'b', linestyle = '--', label = 'Actual Energy')
    plt.xlim(0, max(energy_spectrum)+100)
plt.plot(calibrated_channel, Ba133, 'k')
plt.ylabel("Counts")
plt.xlabel("Energy(keV)")
plt.title("Calibrated Energy Plot")
#plt.legend()
plt.savefig('../images/Ba133_calibrated.png')
#argmax returns the position in the array where maximum occurs
