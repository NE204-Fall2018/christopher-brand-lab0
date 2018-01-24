import numpy as np

def gauss(x, A, B, C):
    """
    This is a 3-parameter gaussian function.

    A=Amplitude
    B=Centroid
    C= Std. dev.
    """
    '''
    use np version of the function because it will work on arrays or numbers
    '''
    return A*np.exp(-(x-B)**2/(2*C**2))
