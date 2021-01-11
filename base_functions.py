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
    GetMean(Data):
        seq(type A) -> float
    GetMeanSquares(Data):
        seq(type A) -> float
    GetVariance(Data):
        seq(type A) -> float
    GetVarianceBessel(Data):
        seq(type A) -> float
    GetStandardDeviation(Data):
        seq(type A) -> float
    GetStandardDeviationBessel(Data):
        seq(type A) -> float
    GetStandardError(Data):
        seq(type A) -> float
    GetFullStandardError(Data):
        seq(type A) -> float
    GetSkewness(Data):
        seq(type A) -> float
    GetSkewnessBessel(Data):
        seq(type A) -> float
    GetKurtosis(Data):
        seq(type A) -> float
    GetKurtosisBessel(Data):
        seq(type A) -> float
    GetMoment(Data, N, *, IsCentral = True):
        seq(type A), int > 0 /, bool/ -> float
    GetCovariance(DataX, DataY):
        seq(type A), seq(type A) -> float
    GetMoment2(DataX, DataY, NX, NY, *, IsCentral = True):
        seq(type A), seq(type A), int > 0, int > 0 /, bool/ -> float
    GetPearsonR(DataX, DataY):
        seq(type A), seq(type A) -> float

Considering the standard spreadsheet applications (MS Excel, LibreOffice Calc)
the following functions correspondence is implemented:

    * MEAN() -> GetMean()
    * STDEV.P() -> GetStandardDeviation()
    * STDEV.S() -> GetStandardDeviationBessel()
    * VAR.P() -> GetVariance()
    * VAR.S() -> GetVarianceBessel()
    * SKEWP() -> GetSkewness()
    * SKEW() -> GetSkewnessBessel()
    * KURT() -> GetKurtosisBessel()
    * COVARIANCE.P() -> GetCovariance()
    * PEARSON() -> GetPearsonR()
"""

__version__= '1.0.0.0'
__date__ = '11-01-2021'
__status__ = 'Production'

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

#functions

#+ helper functions - not for usage outside the module

def _ExtractMeans(Data: TGenericSequence) -> List[TReal]:
    """
    Helper function to unify the mixed input data and to perform the data sanity
    checks. Extracts the values supposed to represent the 'mean' values of the
    measurements data point with the associated measurement uncertainties.

    Sequence:
        seq(type A) -> list(int OR float)
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        list(int OR float): extracted 'mean' values of the data

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    if not isinstance(Data, c_abc.Sequence):
        raise UT_TypeError(Data, c_abc.Sequence, SkipFrames = 2)
    elif not len(Data):
        raise UT_ValueError(len(Data), '> 0 - sequence length', SkipFrames = 2)
    lstResult = []
    for Index, Value in enumerate(Data):
        if isinstance(Value, (int, float)):
            lstResult.append(Value)
        elif hasattr(Value, 'Value'):
            lstResult.append(Value.Value)
        else:
            objError = UT_TypeError(Value, (int, float), SkipFrames = 2)
            strMessage = objError.args[0]
            strNewMessage ='{} - index {} in sequence'.format(strMessage, Index)
            objError.args = (strNewMessage,)
            raise objError
    return lstResult

