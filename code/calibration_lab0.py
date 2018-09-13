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
import sys
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
#from modelling import gauss
from lmfit.models import GaussianModel
from lmfit.models import LinearModel
from gamma_energies import gamma_energies
# import gamma_energies
import operator
from matplotlib.pyplot import *
'''
Source Energy spectrum to be calibrated
'''
energy_spectrum = gamma_energies('Ba133')
energy_spectrum = sorted(energy_spectrum, key=int)
'''
Enter calibration sources into energy_calibration
'''
energy_list = gamma_energies('Cs137', 'Am241')
energy_list = sorted(energy_list, key=int)

channel_width = 7
clean_left = 0
clean_right = 150

'''
Loads the data
'''

fname = '../lab0_spectral_data.txt'
with open(fname, 'r') as f:
    first_line = f.readline()
    length = float(len(first_line.split()))
    length = np.arange(0, length)

data = np.genfromtxt(fname, delimiter='', skip_header=1)
#parse the  data into fields:
Am241 = data[:,0]
Ba133 = data[:,1]
Cs137 = data[:,2]
Co60 = data[:,3]
Eu152 = data[:,4]
calibrate_data = Ba133
'''
Prior knowledge about the spectrum is needed
beforehand. The data needs to be cleaned before running this section.
Remove all of the peaks that are a result of noise or compton continuum.
'''
list_data = np.array(calibrate_data).tolist()
#del list_data[clean_left:clean_right]
iterator = clean_left
while iterator < (clean_right):
    list_data[iterator] = 0
    iterator += 1
'''
merging the data for the calibration
Also converting merged data into a list so channels can be
removed easier.
'''
data_2_calibrate = data[:,0] + data[:,2]

'''
Calibrating the new spectrum with the slope and intercept produced
from the energy calibration.
'''

from calibration import spectrum_calibration
slope, intercept = spectrum_calibration(channel_width, energy_list, data_2_calibrate)
print(slope)
print(intercept)

calibrated_channel = []
for i in range(0,len(calibrate_data)):
    calibrated_channel += [i*slope+ intercept]
calibrated_channel = np.array(calibrated_channel, 'float')

'''
Attempting to iterate through the peaks and identify all of the peaks
for plotting purposes. All of the peaks are found from the trimmed data
and the corresponding count rates are found. A list is created and then the
list is sorted based by the position of the counts.
'''
i = 0; channel_max_list = []; energy_list_2 =[]
gauss_x =[]; gauss_y=[]; fit_channel = []

while i < len(energy_spectrum):
    channel_max = np.argmax(list_data)
    channel_max_list.append(channel_max)
    energy_list_2.append(list_data[channel_max])
    data_left = channel_max - channel_width
    data_right = channel_max + channel_width
    '''
    Instead of deleting the items from the list. I am placing them to
    zero. The while loop iterates over the peak and sets it to zero.
    '''
    iterator = data_left
    while iterator < (data_right):
        gauss_x.append(iterator)
        gauss_y.append(list_data[iterator])
        x = np.asarray(gauss_x)
        y = np.asarray(gauss_y)
        fit_channel.append(list_data[iterator])
        list_data[iterator] = 0
        iterator += 1
    i += 1
    '''
    information for plotting the Gaussian function.
    '''
    mod  = GaussianModel(prefix='g1_')
    line_mod = LinearModel(prefix='line')
    pars = mod.guess(y, x=x)
    pars.update(line_mod.make_params(intercept=y.min(), slope=0))
    pars.update( mod.make_params())
    pars['g1_center'].set(gauss_x[np.argmax(gauss_y)], min=gauss_x[np.argmax(gauss_y)]\
    - 3)
    pars['g1_sigma'].set(3, min=0.25)
    pars['g1_amplitude'].set(max(gauss_y), min=max(gauss_y)-10)
    mod = mod + line_mod
    out  = mod.fit(y, pars, x=x)
    plt.plot(x, fit_channel )
    plt.plot(x, out.best_fit, '--k')
    plt.show()
    gauss_x = []; gauss_y = []; fit_channel = []
    print(out.fit_report(min_correl=10))
    for key in out.params:
        print(key, "=", out.params[key].value, "+/-", out.params[key].stderr)

energy_channel = list(zip(channel_max_list, energy_list_2))
energy_channel.sort(key=operator.itemgetter(0))

'''
Below plots the energy of the peaks and with their corresponding
energies.
'''
fig = plt.figure()
energy_list_2 =[]
for channel, energy in energy_channel:
    energy_list_2.append(float(energy))
for x, y in zip(energy_spectrum, energy_list_2):
    x1 = np.linspace(x,x, 10000) #plotting a horizontal line
    y1 = np.linspace(0, y,10000) #plotting a horizontal line
    p1 = plt.plot(x1,y1, 'b', linestyle = '--', zorder = 10)
    plt.annotate('%0.1f keV' % x, xy=(x, y+50), xytext=(x, y+50))
    plt.xlim(0, max(energy_spectrum)+100)
plt.semilogy(calibrated_channel, calibrate_data, 'k', zorder = 0)
plt.ylabel("Counts")
plt.xlabel("Energy(keV)")
plt.title("Calibrated Energy Plot")
plt.savefig('../images/Ba133_calibrated.png')
#argmax returns the position in the array where maximum occurs
print(energy_spectrum)
''' 
below compares the values of energy peaks to the know values
'''

i=0 
energy_peaks = np.zeros(6)

while i < 5:
     energy_peaks[i] = slope*channel_max_list[i]+intercept
     i += 1

channel_max_list = sorted(channel_max_list)
energy_peaks = sorted(energy_peaks)
energy_peaks[0] = slope*channel_max_list[0]+intercept

print(energy_peaks)
energy_spectrum = np.asarray(energy_spectrum)

delta = abs(energy_spectrum-energy_peaks)

print(delta)
