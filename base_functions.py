#usr/bin/python3
"""
Module statistics_lib.base_functions

Implements class to store a 2-tuple of the mean value of a measurement and its
associated uncertainty as well as basic arithmetics with this new data type.
The input data is supposed to be long sequences, which can be assumed to
represent the full population. Therefore, the Bessel corrections does not have
a lot of sense or importance. Hence, the 'base' versions of the functions do
not employ the Bessel correction. There are 'special versions' of the same
functions with the corrections, which have 'Bessel' suffix in their names.

Functions:
    
"""

__version__= '1.0.0.0'
__date__ = '07-02-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import math
import collections.abc as c_abc

from typing import Any, Sequence, Union, List, Tuple

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#types

TGenericSequence = Sequence[Any]

TReal = Union[int, float]

TRealList = List[TReal]

#functions

#+ helper functions - not for usage outside the module

def _CheckInput(Data: Any) -> None:
    """
    """
    pass

def _ExtractMeans(Data: TGenericSequence) -> TRealList:
    """
    """
    pass

def _ExtractErrors(Data: TGenericSequence) -> TRealList:
    """
    """
    pass

#+ 'public' functions to be available for everyone

#++ 1D statistics

#++ 2D statistics

#test area

if __name__ == '__main__':
    pass