def _ExtractMeans2(DataX: TGenericSequence,
                    DataY: TGenericSequence) -> Tuple[List[TReal], List[TReal]]:
    """
    Helper function to unify the mixed input data and to perform the data sanity
    checks. Extracts the values supposed to represent the 'mean' values of the
    measurements data point with the associated measurement uncertainties.

    Sequence:
        seq(type A) -> list(int OR float)
    
    Args:
        DataX: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
            - the first data set sequence
        DataY: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
            - the second data set sequence
    
    Returns:
        list(int OR float), list(int OR float): extracted 'mean' values of the
            both data sets as an unpacked tuple of two lists

    Raises:
        UT_TypeError: any of the passed arguments is not a sequence, OR any of
            their elements is not a real number (int or float, 'is a' check) or
            an instance of 'real life measurement' class ('has a' check)
        UT_ValueError: any of the passed sequence is empty, OR their lengths are
            not equal
    
    Version 1.0.0.0
    """
    if not isinstance(DataX, c_abc.Sequence):
        objError = UT_TypeError(DataX, c_abc.Sequence, SkipFrames = 2)
        strMessage = objError.args[0]
        strNewMessage = '{} - the X data set'.format(strMessage)
        objError.args = (strNewMessage,)
        raise objError
    elif not len(DataX):
        raise UT_ValueError(len(DataX), '> 0 - X sequence length', SkipFrames=2)
    if not isinstance(DataY, c_abc.Sequence):
        objError = UT_TypeError(DataY, c_abc.Sequence, SkipFrames = 2)
        strMessage = objError.args[0]
        strNewMessage = '{} - the Y data set'.format(strMessage)
        objError.args = (strNewMessage,)
        raise objError
    elif not len(DataY):
        raise UT_ValueError(len(DataY), '> 0 - Y sequence length', SkipFrames=2)
    iNX = len(DataX)
    iNY = len(DataY)
    if iNX != iNY:
        raise UT_ValueError(iNX, '== {} - data sets length'.format(iNY),
                                                                SkipFrames = 2)
    lstDataX = []
    for Index, Value in enumerate(DataX):
        if isinstance(Value, (int, float)):
            lstDataX.append(Value)
        elif hasattr(Value, 'Value'):
            lstDataX.append(Value.Value)
        else:
            objError = UT_TypeError(Value, (int, float), SkipFrames = 2)
            strMessage = objError.args[0]
            strNewMessage ='{} - index {} in X data set'.format(strMessage,
                                                                        Index)
            objError.args = (strNewMessage,)
            raise objError
    lstDataY = []
    for Index, Value in enumerate(DataY):
        if isinstance(Value, (int, float)):
            lstDataY.append(Value)
        elif hasattr(Value, 'Value'):
            lstDataY.append(Value.Value)
        else:
            objError = UT_TypeError(Value, (int, float), SkipFrames = 2)
            strMessage = objError.args[0]
            strNewMessage ='{} - index {} in Y data set'.format(strMessage,
                                                                        Index)
            objError.args = (strNewMessage,)
            raise objError
    return lstDataX, lstDataY

def _ExtractErrors(Data: TGenericSequence) -> List[TReal]:
    """
    Helper function to unify the mixed input data and to perform the data sanity
    checks. Extracts the values supposed to represent the 'error' values of the
    measurements data point with the associated measurement uncertainties.

    Sequence:
        seq(type A) -> list(int OR float)
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        list(int OR float): extracted uncertainty values of the data

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    if not isinstance(Data, c_abc.Sequence):
        raise UT_TypeError(Data, c_abc.Sequence, SkipFrames = 2)
    elif not len(Data):
        raise UT_ValueError(len(Data), '> 0 - sequence length', SkipFrames = 2)
    lstResult = []
    for Index, Value in enumerate(Data):
        if isinstance(Value, (int, float)):
            lstResult.append(0)
        elif hasattr(Value, 'SE'):
            lstResult.append(Value.SE)
        else:
            objError = UT_TypeError(Value, (int, float), SkipFrames = 2)
            strMessage = objError.args[0]
            strNewMessage ='{} - index {} in sequence'.format(strMessage, Index)
            objError.args = (strNewMessage,)
            raise objError
    return lstResult

#+ functions to be available for everyone

#++ 1D statistics

def GetMean(Data: TGenericSequence) -> float:
    """
    Calculates the arithmetic mean of a sequence, which can be a mix of int or
    float (real) numbers and instances of the 'real life measurements' class,
    i.e. the 2-tuples of the 'mean' value of a measurement and the associated
    measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the arithmetic mean of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    fSum = math.fsum(lstData)
    fResult = fSum / iN
    return fResult

def GetMeanSquares(Data: TGenericSequence) -> float:
    """
    Calculates the arithmetic mean of the squares of the values in a sequence,
    which can be a mix of int or float (real) numbers and instances of the
    'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a
    measurement and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the arithmetic mean of the squares of the values in the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    fSum = math.fsum(Item**2 for Item in lstData)
    fResult = fSum / iN
    return fResult

def GetVariance(Data: TGenericSequence) -> float:
    """
    Calculates the variance of the values in a sequence (without the Bessel
    correction, i.e. assuming the sequence is the full population), which can be
    a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the population variance of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum = math.fsum((Item - fMean)**2 for Item in lstData)
    fResult = fSum / iN
    return fResult

