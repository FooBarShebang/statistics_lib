#usr/bin/python3
"""
Module statistics_lib.ordered_functions

Implements functions calculating the statistical properties of 1D or 2D data set
related to the shape of the sample data distribution. These functions accept a
generic sequence of a mixed integers, floating point number values and instances
of a class implementing 'measurements with uncertainty'.

The input data (sample) is treated as the entire population.

Functions:
    GetMin(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetMax(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetMedian(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetFirstQuartle(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetThirdQuartle(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetQuantile(Data, k, m, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue),
            int >= 0, int > 0/, *, int > 0, bool/ -> int OR float
"""

__version__= '1.0.0.0'
__date__ = '18-02-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os

from typing import Any, Sequence, Union, List

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

from phyqus_lib.base_classes import MeasuredValue

from statistics_lib.base_functions import TGenericSequence, TReal
from statistics_lib.base_functions import  _ExtractMeans, _CheckPositiveInteger

#functions

#+ helper functions - not for usage outside the module

def GetMin(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the minimum value of a mixed sequence of real numbers and the
    measurements with uncertainty. Computation speed is O(N), unless the passed
    sequence is already sorted in ascending order sequence of real numbers,
    which is indicated by the keyword argument DoCheck = False, in which case
    the calculation speed is O(1).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, convert the mixed sequence into a list of only real numbers
            and sort the values
    
    Returns:
        int OR float: the calculated min value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        Result = min(_ExtractMeans(Data, SkipFrames = SkipFrames + 1))
    else:
        Result = Data[0]
    return Result

def GetMax(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the maximum value of a mixed sequence of real numbers and the
    measurements with uncertainty. Computation speed is O(N), unless the passed
    sequence is already sorted in ascending order sequence of real numbers,
    which is indicated by the keyword argument DoCheck = False, in which case
    the calculation speed is O(1).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, convert the mixed sequence into a list of only real numbers
            and sort the values
    
    Returns:
        int OR float: the calculated max value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        Result = max(_ExtractMeans(Data, SkipFrames = SkipFrames + 1))
    else:
        Result = Data[-1]
    return Result

def GetMedian(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the median value of a mixed sequence of real numbers and the
    measurements with uncertainty. Computation speed is O(N*log(N)), unless the
    passed sequence is already sorted in ascending order sequence of real
    numbers, which is indicated by the keyword argument DoCheck = False, in
    which case the calculation speed is O(1).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, convert the mixed sequence into a list of only real numbers
            and sort the values
    
    Returns:
        int OR float: the calculated median value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = sorted(_ExtractMeans(Data, SkipFrames = SkipFrames + 1))
    else:
        _Data = Data
    N = len(_Data)
    if N == 1:
        Result = _Data[0]
    else:
        Index, Remainder = divmod(N, 2)
        if Remainder == 1:
            Result = _Data[Index]
        else:
            Result = (_Data[Index - 1] + _Data[Index]) / 2
    return Result

def GetFirstQuartile(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the first quartile value of a mixed sequence of real numbers and
    the measurements with uncertainty. Computation speed is O(N*log(N)), unless
    the passed sequence is already sorted in ascending order sequence of real
    numbers, which is indicated by the keyword argument DoCheck = False, in
    which case the calculation speed is O(1).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, convert the mixed sequence into a list of only real numbers
            and sort the values
    
    Returns:
        int OR float: the calculated Q1 value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = sorted(_ExtractMeans(Data, SkipFrames = SkipFrames + 1))
    else:
        _Data = Data
    N = len(_Data)
    if N == 1:
        raise UT_ValueError(N, '>= 2 - length of the sequence',
                                                        SkipFrames = SkipFrames)
    else:
        Index, Remainder = divmod(N - 1, 4)
        Portion = Remainder / 4
        Result = _Data[Index] * (1 - Portion) + _Data[Index + 1] * Portion
    return Result

def GetThirdQuartile(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the third quartile value of a mixed sequence of real numbers and
    the measurements with uncertainty. Computation speed is O(N*log(N)), unless
    the passed sequence is already sorted in ascending order sequence of real
    numbers, which is indicated by the keyword argument DoCheck = False, in
    which case the calculation speed is O(1).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, convert the mixed sequence into a list of only real numbers
            and sort the values
    
    Returns:
        int OR float: the calculated Q3 value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = sorted(_ExtractMeans(Data, SkipFrames = SkipFrames + 1))
    else:
        _Data = Data
    N = len(_Data)
    if N == 1:
        raise UT_ValueError(N, '>= 2 - length of the sequence',
                                                        SkipFrames = SkipFrames)
    else:
        Index, Remainder = divmod((N - 1) * 3, 4)
        Portion = Remainder / 4
        Result = _Data[Index] * (1 - Portion) + _Data[Index + 1] * Portion
    return Result

def GetQuantile(Data: TGenericSequence, k: int, m: int, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the k-th of m-quantile value of a mixed sequence of real numbers
    and the measurements with uncertainty. Computation speed is O(N*log(N)),
    unless the passed sequence is already sorted in ascending order sequence of
    real numbers, which is indicated by the keyword argument DoCheck = False, in
    which case the calculation speed is O(1).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue),
            int >= 0, int > 0/, *, int > 0, bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        k: int >= 0; the quantile index, between 0 and m inclusively
        m: int > 0; the total number of quantiles
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, convert the mixed sequence into a list of only real numbers
            and sort the values
    
    Returns:
        int OR float: the calculated Q3 value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type, OR quantile index is not an integer, OR the total
            number of quantiles is not an integer
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value, OR the total
            number of quantilies is negative integer or zero, OR the quantile
            index is negative integer or integer greater than the total number
            of qunatiles

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    _CheckPositiveInteger(m)
    if not isinstance(k, int):
        raise UT_TypeError(k, int, SkipFrames = SkipFrames)
    if (k < 0) or (k > m):
        raise UT_ValueError(k, '>= 0 and <= {} - quantile index'.format(m))
    if DoCheck:
        _Data = sorted(_ExtractMeans(Data, SkipFrames = SkipFrames + 1))
    else:
        _Data = Data
    N = len(_Data)
    if N == 1:
        raise UT_ValueError(N, '>= 2 - length of the sequence',
                                                        SkipFrames = SkipFrames)
    else:
        if k == m:
            Result = _Data[N-1]
        elif k == 0:
            Result = _Data[0]
        else:
            Index, Remainder = divmod((N - 1) * k, m)
            Portion = Remainder / m
            Result = _Data[Index] * (1 - Portion) + _Data[Index + 1] * Portion
    return Result