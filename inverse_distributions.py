#usr/bin/python3
"""
Module statistics_lib.inverse_distributions

Classes:
    InverseGaussinan
    InverseGamma
    InverseChiSquared
    ScaledInverseChiSquared
    Cauchy
    Levy
"""

__version__= '1.0.0.0'
__date__ = '22-04-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import math

from typing import ClassVar, Tuple, Union

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

import statistics_lib.special_functions as sf

from statistics_lib.distribution_classes import ContinuousDistributionABC as BC

# classes

class InverseGaussian(BC):
    pass

class InverseGamma(BC):
    pass

class InverseChiSquared(BC):
    pass

class ScaledInverseChiSquared(InverseChiSquared):
    pass

class Cauchy(BC):
    pass

class Levy(Cauchy):
    pass
