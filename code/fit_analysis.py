'''
fit_analysis.py
fit_analysis.py analyzes a spectrum and creates an energy calibration.
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from modelling import gauss

fname = '../lab0_spectral_data.txt'
with open(fname, 'r') as f:
    first_line = f.readline()
    lis = first_line.split()
data = np.genfromtxt(fname, delimiter='', skip_header=1)
#parse the CSV data into fields we can use easily:
Am241 = data[:,0]
Ba133 = data[:,1]
Cs137 = data[:,2]
Co60 = data[:,3]
Eu152 = data[:,4]
#plt.figure(1)
#plt.semilogy(Cs137)

samples = np.random.normal(100, 2, 1000)
v, be, _ = plt.hist(samples, bins = 20, histtype="step")
#v is counts per bin; be is the bin edges
print(v.shape)
print(be.shape)
#want to convert bin edges to the center of the bin
bc = be[:-1] + np.diff(be)[0] / 2.
plt.plot(bc, v, 'o')

#we need to find the sample mean to calculate the centroid
a0= np.max(v)
#argmax returns the position in the array where maximum occurs
b0 = bc[np.argmax(v)]
c0 = 2
p0 = (a0, b0, c0)
curve_fit(gauss, bc, v, p0)
#we constrained our curve fit to certain parameters
popt, pcov = curve_fit(gauss, bc, v, p0)
plt.plot(bc, gauss(bc, *popt), 'g--')
plt.show()
#get_ipython().magic('hist -g')
#get_ipython().magic('rerun 257/1-5')
#get_ipython().magic('logstart ./code/fit_analysis.py')
#%logstart <file_name> saves your script in a file
#get_ipython().magic('logstart fit_analysis.py')
