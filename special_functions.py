#usr/bin/python3
"""
Module statistics_lib.special_functions

Implements special functions required for the implementation of the pdf(), cdf()
and qf() methods of the random distribution classes.

Functions:
    permutation(n, k)
        int >= 0, int >= 0 -> int > 0
    combination(n, k)
        int >= 0, int >= 0 -> int > 0
    log_beta(x, y)
        int > 0 OR float > 0, int > 0 OR float > 0 -> float
    beta(x, y)
        int > 0 OR float > 0, int > 0 OR float > 0 -> float > 0
"""

__version__= '1.0.0.0'
__date__ = '18-03-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import math

from typing import Union

from statistics_lib.base_functions import TReal

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#globals

#+ types

TReal = Union[int, float]

#+ helper constants

PYTHON_MAJOR = sys.version_info[0]

PYTHON_MINOR = sys.version_info[1]

IS_V3_8_PLUS = (PYTHON_MAJOR >= 3) and (PYTHON_MINOR >= 8)

#functions

#+ helper functions

#+ main set of functions

def permutation(n: int, k: int) -> int:
    """
    Calculates 'n permute k' value, i.e. n! / (n-k)!

    Signature:
        int >= 0 , int >= 0 -> int > 0
    
    Args:
        n: int >= 0; the total number of objects available
        k: int >= 0; the number of objects taken
    
    Raises:
        UT_TypeError: either of the arguments is not integer
        UT_ValueError: either of the arguments is negative, or k > n
    
    Version 1.0.0.0
    """
    if not isinstance(n, int):
        raise UT_TypeError(n, int, SkipFrames = 1)
    if not isinstance(k, int):
        raise UT_TypeError(k, int, SkipFrames = 1)
    if n < 0:
        raise UT_ValueError(n, '>= 0, number of objects', SkipFrames = 1)
    if k < 0:
        raise UT_ValueError(k, '>= 0, number of trials', SkipFrames = 1)
    if k > n:
        raise UT_ValueError(k,
                    '<= {}, number of trials <= number of objects'.format(n),
                                                                SkipFrames = 1)
    if IS_V3_8_PLUS:
        Result = math.perm(n, k)
    else:
        if k > 0:
            Result = n
            for i in range(1, k):
                Result *= (n - i)
        else:
            Result = 1
    return Result

def combination(n: int, k: int) -> int:
    """
    Calculates 'n chose k' value, i.e. n! / ((n-k)! k!)

    Signature:
        int >= 0 , int >= 0 -> int > 0
    
    Args:
        n: int >= 0; the total number of objects available
        k: int >= 0; the number of objects taken
    
    Raises:
        UT_TypeError: either of the arguments is not integer
        UT_ValueError: either of the arguments is negative, or k > n
    
    Version 1.0.0.0
    """
    if not isinstance(n, int):
        raise UT_TypeError(n, int, SkipFrames = 1)
    if not isinstance(k, int):
        raise UT_TypeError(k, int, SkipFrames = 1)
    if n < 0:
        raise UT_ValueError(n, '>= 0, number of objects', SkipFrames = 1)
    if k < 0:
        raise UT_ValueError(k, '>= 0, number of trials', SkipFrames = 1)
    if k > n:
        raise UT_ValueError(k,
                    '<= {}, number of trials <= number of objects'.format(n),
                                                                SkipFrames = 1)
    if IS_V3_8_PLUS:
        Result = math.comb(n, k)
    else:
        if k > n - k:
            Result = permutation(n, n - k) // math.factorial(n - k)
        else:
            Result = permutation(n, k) // math.factorial(k)
    return Result

def log_beta(x: TReal, y: TReal) -> float:
    """
    The value of the natural logarithm of beta function ln(B(x, y)).

    Signature:
        int > 0 OR float > 0, int > 0 OR float > 0 -> float
    
    Args:
        x: int >0 OR float > 0; any real number first argument
        y: int >0 OR float > 0; any real number second argument
    
    Raises:
        UT_TypeError: either of the arguments is not integer or float
        UT_ValueError: either of the arguments is not positive
    
    Version 1.0.0.0
    """
    if not isinstance(x, (int, float)):
        raise UT_TypeError(x, (int, float), SkipFrames = 1)
    if not isinstance(y, (int, float)):
        raise UT_TypeError(y, (int, float), SkipFrames = 1)
    if x <= 0:
        raise UT_ValueError(x, '> 0, x argument', SkipFrames = 1)
    if y <= 0:
        raise UT_ValueError(y, '> 0, y argument', SkipFrames = 1)
    Result = math.lgamma(x) + math.lgamma(y) - math.lgamma(x + y)
    return Result

def beta(x: TReal, y: TReal) -> float:
    """
    The value of beta function B(x, y).

    Signature:
        int > 0 OR float > 0, int > 0 OR float > 0 -> float > 0
    
    Args:
        x: int >0 OR float > 0; any real number first argument
        y: int >0 OR float > 0; any real number second argument
    
    Raises:
        UT_TypeError: either of the arguments is not integer or float
        UT_ValueError: either of the arguments is not positive
    
    Version 1.0.0.0
    """
    if not isinstance(x, (int, float)):
        raise UT_TypeError(x, (int, float), SkipFrames = 1)
    if not isinstance(y, (int, float)):
        raise UT_TypeError(y, (int, float), SkipFrames = 1)
    if x <= 0:
        raise UT_ValueError(x, '> 0, x argument', SkipFrames = 1)
    if y <= 0:
        raise UT_ValueError(y, '> 0, y argument', SkipFrames = 1)
    Result = math.lgamma(x) + math.lgamma(y) - math.lgamma(x + y)
    return math.exp(Result)
