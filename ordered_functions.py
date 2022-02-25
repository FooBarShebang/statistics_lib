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
    GetHistogram(Data, *, NBins=None, BinSize=None, SkipFrames=1, DoCheck=True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *,
            int > 0 OR None, int > 0 OR float > 0 OR None, int > 0, bool/
                -> dict(int OR float -> int >=0)
    GetModes(Data, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> list(int OR float)
    GetSpearman(DataX, DataY, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
                *, int > 0, bool/ -> int OR float
    GetKendall(DataX, DataY, *, SkipFrames = 1, DoCheck = True)
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
                *, int > 0, bool/ -> int OR float
"""

__version__= '1.0.0.0'
__date__ = '24-02-2022'
__status__ = 'Production'

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

from statistics_lib.base_functions import TGenericSequence, TReal, TRealList
from statistics_lib.base_functions import GetMean, GetPearsonR
from statistics_lib.base_functions import _ExtractMeans, _CheckPositiveInteger

#functions

#+ helper functions - not for usage outside the module

def _GetRanks(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TRealList:
    """
    Calculates the fractional ranks of the elements of a mixed sequence of real
    numbers and the measurements with uncertainty. Computation speed is always
    O(N*log(N)).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> list(int OR float)
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, convert the mixed sequence into a list of only real numbers
            and sort the values
    
    Returns:
        list(int OR float): the calculated ranks, in the same order as the
            initial sequence
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence of real numbers or
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
    _DataSorted = sorted(_Data)
    dictFrequencies = dict()
    for Item in _DataSorted:
        dictFrequencies[Item] = dictFrequencies.get(Item, 0) + 1
    dictRanks = dict()
    Last = 0
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 7:
        Keys = dictFrequencies.keys()
    else:
        Keys = sorted(dictFrequencies.keys())
    for Key in Keys:
        Value = dictFrequencies[Key]
        if Value == 1:
            dictRanks[Key] = Last + 1
        else:
            dictRanks[Key] = Last + (Value + 1) / 2
        Last += Value
    Result = [dictRanks[Key] for Key in _Data]
    return Result

#+ main, public functions

#++ 1D statistics

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
    
    Returns:
        int OR float: the calculated min value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence of real numbers or
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
    
    Returns:
        int OR float: the calculated max value
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence of real numbers or
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
        UT_TypeError: mandatory argument is not a sequence of real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = sorted(_ExtractMeans(Data, SkipFrames = SkipFrames + 2))
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
        UT_TypeError: mandatory argument is not a sequence of real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is shorter than 2 elements, OR
            any keyword argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = sorted(_ExtractMeans(Data, SkipFrames = SkipFrames + 2))
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
        UT_TypeError: mandatory argument is not a sequence of real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is shorter than 2 elements, OR
            any keyword argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if DoCheck:
        _Data = sorted(_ExtractMeans(Data, SkipFrames = SkipFrames + 2))
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
        UT_TypeError: mandatory argument is not a sequence of real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type, OR quantile index is not an integer, OR the total
            number of quantiles is not an integer
        UT_ValueError: passed mandatory sequence is shorter than 2 elements, OR
            any keyword argument is of the proper type but unacceptable value,
            OR the total number of quantilies is negative integer or zero, OR
            the quantile index is negative integer or integer greater than the
            total number of qunatiles

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    _CheckPositiveInteger(m)
    if not isinstance(k, int):
        raise UT_TypeError(k, int, SkipFrames = SkipFrames)
    if (k < 0) or (k > m):
        raise UT_ValueError(k, '>= 0 and <= {} - quantile index'.format(m))
    if DoCheck:
        _Data = sorted(_ExtractMeans(Data, SkipFrames = SkipFrames + 2))
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

def GetHistogram(Data: TGenericSequence, *, NBins: Optional[int] = None,
                        BinSize: Optional[TReal] = None, SkipFrames: int = 1,
                            DoCheck: bool = True) -> Dict[TReal, int]:
    """
    Calculates the histogram of number of apperance of 'mean' values belonging
    to the respective bins for the data sample. Either total number of bins OR
    the desired bin width can be specified, where number of bins takes the
    precedence. When neither value is defined, the default number of bins is 20.
    Computation speed is always O(N).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *,
            int > 0 OR None, int > 0 OR float > 0 OR None, int > 0, bool/
                -> dict(int OR float -> int >= 0)
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        NBins: (keyword) int > 0 OR None; the desired number of bins
        BinSize: (keyword) int > 0 OR float > 0 OR None; the desired bin size,
            ignored is NBins is passed as not None value
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, convert the mixed sequence into a list of only real numbers
    
    Returns:
        dict(int OR float -> int >= 0): the calculated histogram
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence of real numbers or
            measurements with uncertainty, OR any keyword argument is of
            improper type
        UT_ValueError: passed mandatory sequence is empty, OR any keyword
            argument is of the proper type but unacceptable value

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    if (NBins is None) and (BinSize is None):
        _NBins = 20
    elif not (NBins is None):
        _CheckPositiveInteger(NBins)
        _NBins = NBins
    else:
        if not isinstance(BinSize, (int, float)):
            raise UT_TypeError(BinSize, (int, float), SkipFrames = SkipFrames)
        elif BinSize <= 0:
            raise UT_ValueError(BinSize, '> 0 - bin size',
                                                        SkipFrames = SkipFrames)
        _NBins = None
    if DoCheck:
        _Data = _ExtractMeans(Data, SkipFrames = SkipFrames + 1)
    else:
        _Data = Data
    Min = min(_Data)
    Max = max(_Data)
    if not (_NBins is None):
        NSteps = _NBins
        if NSteps > 1:
            Start = round(Min, 16)
            Step = round((Max - Min) / (_NBins - 1), 16)
        else:
            Start = round(GetMean(_Data, DoCheck = False), 16)
            Step = 0
    else:
        Step = round(BinSize, 16)
        Mean = GetMean(_Data, DoCheck = False)
        NLeft = int(math.ceil((Mean - Min) / Step - 0.5))
        NRight = int(math.ceil((Max - Mean) / Step - 0.5))
        NSteps = NLeft + NRight + 1
        Start = Mean - NLeft * Step
    if Step == 0 or NSteps == 1:
        Result = {Start : len(_Data)}
    else:
        Temp = [0 for _ in range(NSteps)]
        for Item in _Data:
            Index = int((round(Item, 16) - Start) / Step + 0.5)
            if Index >= NSteps: #rounding-up errors
                Index = NSteps + 1
            elif Index < 0:
                Index = 0
            Temp[Index] += 1
        Result = {round(Start+Index*Step, 16) : Item
                                            for Index, Item in enumerate(Temp)}
    return Result

def GetModes(Data: TGenericSequence, *, SkipFrames: int = 1,
                                            DoCheck: bool = True) -> TRealList:
    """
    Calculates the mode(s) of a mixed sequence of real numbers and the
    measurements with uncertainty. Computation speed is always O(N).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/, *, int > 0,
            bool/ -> list(int OR float)
    
    Args:
        Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty'
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check, convert the mixed sequence into a list of only real numbers
    
    Returns:
        list(int OR float): the calculated modes
    
    Raises:
        UT_TypeError: mandatory argument is not a sequence of real numbers or
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
    dictTemp = dict()
    for Item in _Data:
        dictTemp[Item] = dictTemp.get(Item, 0) + 1
    MaxCount = max(dictTemp.values())
    Result = []
    for Key, Value in dictTemp.items():
        if Value == MaxCount:
            Result.append(Key)
    return Result

#++ 2D statistics

def GetSpearman(DataX: TGenericSequence, DataY: TGenericSequence, *,
                            SkipFrames: int = 1, DoCheck: bool = True) -> TReal:
    """
    Calculates the Spearman rank correlation coeffificent of the paired  mixed
    sequences of real numbers and the measurements with uncertainty. Computation
    speed is always O(N*log(N)).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
                *, int > 0, bool/ -> int OR float
    
    Args:
        DataX: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as X
        DataY: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as Y
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated rank correlation value
    
    Raises:
        UT_TypeError: any of mandatory data arguments is not a sequence of real
            numbers or measurements with uncertainty, OR any keyword argument is
            of improper type
        UT_ValueError: any of the passed mandatory sequence is empty, OR any
            keyword argument is of the proper type but unacceptable value, OR
            the X and Y sequences are of different length

    Version 1.0.0.0
    """
    _CheckPositiveInteger(SkipFrames)
    RankX = _GetRanks(DataX, SkipFrames = SkipFrames + 1, DoCheck = DoCheck)
    RankY = _GetRanks(DataY, SkipFrames = SkipFrames + 1, DoCheck = DoCheck)
    Length = len(RankX)
    if Length != len(RankY):
        raise UT_ValueError(
                Length, '== {} - X and Y data length'.format(len(RankY)),
                                                    SkipFrames = SkipFrames)
    if Length == 1:
        Result = 1
    else:
        Result = GetPearsonR(RankX, RankY, DoCheck = False)
    return Result

def GetKendall(DataX: TGenericSequence, DataY: TGenericSequence, *,
                            SkipFrames: int = 1, DoCheck: bool = True) -> TReal:
    """
    Calculates the Kendall rank correlation coeffificent of the paired  mixed
    sequences of real numbers and the measurements with uncertainty. Computation
    speed is always O(N^2).

    Signature:
        seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)/,
                *, int > 0, bool/ -> int OR float
    
    Args:
        DataX: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as X
        DataY: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue); a
            sequence of real numbers or 'measurements with uncertainty' as Y
        SkipFrames: (keyword) int > 0; how many frames to hide in the
            exception traceback, defaults to 1
        DoCheck: (keyword) bool; flag if to perform the input data sanity
            check and convert the mixed sequence into a list of only real
            numbers
    
    Returns:
        int OR float: the calculated rank correlation value
    
    Raises:
        UT_TypeError: any of mandatory data arguments is not a sequence of real
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
    Length = len(_DataX)
    if Length != len(_DataY):
        raise UT_ValueError(
                Length, '== {} - X and Y data length'.format(len(_DataY)),
                                                    SkipFrames = SkipFrames)
    if Length== 1:
        Result = 1
    else:
        NConcord = 0
        NDiscord = 0
        NXTies = 0
        NYTies = 0
        for FirstIdx in range(Length - 1):
            for SecondIdx in range(FirstIdx + 1, Length):
                X1 = _DataX[FirstIdx]
                X2 = _DataX[SecondIdx]
                Y1 = _DataY[FirstIdx]
                Y2 = _DataY[SecondIdx]
                if X1 == X2 and Y1 != Y2:
                    NXTies += 1
                elif X1 != X2 and Y1 == Y2:
                    NYTies += 1
                elif (X1 > X2 and Y1 > Y2) or (X1 < X2 and Y1 < Y2):
                    NConcord += 1
                elif (X1 > X2 and Y1 < Y2) or (X1 < X2 and Y1 > Y2):
                    NDiscord += 1
        Difference = NConcord - NDiscord
        Correction = math.sqrt((NConcord + NDiscord + NXTies) *
                                                (NConcord + NDiscord + NYTies))
        if Correction == 0:
            Result = 1
        else:
            Result = Difference / Correction
    return Result
