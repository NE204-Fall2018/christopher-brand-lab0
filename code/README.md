# NE 204 Report Lab0 Code Section

# Energy Calibration

## gamma_energies.py

gamma_energies.py is a function that takes a user input of isotopes
and returns the corresponding gamma-ray energies. An example input is shown.
The isotopes need to be separated by a comma

```
gamma_energies('Cs137', 'Am241', 'Co60')

```

## calibration.py

calibration.py is a function that takes the data that needs to be calibrated
and performs a linear calibration using the input from gamma_energies function.

It identifies the peaks within the spectrum and fits a gaussian model to these
peaks to find the centroid of the peaks. The fit uses lmfit. The code uses inputs
from calibration_lab0.py. Channel_width narrows the data lmfit tries to fit the
gaussian to.

Merged data is the combination of the Am241 and Cs137 dta.
```
spectrum_calibration(channel_width, energy_list, merged_data)

```

### calibration_lab0.py

This code is almost fully automated to run. Update
the gamma-ray energies you are interested in calibrating your spectrum with.
This line is found near 25
The width of the peaks to remove might need to be adjusted as well depending
on the peak sizes.
