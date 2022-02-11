#usr/bin/python3
"""
Module statistics_lib.base_functions

Implements class to store a 2-tuple of the mean value of a measurement and its
associated uncertainty as well as basic arithmetics with this new data type.
The input data is supposed to be long sequences, which can be assumed to
represent the full population. Therefore, the Bessel corrections does not have
a lot of sense or importance. Hence, the 'base' versions of the functions do
not employ the Bessel correction, and they have 'P' suffix in their neames.
There are 'special versions' of the same functions with the corrections, which
have 'S' suffix in their names. The generic moments, standard error, covariance
and correlation functions assume that the passed data represent the entire
population.

Functions:
    GetMean(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetVarianceP(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetStdevP(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetVarianceS(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetStdevS(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetSE(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetMeanSqrSE(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetFullSE(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetMoment(Data, Power, *, IsCentral = False, IsNormalized = False,
                                                SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue), int > 0/,
            *, bool, bool, int > 0, bool/ -> int OR float
    GetSkewnessP(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetSkewnessS(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetKurtosisP(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetKurtosisS(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    GetCovariance(DataX, DataY, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
                *, int > 0, bool/ -> int OR float
    GetMoment2(DataX, DataY, PowerX, PowerY, *, IsCentral = False,
                        IsNormalized = False, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue),
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue),
                int > 0, int > 0/, *, bool, bool, int > 0, bool/ -> int OR float
    GetPearsonR(DataX, DataY, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
                *, int > 0, bool/ -> int OR float
"""

__version__= '1.0.0.0'
__date__ = '10-02-2022'
__status__ = 'Production'

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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> list(int OR float)
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> list(int OR float)
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
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

