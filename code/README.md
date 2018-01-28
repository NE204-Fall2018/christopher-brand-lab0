# NE 204 Report Lab0 Code Section

# Energy Calibration

## gamma_energies.py

gamma_energies.py is a function that takes a user input of isotopes
and returns the corresponding gamma-ray energies. An example input is shown. The isotopes need to be separated by a comma

```
gamma_energies('Cs137', 'Am241', 'Co60')

```

## calibration.py

calibration.py is a function that takes the data that needs to be calibrated
and performs a linear calibration using the input from gamma_energies function.

```
spectrum_calibration(channel_width, energy_list, merged_data)

```

### calibration_lab0.py

This code is almost fully automated to run. Enter the gamma-ray energies you
are interested in calibrating your spectrum with by updating
energy_calibration within the code.
The width of the peaks to remove might need to be adjusted as well depending
on the peak sizes.
