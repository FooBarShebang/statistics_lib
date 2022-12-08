#usr/bin/python3
"""
Module statistics_lib.special_functions

Implements special functions required for the implementation of the pdf(), cdf()
and qf() methods of the random distribution classes.

Note, that this module simply defines aliases to the actual functions
implemented in the library math_extra_lib.

Functions:
    permutation(n, k)
        int >= 0, int >= 0 -> int > 0
    combination(n, k)
        int >= 0, int >= 0 -> int > 0
    log_beta(x, y)
        int > 0 OR float > 0, int > 0 OR float > 0 -> float
    beta(x, y)
        int > 0 OR float > 0, int > 0 OR float > 0 -> float > 0
    inv_erf(x)
        int = 0 OR -1 < float < 1 -> float
    lower_gamma(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> float >= 0
    log_lower_gamma(x, y)
        int > 0 OR float > 0, int > 0 OR float > 0 -> float
    lower_gamma_reg(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> 0 <= float < 1
    upper_gamma(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> float > 0
    log_upper_gamma(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> float
    upper_gamma_reg(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> 0 < float <= 1
    incomplete_beta(z, x, y)
        0 <= int <= 1 OR 0 < float < 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> float >= 0
    log_incomplete_beta(z, x, y)
        int = 1 OR 0 < float < 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> float
    incomplete_beta_reg(z, x, y)
        0 <= int <= 1 OR 0 < float < 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> 0 <= float <= 1
"""

__version__= '2.0.0.0'
__date__ = '08-12-2022'
__status__ = 'Production'

#imports

#+ standard library

import sys
import os

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import math_extra_lib.special_functions as sf

#functions aliases definitions

TReal = sf.TReal

permutation = sf.permutation

combination = sf.combination

log_beta = sf.log_beta

beta = sf.beta

inv_erf = sf.inv_erf

lower_gamma = sf.lower_gamma

log_lower_gamma = sf.log_lower_gamma

lower_gamma_reg = sf.lower_gamma_reg

upper_gamma = sf.upper_gamma

log_upper_gamma = sf.log_upper_gamma

upper_gamma_reg = sf.upper_gamma_reg

beta_incomplete = sf.beta_incomplete

log_beta_incomplete = sf.log_beta_incomplete

beta_incomplete_reg = sf.beta_incomplete_reg
