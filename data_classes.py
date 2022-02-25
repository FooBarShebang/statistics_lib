#usr/bin/python3
"""
Module statistics_lib.data_classes

Implements classes for storing (encapsulation) of 1D and 2D data sets as the
(paired) sequence(s) of real numbers (integers and / or floating point numbers)
and / or measurements with uncertainty, which are treated as the entire
population. The statistical properties of the population distribution are
calculated and returned on demand.

Classes:
    Statistics1D
    Statistics2D
"""

__version__= '1.0.0.0'
__date__ = '25-02-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import math

from typing import Optional, Dict

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

import statistics_lib.base_functions as bf
import statistics_lib.ordered_functions as of

#classes

class Statistics1D:
    """
    """
    pass

class Statistics2D:
    """
    """
    pass