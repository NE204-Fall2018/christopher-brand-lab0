import sys
sys.path.append('../')

from chrisBrand_lab0.code.modelling import gauss
from nose.tools import assert_almost_equal
#from chrisBrand_lab0.code.calibration_lab0 import spectrum_calibration
#from chrisBrand_lab0.code.gamma_energies import gamma_energies
import pytest

def test_gauss_symmetry():
    A = 100
    B = 0
    C = 1
    xr = 2.0
    xl = -xr
    assert_almost_equal(gauss(xr,A,B,C), gauss(xl,A,B,C))
#    assert_almost_equal(xr, A, B, C)
#    slope, intercept = spectrum_calibration(1, 2, np.array(range(4)))