def GetVarianceBessel(Data: TGenericSequence) -> float:
    """
    Calculates the variance of the values in a sequence (with the Bessel
    correction, i.e. assuming the sequence is not full population), which can be
    a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the sample variance of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is shoerter than 2 elements
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    if iN == 1:
        raise UT_ValueError(iN, '> 1 - sequence length', SkipFrames = 2)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum = math.fsum((Item - fMean)**2 for Item in lstData)
    fResult = fSum / (iN - 1)
    return fResult

def GetStandardDeviation(Data: TGenericSequence) -> float:
    """
    Calculates the Std.Deviation of the values in a sequence (without the Bessel
    correction, i.e. assuming the sequence is the full population), which can be
    a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the population standard deviation of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum = math.fsum((Item - fMean)**2 for Item in lstData)
    fResult = math.sqrt(fSum / iN)
    return fResult

def GetStandardDeviationBessel(Data: TGenericSequence) -> float:
    """
    Calculates the Std.Deviation of the values in a sequence (with the Bessel
    correction, i.e. assuming the sequence is not full population), which can be
    a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the sample standard deviation of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is shorter than 2 elements
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    if iN == 1:
        raise UT_ValueError(iN, '> 1 - sequence length', SkipFrames = 2)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum = math.fsum((Item - fMean)**2 for Item in lstData)
    fResult = math.sqrt(fSum / (iN - 1))
    return fResult

def GetStandardError(Data: TGenericSequence) -> float:
    """
    Calculates the standard error of the mean of the values in a sequence
    (without the Bessel correction, i.e. assuming the sequence is the full
    population) and without the acccount for the measurements uncertainties,
    which sequence can be a mix of int or float (real) numbers and instances of
    the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of
    a measurement and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the simple SE of the mean of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum = math.fsum((Item - fMean)**2 for Item in lstData)
    fResult = math.sqrt(fSum / (iN**2))
    return fResult

def GetFullStandardError(Data: TGenericSequence) -> float:
    """
    Calculates the standard error of the mean of the values in a sequence
    (without the Bessel correction, i.e. assuming the sequence is the full
    population) and including the individual measurements uncertainties,
    which sequence can be a mix of int or float (real) numbers and instances of
    the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of
    a measurement and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the 'full' SE of the mean of the sequence, including the
            individual measurements uncertainties

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum2 = math.fsum((Item - fMean)**2 for Item in lstData)
    lstData = _ExtractErrors(Data)
    fSum = math.fsum(lstData)
    fResult = math.sqrt((fSum2 + fSum**2) / (iN**2))
    return fResult

def GetSkewness(Data: TGenericSequence) -> float:
    """
    Calculates the skewness of the values in a sequence (without the Bessel
    correction, i.e. assuming the sequence is the full population), which can be
    a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the population skewness of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum2 = math.fsum((Item - fMean)**2 for Item in lstData)
    fSigma = math.sqrt(fSum2 / iN)
    fResult = math.fsum(((Item - fMean) / fSigma)**3 for Item in lstData) / iN
    return fResult

def GetSkewnessBessel(Data: TGenericSequence) -> float:
    """
    Calculates the skewness of the values in a sequence (with the Bessel
    correction, i.e. assuming the sequence is not full population), which can be
    a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the sample skewness of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is shorter than 3 elements
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    if iN < 3:
        raise UT_ValueError(iN, '> 2 - sequence length', SkipFrames = 2)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum2 = math.fsum((Item - fMean)**2 for Item in lstData)
    fSigma = math.sqrt(fSum2 / iN)
    fResult = math.fsum(((Item - fMean) / fSigma)**3 for Item in lstData)
    fResult *= math.sqrt((iN -1) / iN) / (iN - 2)
    return fResult

def GetKurtosis(Data: TGenericSequence) -> float:
    """
    Calculates the excess kurtosis of the values in a sequence (without the
    Bessel correction, i.e. assuming the sequence is the full population), which
    can be a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the population excess kurtosis of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is empty
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum2 = math.fsum((Item - fMean)**2 for Item in lstData)
    fSigma = math.sqrt(fSum2 / iN)
    fResult = math.fsum(((Item - fMean) / fSigma)**4 for Item in lstData) / iN
    fResult -= 3
    return fResult