def GetMoment(Data: TGenericSequence, Power: int, *, IsCentral: bool = False,
                IsNormalized: bool = False, SkipFrames: int = 1,
                    DoCheck: bool = True) -> TReal:
    """
    Calculates the generic N-th moment of a mixed sequence of real numbers and
    the measurements with uncertainty, which can be central or non-central,
    normailized or not normalized, depending on the values of the keyword
    arguments.

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue), int > 0/,
            *, bool, bool, int > 0, bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        Power: int > 0; the moment power
        IsCentral: (keyword) bool; is the central moment is to be calculated,
            defaults to False
        IsNormalized: (keyword) bool; is the normalized moment is to be
            calculated, defaults to False
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated moment value
    
    Raises:
        UT_TypeError: the mandatory data argument is not a sequence or real
            numbers or measurements with uncertainty, OR the moment power is not
            an integer number, OR any keyword argument is of improper type
        UT_ValueError: passed mandatory sequence is empty, OR the moment power
            is zero or negative integer, OR any keyword argument is of the
            proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(Power)
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    if IsCentral:
        Mean = GetMean(_Data, SkipFrames = SkipFrames + 1, DoCheck = False)
    else:
        Mean = 0
    if IsNormalized:
        Sigma = GetStdevP(_Data, SkipFrames = SkipFrames + 1, DoCheck = False)
    else:
        Sigma = 1
    Length = len(_Data)
    Eps = sys.float_info.epsilon
    First = _Data[0]
    bCond = any(map(lambda x: abs(x - First) > Eps, _Data))
    if bCond:
        Sum = sum(pow((Item - Mean) / Sigma, Power) for Item in _Data)
        Result = Sum / Length
    else: #all elements are the same!!!!
        if IsNormalized and (not IsCentral):
            raise UT_ValueError(Sigma, '!= 0 - variance of the data',
                                                        SkipFrames = SkipFrames)
        elif (not IsNormalized) and (not IsCentral):
            Result = sum(pow(Item, Power) for Item in _Data) / Length
        else:
            Result = 0
    return Result

def GetSkewnessP(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the population skewness of a mixed sequence of real numbers and
    the measurements with uncertainty.

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated skewness value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    Result = GetMoment(Data, 3, IsCentral = True, IsNormalized = True,
                                SkipFrames = SkipFrames + 1, DoCheck= DoCheck)
    return Result

def GetSkewnessS(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the sample skewness of a mixed sequence of real numbers and the
    measurements with uncertainty.

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated skewness value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is less than 3 elements long,
            OR any keyword argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    Length = len(_Data)
    if Length < 3:
        raise UT_ValueError(Length, '> 2 - sequence length',
                                                        SkipFrames = SkipFrames)
    Skew = GetSkewnessP(_Data, SkipFrames = SkipFrames + 1, DoCheck= False)
    Result = math.sqrt(Length * (Length - 1)) * Skew / (Length - 2)
    return Result

def GetKurtosisP(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the population excess kurtosis of a mixed sequence of real
    numbers and the measurements with uncertainty.

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated excess kurtosis value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    Result = GetMoment(Data, 4, IsCentral = True, IsNormalized = True,
                            SkipFrames = SkipFrames + 1, DoCheck= DoCheck) - 3
    return Result

def GetKurtosisS(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TReal:
    """
    Calculates the sample excess kurtosis of a mixed sequence of real numbers
    and the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> int OR float
    
    Args:
        Data: list(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated skewness value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence or real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is less than 4 elements long,
            OR any keyword argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    Length = len(_Data)
    if Length < 4:
        raise UT_ValueError(Length, '> 3 - sequence length',
                                                        SkipFrames = SkipFrames)
    Kurt = GetKurtosisP(_Data, SkipFrames = SkipFrames + 1, DoCheck= False)
    Temp = (Length - 1) * ((Length + 1) * Kurt  + 6)
    Result = Temp / ((Length - 2) * (Length - 3))
    return Result

#++ 2D statistics

def GetCovariance(DataX: TGenericSequence, DataY: TGenericSequence, *,
                            SkipFrames: int = 1, DoCheck: bool = True) -> TReal:
    """
    Calculates the covariance of the paired  mixed sequences of real numbers and
    the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
            list(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
                *, int > 0, bool/ -> int OR float
    
    Args:
        DataX: list(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as X
        DataY: list(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as Y
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated covariance value
    
    Raises:
        UT_TypeError: any of mandatory data arguments is not a sequence or real
            numbers or measurements with uncertainty, OR any keyword argument is
            of improper type
        UT_ValueError: any of the passed mandatory sequence is empty, OR any
            keyword argument is of the proper type but unacceptable value, OR
            the X and Y sequences are of different length

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _DataX = _ExtractMeans(DataX, SkipFrames = SkipFrames + 1)
        _DataY = _ExtractMeans(DataY, SkipFrames = SkipFrames + 1)
    else:
        _DataX = DataX
        _DataY = DataY
    if len(_DataX) != len(_DataY):
        raise UT_ValueError(
                len(_DataX), '== {} - X and Y data length'.format(len(_DataY)))
    MeanX = GetMean(_DataX, SkipFrames = SkipFrames + 1, DoCheck = False)
    MeanY = GetMean(_DataY, SkipFrames = SkipFrames + 1, DoCheck = False)
    Length = len(_DataX)
    Sum = sum((Item - MeanX) * (_DataY[Index] - MeanY)
                                        for Index, Item in enumerate(_DataX))
    Result = Sum / Length
    return Result

def GetMoment2(DataX: TGenericSequence, DataY: TGenericSequence, PowerX: int,
                    PowerY: int, *, IsCentral: bool = False,
                        IsNormalized: bool = False, SkipFrames: int = 1,
                            DoCheck: bool = True) -> TReal:
    """
    Calculates the generic N-th / M-th moment of the paired mixed sequences of
    real numbers and the measurements with uncertainty, which can be central or
    non-central, normailized or not normalized, depending on the values of the
    keyword arguments.

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue),
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue),
                int > 0, int > 0/, *, bool, bool, int > 0, bool/ -> int OR float
    
    Args:
        DataX: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as X
        DataY: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as Y
        PowerX: int > 0; the moment power of X
        PowerY: int > 0; the moment power of Y
        IsCentral: (keyword) bool; is the central moment is to be calculated,
            defaults to False
        IsNormalized: (keyword) bool; is the normalized moment is to be
            calculated, defaults to False
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated moment value
    
    Raises:
        UT_TypeError: any of mandatory data arguments is not a sequence or real
            numbers or measurements with uncertainty, OR any moment power is
            not an integer number, OR any keyword argument is of improper type
        UT_ValueError: any of the passed mandatory sequence is empty, OR any
            moment power is zero or negative integer, OR any keyword argument is
            of the proper type but unacceptable value, OR the X and Y sequences
            are of different length

    Version 1.0.0.0
    """
    _CheckPositiveInteger(PowerX)
    _CheckPositiveInteger(PowerY)
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _DataX = _ExtractMeans(DataX, SkipFrames = SkipFrames + 1)
        _DataY = _ExtractMeans(DataY, SkipFrames = SkipFrames + 1)
    else:
        _DataX = DataX
        _DataY = DataY
    if len(_DataX) != len(_DataY):
        raise UT_ValueError(
                len(_DataX), '== {} - X and Y data length'.format(len(_DataY)))
    Length = len(_DataX)
    if IsCentral:
        MeanX = GetMean(_DataX, SkipFrames = SkipFrames + 1, DoCheck = False)
        MeanY = GetMean(_DataY, SkipFrames = SkipFrames + 1, DoCheck = False)
    else:
        MeanX = 0
        MeanY = 0
    if IsNormalized:
        SigmaX = GetStdevP(_DataX, SkipFrames = SkipFrames + 1, DoCheck = False)
        SigmaY = GetStdevP(_DataY, SkipFrames = SkipFrames + 1, DoCheck = False)
    else:
        SigmaX = 1
        SigmaY = 1
    Eps = sys.float_info.epsilon
    First = _DataX[0]
    bCond1 = any(map(lambda x: abs(x - First) > Eps, _DataX))
    First = _DataY[0]
    bCond2 = any(map(lambda x: abs(x - First) > Eps, _DataY))
    if bCond1 and bCond2:
        Sum = sum((pow((Item - MeanX) / SigmaX, PowerX) *
                pow((_DataY[Index] - MeanY) / SigmaY, PowerY))
                                        for Index, Item in enumerate(_DataX))
        Result = Sum / Length
    else: #at least, in one sequence all items are the same!!!
        if IsNormalized and (not IsCentral):
            raise UT_ValueError((SigmaX, SigmaY), '!= 0 - variance of the data',
                                                        SkipFrames = SkipFrames)
        elif (not IsNormalized) and (not IsCentral):
            Result = sum(pow(Item, PowerX) * pow(_DataY[Index], PowerY)
                                for Index, Item in enumerate(_DataX)) / Length
        else: # any central moment
            Result = 0
    return Result

def GetPearsonR(DataX: TGenericSequence, DataY: TGenericSequence, *,
                            SkipFrames: int = 1, DoCheck: bool = True) -> TReal:
    """
    Calculates the Pearson`s correlation coefficient r of the paired  mixed
    sequences of real numbers and the measurements with uncertainty.

    Signature:
        list(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
            list(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
                *, int > 0, bool/ -> int OR float
    
    Args:
        DataX: list(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as X
        DataY: list(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as Y
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the correlation value
    
    Raises:
        UT_TypeError: any of mandatory data arguments is not a sequence or real
            numbers or measurements with uncertainty, OR any keyword argument is
            of improper type
        UT_ValueError: any of the passed mandatory sequence is empty, OR any
            keyword argument is of the proper type but unacceptable value, OR
            the X and Y sequences are of different length

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _DataX = _ExtractMeans(DataX, SkipFrames = SkipFrames + 1)
        _DataY = _ExtractMeans(DataY, SkipFrames = SkipFrames + 1)
    else:
        _DataX = DataX
        _DataY = DataY
    Covariance = GetCovariance(_DataX, _DataY, SkipFrames = SkipFrames + 1,
                                                                DoCheck = False)
    SigmaX = GetStdevP(_DataX, SkipFrames = SkipFrames + 1, DoCheck = False)
    SigmaY = GetStdevP(_DataY, SkipFrames = SkipFrames + 1, DoCheck = False)
    if SigmaX > 0 and SigmaY > 0:
        Result = Covariance / (SigmaX * SigmaY)
    elif (SigmaX > 0)  or (SigmaY > 0): #one sequence is constant
        Result = 0
    else: #both sequences are constants
        Result = 1
    return Result