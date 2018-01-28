def spectrum_calibration(channel_width, energy_list, merged_data):
    import numpy as np
    import matplotlib.pyplot as plt
    #from scipy.optimize import curve_fit
    #from modelling import gauss
    import statsmodels.api as sm


    i = 0; channel_max_list = []
    while i < len(energy_list):
        channel_max = np.argmax(merged_data)
        data_left = channel_max - channel_width
        data_right = channel_max + channel_width
        del merged_data[data_left:data_right]
        channel_max_list.append(channel_max)
        i += 1

    '''
    sorting channel number so the correct channel number corresponds with
    the correct energy.
    '''
    channel_number = sorted(channel_max_list, key=int)
    energy = energy_list
    results = sm.OLS(energy,sm.add_constant(channel_number)).fit()

    slope, intercept = np.polyfit(channel_number, energy, 1)

    abline_values = [slope * i + intercept for i in channel_number]
    plt.plot(channel_number,energy, 'ro')
    plt.plot(channel_number, abline_values, 'b')
    plt.xlabel('ADC Val')
    plt.ylabel('Energy [keV]')
    plt.title('Best Fit Line')
    return slope, intercept