def GetKurtosisBessel(Data: TGenericSequence) -> float:
    """
    Calculates the excess kurtosis of the values in a sequence (with the Bessel
    correction, i.e. assuming the sequence is not full population), which can be
    a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty.

    Sequence:
        seq(type A) -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
    
    Returns:
        float: the sample excess kurtosis of the sequence

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check)
        UT_ValueError: the passed sequence is shorter than 4 elements
    
    Version 1.0.0.0
    """
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    if iN < 4:
        raise UT_ValueError(iN, '> 3 - sequence length', SkipFrames = 2)
    fSum = math.fsum(lstData)
    fMean = fSum / iN
    fSum2 = math.fsum((Item - fMean)**2 for Item in lstData)
    fSigma = math.sqrt(fSum2 / iN)
    fResult = math.fsum(((Item - fMean) / fSigma)**4 for Item in lstData)
    fResult *= ((iN + 1) * (iN - 1)) / (iN * (iN - 2) * (iN - 3))
    fResult -= 3 * (((iN - 1)**2) / ((iN - 2) * (iN -3)))
    return fResult

def GetMoment(Data: TGenericSequence, N: int, *,
                                            IsCentral: bool = True) -> float:
    """
    Calculates the Nth moment of the values in a sequence (without the Bessel
    correction, i.e. assuming the sequence is the full population), which can be
    a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty. By default, the central moment
    is calculated, pass keyword argument IsCentral = False explicitely to
    calculated a non-central moment.

    Sequence:
        seq(type A), int > 0 /, bool/ -> float
    
    Args:
        Data: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
        N: int > 0; the power of the moment
        IsCentral: (keyword) bool; flag if the central moment should be
            calculated, defaults to True
    
    Returns:
        float: the calculated moment

    Raises:
        UT_TypeError: the passed argument is not a sequence, OR any of its
            elements is not a real number (int or float, 'is a' check) or an
            instance of 'real life measurement' class ('has a' check); OR the
            second passed argument is not an integer
        UT_ValueError: the passed sequence is empty; OR the second passed
            argument is not positive
    
    Version 1.0.0.0
    """
    if not isinstance(N, int):
        objError = UT_TypeError(N, int, SkipFrames = 1)
        strMessage = objError.args[0]
        strNewMessage = '{} - moment power'.format(strMessage)
        objError.args = (strNewMessage, )
        raise objError
    elif N < 1:
        raise UT_ValueError(N, '> 0 - moment power', SkipFrames = 1)
    lstData = _ExtractMeans(Data)
    iN = len(lstData)
    if IsCentral:
        fSum = math.fsum(lstData)
        fMean = fSum / iN
    else:
        fMean = 0.0
    fSum = math.fsum((Item - fMean)**N for Item in lstData)
    fResult = fSum / iN
    return fResult

#++ 2D statistics

def GetCovariance(DataX: TGenericSequence,
                    DataY: TGenericSequence) -> float:
    """
    Calculates the covariance of the values in two data sets (without the Bessel
    correction, i.e. assuming the sequence is the full population), which can be
    a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty.

    Sequence:
        seq(type A), seq(type A), int > 0, int > 0 /, bool/ -> float
    
    Args:
        DataX: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
            - the first data set sequence
        DataY: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
            - the second data set sequence
    
    Returns:
        float: the calculated covariance

    Raises:
        UT_TypeError: any of the passed data sets is not a sequence, OR any of
            their elements is not a real number (int or float, 'is a' check) or
            an instance of 'real life measurement' class ('has a' check)
        UT_ValueError: any of the passed sequence is empty, OR their lengths are
            not equal
    
    Version 1.0.0.0
    """
    lstDataX, lstDataY = _ExtractMeans2(DataX, DataY)
    iN = len(lstDataX)
    fSum = math.fsum(lstDataX)
    fMeanX = fSum / iN
    fSum = math.fsum(lstDataY)
    fMeanY = fSum / iN
    fSum = math.fsum((Item - fMeanX)*(lstDataY[iId] - fMeanY)
                                        for iId, Item in enumerate(lstDataX))
    fResult = fSum / iN
    return fResult

