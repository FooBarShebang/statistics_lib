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
    GetMean(Data, *, SkipFrames = 1, DoCheck = True)
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    GetVarianceP(Data, *, SkipFrames = 1, DoCheck = True)
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    GetStdevP(Data, *, SkipFrames = 1, DoCheck = True)
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    GetVarianceS(Data, *, SkipFrames = 1, DoCheck = True)
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    GetStdevS(Data, *, SkipFrames = 1, DoCheck = True)
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    GetSE(Data, *, SkipFrames = 1, DoCheck = True)
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    GetMeanSqrSE(Data, *, SkipFrames = 1, DoCheck = True)
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    GetFullSE(Data, *, SkipFrames = 1, DoCheck = True)
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
"""

__version__= '1.0.0.0'
__date__ = '08-02-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import math
import collections.abc as c_abc
from tkinter import S

from typing import Any, Sequence, Union, List, Tuple

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

from phyqus_lib.base_classes import MeasuredValue

#types

TGenericSequence = Sequence[Any]

TReal = Union[int, float]

TRealList = List[TReal]

#functions

#+ helper functions - not for usage outside the module

def _CheckPositiveInteger(Value: Any) -> None:
    """
    Raises an exception if the passed argument is not a positive integer.

    Signature:
        type A -> None
    
    Raises:
        UT_TypeError: the passed argument is not an integer
        UT_ValueError: the passed argument is an integer but not positive

    Version 1.0.0.0
    """
    if not isinstance(Value, int):
        raise UT_TypeError(Value, int, SkipFrames = 2)
    elif Value < 1:
        raise UT_ValueError(Value, '> 0 integer', SkipFrames = 2)

def _CheckInput(Data: Any, *, SkipFrames: int = 1) -> None:
    """
    Checks if the passed argument is a sequence of real numbers or measurements
    with uncertainty.

    Signature:
        type A/, * , int > 0/ -> None
    
    Args:
        Data: type A; any type to be checked, should be a sequence of real
            numbers or 'measurements with uncertainty' to avoid an exception
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if ((not isinstance(Data, c_abc.Sequence))
                                or (isinstance(Data, (str, bytes, bytearray)))):
        raise UT_TypeError(Data, (list, tuple), SkipFrames = SkipFrames)
    if not len(Data):
        raise UT_ValueError(len(Data), '> 0 - length of the sequence',
                                                        SkipFrames = SkipFrames)
    for Index, Element in enumerate(Data):
        if not isinstance(Element, (int, float)):
            if not (hasattr(Element, 'Value') and hasattr(Element, 'SE')):
                err = UT_TypeError(Element, (int, float, MeasuredValue),
                                                        SkipFrames = SkipFrames)
                err.args = ('{} at position {} in sequence'.format(err.args[0],
                                                                    Index), )
                raise err
    

def _ExtractMeans(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TRealList:
    """
    Extracts all 'mean' values from a mixed sequence of real numbers and the
    measurements with uncertainty, where the real numbers are treated as having
    zero uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> list(int OR float)
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, defautls to True
    
    Returns:
        list(int OR float): the extracted 'mean' values

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
        _CheckInput(Data, SkipFrames = SkipFrames + 1)
    Result = []
    for Item in Data:
        if isinstance(Item, (int, float)):
            Result.append(Item)
        else:
            Result.append(Item.Value)
    return Result

def _ExtractErrors(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TRealList:
    """
    Extracts all 'errors' values from a mixed sequence of real numbers and the
    measurements with uncertainty, where the real numbers are treated as having
    zero uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> list(int OR float)
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, defaults to True
    
    Returns:
        list(int OR float): the extracted 'error' values
    
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
        _CheckInput(Data, SkipFrames = SkipFrames + 1)
    Result = []
    for Item in Data:
        if isinstance(Item, (int, float)):
            Result.append(0)
        else:
            Result.append(Item.SE)
    return Result

#+ 'public' functions to be available for everyone

#++ 1D statistics

def GetMean(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the arithmetic mean of a mixed sequence of real numbers and the
    measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated mean value
    
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
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    Length = len(_Data)
    Sum = sum(Item for Item in _Data)
    Result = Sum / Length
    return Result

def GetVarianceP(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the population variance of a mixed sequence of real numbers and
    the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated variance value
    
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
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    Length = len(_Data)
    Mean = GetMean(_Data, SkipFrames = SkipFrames + 1, DoCheck = False)
    Sum = sum(pow(Item - Mean, 2) for Item in _Data)
    Result = Sum / Length
    return Result

def GetStdevP(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the population standard deviation of a mixed sequence of real
    numbers and the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated standard deviation value
    
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
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    Variance = GetVarianceP(_Data, SkipFrames = SkipFrames + 1,  DoCheck= False)
    Result = math.sqrt(Variance)
    return Result

def GetVarianceS(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the sample variance of a mixed sequence of real numbers and
    the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated variance value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is less than 2 elements long,
            OR any keyword argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    Length = len(_Data)
    if Length < 2:
        raise UT_ValueError(Length, '> 1 - sequence length',
                                                        SkipFrames = SkipFrames)
    Mean = GetMean(_Data, SkipFrames = SkipFrames + 1, DoCheck = False)
    Sum = sum(pow(Item - Mean, 2) for Item in _Data)
    Result = Sum / (Length - 1)
    return Result

def GetStdevS(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the sample standard deviation of a mixed sequence of real
    numbers and the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated standard deviation value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is less than 2 elements long,
            OR any keyword argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    Variance = GetVarianceS(_Data, SkipFrames = SkipFrames + 1,  DoCheck= False)
    Result = math.sqrt(Variance)
    return Result

def GetSE(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the standard error of the mean of a mixed sequence of real
    numbers and the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated standard error of the mean value
    
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
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    Variance = GetVarianceP(_Data, SkipFrames = SkipFrames + 1,  DoCheck= False)
    Result = math.sqrt(Variance / len(_Data))
    return Result

def GetMeanSqrSE(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the mean squared uncertainty of a mixed sequence of real
    numbers and the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated mean squared uncertainty value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    _Data = _ExtractErrors(Data, SkipFrames = SkipFrames + 1, DoCheck = DoCheck)
    Length = len(_Data)
    Sum = sum(pow(Item, 2) for Item in _Data)
    Result = Sum / Length
    return Result

def GetFullSE(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the full uncertainty of the mean of a mixed sequence of real
    numbers and the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasureValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasureValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated full uncertainty of the mean value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    Variance = GetVarianceP(Data, SkipFrames = SkipFrames + 1, DoCheck= DoCheck)
    MSSE = GetMeanSqrSE(Data, SkipFrames = SkipFrames + 1, DoCheck = False)
    Result = math.sqrt((Variance + MSSE) / len(Data))
    return Result

#++ 2D statistics