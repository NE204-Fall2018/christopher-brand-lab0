from code.modelling import gauss
from nose.tools import assert_almost_equal

def test_gauss_symmetry():
    A = 100
    B = 0
    C = 1
    xr = 2.0
    xl = -xr
    #assert gauss(xr, A, B, C) == gauss(xl, A,B,C)
    assert_almost_equal(xr, A, B, C)