def GetMoment2(DataX: TGenericSequence,
                    DataY: TGenericSequence, NX: int, NY: int, *,
                                            IsCentral: bool = True) -> float:
    """
    Calculates the Nth-Mth moment of the values in two data sets (without the
    Bessel correction, i.e. assuming the sequence is the full population), which
    can be a mix of int or float (real) numbers and instances of the 'real life
    measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement
    and the associated measurement uncertainty. By default, the central moment
    is calculated, pass keyword argument IsCentral = False explicitely to
    calculated a non-central moment.

    Sequence:
        seq(type A), seq(type A), int > 0, int > 0 /, bool/ -> float
    
    Args:
        DataX: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
            - the first data set sequence
        DataY: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
            - the second data set sequence
        NX: int > 0; the power of the moment for X data set
        NY: int > 0; the power of the moment for Y data set
        IsCentral: (keyword) bool; flag if the central moment should be
            calculated, defaults to True
    
    Returns:
        float: the calculated moment

    Raises:
        UT_TypeError: any of the passed data sets is not a sequence, OR any of
            their elements is not a real number (int or float, 'is a' check) or
            an instance of 'real life measurement' class ('has a' check), OR any
            of the passed powers are not integers
        UT_ValueError: any of the passed sequence is empty, OR their lengths are
            not equal, OR any of the passed powers is not positive
    
    Version 1.0.0.0
    """
    if not isinstance(NX, int):
        objError = UT_TypeError(NX, int, SkipFrames = 1)
        strMessage = objError.args[0]
        strNewMessage = '{} - moment power X data set'.format(strMessage)
        objError.args = (strNewMessage, )
        raise objError
    elif NX < 1:
        raise UT_ValueError(NX, '> 0 - moment power X data set', SkipFrames = 1)
    if not isinstance(NY, int):
        objError = UT_TypeError(NY, int, SkipFrames = 1)
        strMessage = objError.args[0]
        strNewMessage = '{} - moment power Y data set'.format(strMessage)
        objError.args = (strNewMessage, )
        raise objError
    elif NY < 1:
        raise UT_ValueError(NY, '> 0 - moment power Y data set', SkipFrames = 1)
    lstDataX, lstDataY = _ExtractMeans2(DataX, DataY)
    iN = len(lstDataX)
    if IsCentral:
        fSum = math.fsum(lstDataX)
        fMeanX = fSum / iN
        fSum = math.fsum(lstDataY)
        fMeanY = fSum / iN
    else:
        fMeanX = 0.0
        fMeanY = 0.0
    fSum = math.fsum((((Item - fMeanX)**NX)*((lstDataY[iId] - fMeanY)**NY))
                                        for iId, Item in enumerate(lstDataX))
    fResult = fSum / iN
    return fResult

def GetPearsonR(DataX: TGenericSequence,
                    DataY: TGenericSequence) -> float:
    """
    Calculates the Pearson's coefficient of correlation r of the values in two
    data sets (without the Bessel correction, i.e. assuming the sequence is the
    full population), which can be a mix of int or float (real) numbers and
    instances of the 'real life measurements' class, i.e. the 2-tuples of the
    'mean' value of a measurement and the associated measurement uncertainty.

    Sequence:
        seq(type A), seq(type A), int > 0, int > 0 /, bool/ -> float
    
    Args:
        DataX: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
            - the first data set sequence
        DataY: seq(type A); the input data sequence, expected a mixture of real
            numbers and 'real life measurements' (mean + associated uncertainty)
            - the second data set sequence
    
    Returns:
        float: the calculated correlation coefficient

    Raises:
        UT_TypeError: any of the passed data sets is not a sequence, OR any of
            their elements is not a real number (int or float, 'is a' check) or
            an instance of 'real life measurement' class ('has a' check)
        UT_ValueError: any of the passed sequence is empty, OR their lengths are
            not equal
    
    Version 1.0.0.0
    """
    lstDataX, lstDataY = _ExtractMeans2(DataX, DataY)
    iN = len(lstDataX)
    fSum = math.fsum(lstDataX)
    fMeanX = fSum / iN
    fSum = math.fsum(lstDataY)
    fMeanY = fSum / iN
    CoVar = math.fsum((Item - fMeanX)*(lstDataY[iId] - fMeanY)
                                        for iId, Item in enumerate(lstDataX))
    VarX = math.fsum((Item - fMeanX)**2 for Item in lstDataX)
    VarY = math.fsum((Item - fMeanY)**2 for Item in lstDataY)
    fResult = CoVar / math.sqrt(VarX * VarY)
    return fResult
