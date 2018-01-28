'''
fit_analysis.py
fit_analysis.py analyzes a spectrum and creates an energy calibration.
It uses the function energy_calibration to calibrate an energy spectrum.
Two points are needed for this linear calibration.
'''
import numpy as np
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
#from modelling import gauss

'''
Enter in your calibration sources into energy_calibration
energy_calibration('Co60', 'Cs137')
'''
from gamma_energies import gamma_energies
energy_list = gamma_energies('Cs137', 'Am241')
energy_list = sorted(energy_list, key=int)

channel_width = 10

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
merged_data = data[:,0] + data[:,2]
merged_data = np.array(merged_data).tolist()
plt.plot(merged_data)

'''
The while loop goes through and identifies the largest peak in the
spectrum and it records the position of that peak. It then removes
the peak by removing 10 channels from the right and left of the peak.
The code will then search for the next largest position.
'''
from calibration import spectrum_calibration
slope, intercept = spectrum_calibration(channel_width, energy_list, merged_data)
Cs = []
for i in range(0,len(Cs137)):
    Cs += [i*slope+ intercept]
Cs = np.array(Cs, 'float')
plt.figure(2)
plt.plot(Cs, Cs137, 'g')
fig = plt.figure()
plt.plot(Cs137)
plt.savefig('../images/Ba133.png')
x1 = np.linspace(661.657,661.657, 100) #plotting a horizontal line
y1 = np.linspace(0,50000,100) #plotting a horizontal line
plt.plot(x1,y1, 'b', linestyle = '--', label = 'Desired')
plt.ylabel("Counts")
plt.xlabel("Energy(keV)")
plt.title("Calibrated Energy Plot")
plt.show()
#argmax returns the position in the array where maximum occurs
