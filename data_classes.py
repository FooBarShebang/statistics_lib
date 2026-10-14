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

__version__= '1.1.0.0'
__date__ = '14-10-2026'
__status__ = 'Production'

#imports

#+ standard library

import sys
import os
import math
import operator

from collections.abc import Sequence

from typing import Optional, Union, Any, Tuple, Generator, Self, Callable

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

#globals

#+ data types

TReal = Union[int, float]

TRealTuple = Tuple[TReal, ...]

TNumber = Union[TReal, bf.MeasuredValue]

TNumberSequence = Sequence[TNumber]

TAllowedOperand = Union[TNumber, TNumberSequence]

#helper functions

def _CheckIfNumber(Other: Any) -> bool:
    """
    Helper function to check if a value is an integer, floating point or value
    with uncertainty.

    Signature:
        type A -> bool

    Version 1.0.0.0
    """
    return True if isinstance(Other, (int, float, bf.MeasuredValue)) else False

def _CheckIfNumberSequence(Other: Any) -> bool:
    """
    Helper function to check if a value is a sequence of integers, floating
    point numbers or values with uncertainty.
    
    Signature:
        type A -> bool
    
    Version 1.0.0.0
    """
    if isinstance(Other, Sequence):
        Result = True if all(map(_CheckIfNumber, Other)) else False
    else:
        Result = False
    return Result

#classes

class Statistics1D:
    """
    Data storage class encapsulating 1D data set and ensuring its immutability.
    The statistical properties are calculated 'on demand', cached and interfaced
    via read-only properties (attributes).

    Supports len(), iter() and getitem(Index: int) protocols, thus can be used
    in 'for loop' and enumerate(). Also supports basic scalar-array and per
    element array-array arithmetics.

    Must be instantiated with one sequence of (a mix of) real numbers or
    instances of classes implementing 'measurements with uncertainty' of the
    same length.

    Properties:
        Name: str; arbitrary identifier of the data set
        Values: (read-only) tuple(int OR float); the stored 'mean / most
            probable' values of the data set
        Errors: (read-only) tuple(int >= 0 OR float >= 0); the stored 'errors /
            uncertainties' values of the measurements in the data set
        Sorted: (read-only) tuple(int OR float); the stored 'mean / most
            probable' values of the data set, sorted in the ascending order
        N: (read-only) int > 0; the length of the data set (number of points)
        Mean: (read-only) int OR float; the arithmetic mean of the stored data
        Median: (read-only) int OR float; the median value of the stored data
        Q1: (read-only) int OR float; the first quartile of the stored data
        Q3: (read-only) int OR float; the third quartile of the stored data
        Min: (read-only) int OR float; the minimum value within the stored data
        Max: (read-only) int OR float; the maximum value within the stored data
        Var: (read-only) int >= 0 OR float >= 0; the (population) variance of
            the data set
        Sigma: (read-only) int >= 0 OR float >= 0; the (population) standard
            deviation of the data set
        SE: (read-only) int >= 0 OR float >= 0; the (population) standard
            error of the mean of the data set
        FullVar: (read-only) int >= 0 OR float >= 0; the (population) full
            variance of the data set, including the contribution of the
            measurements uncertainties
        FullSigma: (read-only) int >= 0 OR float >= 0; the (population) full
            standard deviation of the data set, including the contribution of
            the measurements uncertainties
        FullSE: (read-only) int >= 0 OR float >= 0; the (population) full
            standard error of the mean of the data set, including the
            contribution of the measurements uncertainties
        Skew: (read-only) int OR float; the (population) skewness of the stored
            data
        Kurt: (read-only) int OR float; the (population) excess kurtosis of the
            stored data
        Summary: (read-only) str; the summary of the statistical properties of
            the data set
    
    Methods:
        getQuantile(k, m)
            0<= int k <= int m -> int OR float
        getHistogram(*, NBins = None, BinSize = None)
            /*, int > 0 OR None, int > 0 OR float > 0 OR None/
                -> tuple(tuple(int OR float, int >= 0))
        generateZ_Score()
            None -> Statistics1D
    
    Version 1.1.0.0
    """

    #'private' helper methods

    def _checkOther(self, Other: Any) -> None:
        """
        Helper method to check if the passed value is a generic number or a
        sequence of generic numbers of the same length as the stored data.

        Signature:
            type A -> None
        
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument does
                not meet the expected data type restriction
        
        Version 1.0.0.0
        """
        if _CheckIfNumberSequence(Other) or isinstance(Other, self.__class__):
            if len(Other) != self.N:
                Error = bf.UT_TypeError(Other, (Sequence, self.__class__),
                                                                SkipFrames = 2)
                Message = f'of length {self.N} - operand {Other}'
                Error.appendMessage(Message)
                raise Error
        elif not _CheckIfNumber(Other):
            Error = bf.UT_TypeError(Other, (Sequence, self.__class__, int,
                                    float, bf.MeasuredValue), SkipFrames = 2)
            Message = f'- operand {Other}'
            Error.appendMessage(Message)
            raise Error

    def _applyOperator(self, Other: TAllowedOperand,
                            Operator: Callable[[TNumber, TNumber], TNumber], *,
                                                Reversed: bool = False) -> Self:
        """
        Helper method to implement array-scalar and array-array arithmethics.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue),
                func(type A, type B -> type C)/, *, bool/ -> Statistics1D
        """
        IsScalar = _CheckIfNumber(Other)
        Temp = list()
        for Index, Item in enumerate(self):
            Value = Other[Index] if not IsScalar else Other
            if not Reversed:
                Result = Operator(Item, Value)
            else:
                Result = Operator(Value, Item)
            Temp.append(Result)
        return self.__class__(Temp)

    #special methods

    def __init__(self, Data: bf.TGenericSequence) -> None:
        """
        Initialization method. Perfroms the input data sanity check, extaction
        of the 'means' and uncertainties of the measurements, and encapsulation
        of the data.

        Signature:
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue) -> None

        Args:
            Data: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue);
                generic sequence of the measurements data to be stored

        Raises:
            UT_TypeError: argument is not a sequence of real numbers or
                measurements with uncertainty
            UT_ValueError: passed sequence is empty
        
        Version 1.0.0.1
        """
        Temp = bf._ExtractMeans(Data, SkipFrames = 2)
        self._Data = dict()
        self._Data['Values'] = tuple(Temp)
        self._Data['Errors'] = tuple(bf._ExtractErrors(Data, DoCheck = False))
        self._Data['Sorted'] =  None
        self._Properties = {Key : None for Key in ['N', 'Mean', 'Median', 'Q1',
                                    'Q3', 'Min', 'Max', 'Var', 'Sigma', 'SE',
                                        'Skew', 'Kurt', 'FullVar', 'FullSigma',
                                                            'FullSE', 'Name']}
        self._SupportsMeasuredValue = True #walkaround to fix conflict with
        # MeasuredValue arithmetics implementation
    
    def __str__(self) -> str:
        """
        'Magic' method returning the string representaton of the instance as
        the string '{class name}({value of Name property})'.
        
        Signature:
            None -> str
        
        Version 1.0.1.0
        """
        return f'{self.__class__.__name__}({self.Name})'
    
    def __repr__(self) -> str:
        """
        'Magic' method returning the string representaton of the instance as
        the string '<{class name}({value of Name property}) at {id}>'.
        
        Signature:
            None -> str
        
        Version 1.0.1.0
        """
        IdHex = hex(id(self))
        return f'<{self.__class__.__name__}({self.Name}) at {IdHex}>'

    def __len__(self) -> int:
        """
        'Magic' method returning the stored data sample size, basically the
        same as the getter property self.N.

        Signature:
            None -> int >= 0
        
        Version 1.0.0.0
        """
        return self.N

    def __iter__(self) -> Generator[TNumber, None, None]:
        """
        'Magic' method implementing looping through the stored data points as
        in 'for Item in Sequence'.

        Signature:
            None -> gen(None -> int OR float OR MeasuredValue)
        
        Returns:
            gen(None -> int OR float OR MeasuredValue); a generator function
                returning a real value OR an instance of MeasuredValue class
                for each consequence call
        
        Version 1.0.0.0
        """
        for Index, Value in enumerate(self._Data['Values']):
            Error = self._Data["Errors"][Index]
            Item = bf.MeasuredValue(Value, Error) if Error else Value
            yield Item

    def __getitem__(self, Index: int) -> TNumber:
        """
        'Magic' method to retrieve a stored data point by its positional index.

        Signature:
            int -> int OR float OR MeasuredValue
        
        Version 1.0.0.0
        """
        Value = self._Data['Values'][Index]
        Error = self._Data['Errors'][Index]
        return bf.MeasuredValue(Value, Error) if Error else Value

    def __add__(self, Other: Union[TNumberSequence, Self]) -> Self:
        """
        'Magic' method implementing right addition of a scalar or an array to
        the stored data.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue)
                -> Statistics1D
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument does
                not meet the expected data type restriction
        
        Version 1.0.0.0
        """
        self._checkOther(Other)
        return self._applyOperator(Other, operator.add)

    def __radd__(self, Other: Union[TNumberSequence, Self]) -> Self:
        """
        'Magic' method implementing left addition of a scalar or an array to
        the stored data.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue)
                -> Statistics1D
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument does
                not meet the expected data type restriction
        
        Version 1.0.0.0
        """
        self._checkOther(Other)
        return self._applyOperator(Other, operator.add, Reversed = True)

    def __sub__(self, Other: Union[TNumberSequence, Self]) -> Self:
        """
        'Magic' method implementing right subtraction of a scalar or an array to
        the stored data.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue)
                -> Statistics1D
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument does
                not meet the expected data type restriction
        
        Version 1.0.0.0
        """
        self._checkOther(Other)
        return self._applyOperator(Other, operator.sub)

    def __rsub__(self, Other: Union[TNumberSequence, Self]) -> Self:
        """
        'Magic' method implementing left addition of a scalar or an array to
        the stored data.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue)
                -> Statistics1D
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument does
                not meet the expected data type restriction
        
        Version 1.0.0.0
        """
        self._checkOther(Other)
        return self._applyOperator(Other, operator.sub, Reversed = True)

    def __mul__(self, Other: Union[TNumberSequence, Self]) -> Self:
        """
        'Magic' method implementing right multiplication by a scalar or an array
        of the stored data.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue)
                -> Statistics1D
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument does
                not meet the expected data type restriction
        
        Version 1.0.0.0
        """
        self._checkOther(Other)
        return self._applyOperator(Other, operator.mul)

    def __rmul__(self, Other: Union[TNumberSequence, Self]) -> Self:
        """
        'Magic' method implementing left multiplication by a scalar or an array
        of the stored data.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue)
                -> Statistics1D
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument does
                not meet the expected data type restriction
        
        Version 1.0.0.0
        """
        self._checkOther(Other)
        return self._applyOperator(Other, operator.mul, Reversed = True)

    def __truediv__(self, Other: Union[TNumberSequence, Self]) -> Self:
        """
        'Magic' method implementing division of the stored data by a scalar or
        an array.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue)
                -> Statistics1D
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument does
                not meet the expected data type restriction
        
        Version 1.0.0.0
        """
        self._checkOther(Other)
        return self._applyOperator(Other, operator.truediv)

    def __rtruediv__(self, Other: Union[TNumberSequence, Self]) -> Self:
        """
        'Magic' method implementing division of a scalar or an array by the
        stored data.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue)
                -> Statistics1D
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument does
                not meet the expected data type restriction
        
        Version 1.0.0.0
        """
        self._checkOther(Other)
        return self._applyOperator(Other, operator.truediv, Reversed = True)

    def __pow__(self, Other: int) -> Self:
        """
        'Magic' method implementing raising of the stored data to an integer
        power.

        Signature:
            Statistics1D OR int OR float OR seq(int OR float OR MeasuredValue)
                -> Statistics1D
        Raises:
            introspection_lib.base_exceptions.UT_TypeError: the argument is not
                an integer number
        
        Version 1.0.0.0
        """
        if not isinstance(Other, int):
            Error = bf.UT_TypeError(Other, int, SkipFrames = 1)
            Message = f'- operand {Other}'
            Error.appendMessage(Message)
            raise Error
        return self._applyOperator(Other, operator.pow)

    #public API

    #+ properties

    @property
    def Name(self) -> Union[str, None]:
        """
        Getter property to access the string identificator assigned to the data
        set. The defualt (initial) value is None.

        Signature:
            None -> str OR None
        
        Version 1.0.0.0
        """
        return self._Properties['Name']
    
    @Name.setter
    def Name(self, Value: Any) -> None:
        """
        Setter property for the string identificator of the data set. Any passed
        value is converted into a string.

        Singature:
            type A -> None
        
        Version 1.0.0.0
        """
        self._Properties['Name'] = str(Value)
    
    @property
    def Values(self) -> TRealTuple:
        """
        Read-only property to access the stored 'mean / most probable' values
        of the measurements sequence data set as an immutable sequence.

        Signature:
            None -> tuple(int OR float)
        
        Version 1.0.0.0
        """
        return self._Data['Values']
    
    @property
    def Errors(self) -> TRealTuple:
        """
        Read-only property to access the stored 'uncertainties of measurements'
        values of the measurements sequence data set as an immutable sequence.

        Signature:
            None -> tuple(int >= 0 OR float >= 0)
        
        Version 1.0.0.0
        """
        return self._Data['Errors']
    
    @property
    def Sorted(self) -> TRealTuple:
        """
        Read-only property to access the stored 'mean / most probable' values of
        the measurements sequence data set sorted in the ascending order as an
        immutable sequence.

        Signature:
            None -> tuple(int >= 0 OR float >= 0)
        
        Version 1.0.0.0
        """
        if self._Data['Sorted'] is None:
            self._Data['Sorted'] = tuple(sorted(self.Values))
        return self._Data['Sorted']

    @property
    def N(self) -> int:
        """
        Read-only property returning the length of the stored data set.

        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        if self._Properties['N'] is None:
            self._Properties['N'] = len(self.Values)
        return self._Properties['N']
    
    @property
    def Mean(self) -> bf.TReal:
        """
        Read-only property returning the arithmetic mean of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Mean'] is None:
            self._Properties['Mean'] = bf.GetMean(self.Values, DoCheck = False)
        return self._Properties['Mean']
    
    @property
    def Min(self) -> bf.TReal:
        """
        Read-only property returning the minimum value of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Min'] is None:
            self._Properties['Min'] = min(self.Values)
        return self._Properties['Min']
    
    @property
    def Max(self) -> bf.TReal:
        """
        Read-only property returning the maximum value of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Max'] is None:
            self._Properties['Max'] = max(self.Values)
        return self._Properties['Max']
    
    @property
    def Median(self) -> bf.TReal:
        """
        Read-only property returning the median value of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Median'] is None:
            self._Properties['Median'] = of.GetMedian(self.Sorted,
                                                                DoCheck = False)
        return self._Properties['Median']
    
    @property
    def Q1(self) -> bf.TReal:
        """
        Read-only property returning the first quartile of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Q1'] is None:
            self._Properties['Q1'] = of.GetFirstQuartile(self.Sorted,
                                                                DoCheck = False)
        return self._Properties['Q1']
    
    @property
    def Q3(self) -> bf.TReal:
        """
        Read-only property returning the third quartile of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Q3'] is None:
            self._Properties['Q3'] = of.GetThirdQuartile(self.Sorted,
                                                                DoCheck = False)
        return self._Properties['Q3']
    
    @property
    def Var(self) -> bf.TReal:
        """
        Read-only property returning the variance of the stored data set.

        Signature:
            None -> int >= 0 OR float >= 0
        
        Version 1.0.0.0
        """
        if self._Properties['Var'] is None:
            self._Properties['Var'] = bf.GetVarianceP(self.Values,
                                                                DoCheck = False)
        return self._Properties['Var']
    
    @property
    def Sigma(self) -> bf.TReal:
        """
        Read-only property returning the standard deviation of the stored data
        set.

        Signature:
            None -> int >= 0 OR float >= 0
        
        Version 1.0.0.0
        """
        if self._Properties['Sigma'] is None:
            self._Properties['Sigma'] = math.sqrt(self.Var)
        return self._Properties['Sigma']
    
    @property
    def SE(self) -> bf.TReal:
        """
        Read-only property returning the standard error of the mean of the
        stored data set.

        Signature:
            None -> int >= 0 OR float >= 0
        
        Version 1.0.0.0
        """
        if self._Properties['SE'] is None:
            self._Properties['SE'] = math.sqrt(self.Var / self.N)
        return self._Properties['SE']
    
    @property
    def FullVar(self) -> bf.TReal:
        """
        Read-only property returning the full variance of the stored data set,
        including the contribution of the measurement uncertainties.

        Signature:
            None -> int >= 0 OR float >= 0
        
        Version 1.0.0.0
        """
        if self._Properties['FullVar'] is None:
            MSSE = sum(pow(Item, 2) for Item in self.Errors) / self.N
            self._Properties['FullVar']= self.Var + MSSE
        return self._Properties['FullVar']
    
    @property
    def FullSigma(self) -> bf.TReal:
        """
        Read-only property returning the full standard deviation of the stored
        data set, including the contribution of the measurement uncertainties.

        Signature:
            None -> int >= 0 OR float >= 0
        
        Version 1.0.0.0
        """
        if self._Properties['FullSigma'] is None:
            self._Properties['FullSigma'] = math.sqrt(self.FullVar)
        return self._Properties['FullSigma']
    
    @property
    def FullSE(self) -> bf.TReal:
        """
        Read-only property returning the full standard error of the mean of the
        stored data set, including the contribution of the measurement
        uncertainties.

        Signature:
            None -> int >= 0 OR float >= 0
        
        Version 1.0.0.0
        """
        if self._Properties['FullSE'] is None:
            self._Properties['FullSE'] = math.sqrt(self.FullVar / self.N)
        return self._Properties['FullSE']
    
    @property
    def Skew(self) -> bf.TReal:
        """
        Read-only property returning the skewness of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Skew'] is None:
            self._Properties['Skew'] = bf.GetSkewnessP(self.Values,
                                                                DoCheck = False)
        return self._Properties['Skew']
    
    @property
    def Kurt(self) -> bf.TReal:
        """
        Read-only property returning the excess kurtosis of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Kurt'] is None:
            self._Properties['Kurt'] = bf.GetKurtosisP(self.Values,
                                                                DoCheck = False)
        return self._Properties['Kurt']
    
    @property
    def Summary(self) -> str:
        """
        Read-only property to generate human-reaadble, multi-line, TSV format
        tabulated report listing all relevant statistical properties of the
        stored data set (as entire population).

        Signature:
            None -> str
        
        Version 1.0.1.0
        """
        Separator = '----------------------------------------------------------'
        if self.Name is None:
            Result = Separator
        else:
            Result = f'{Separator}\nName:\t{self.Name}'
        Result = '\n'.join([Result,
                        '\n'.join(f'{Key}:\t{getattr(self, Key)}' for Key in
                        ['N', 'Mean', 'Median', 'Q1', 'Q3', 'Min', 'Max', 'Var',
                                        'FullVar', 'Skew', 'Kurt']), Separator])
        return Result
    
    #+ methods

    def getQuantile(self, k: int, m: int) -> bf.TReal:
        """
        Calculates the k-th of m-quantile value of the stored data set. The
        computation speed is O(N*log(N)), if the sorted copy of the stored data
        haven't been accessed yet, otherwise - O(1), including consequtive
        calculation of different quantiles. The proper relations are:
            * 0<= k <=m
            * m > 0

        Signature:
            int >= 0, int > 0 -> int OR float
        
        Args:
            k: int >= 0; the quantile index, between 0 and m inclusively
            m: int > 0; the total number of quantiles
        
        Raises:
            UT_TypeError: quantile index is not an integer, OR the total
                number of quantiles is not an integer
            UT_ValueError: the total number of quantilies is negative integer or
                zero, OR the quantile index is negative integer or integer
                greater than the total number of quantiles, OR the stored
                sequence is of length 1

        Version 1.0.0.0
        """
        Result = of.GetQuantile(self.Sorted, k, m, SkipFrames = 2,
                                                                DoCheck = False)
        return Result
    
    def getHistogram(self, *, NBins: Optional[int] = None,
                                BinSize: Optional[bf.TReal]= None) -> Tuple[
                                                    Tuple[bf.TReal, int], ...]:
        """
        Calculates the histogram of number of apperance of 'mean' values
        belonging to the respective bins for the data sample. Either total
        number of bins OR the desired bin width can be specified, where number
        of bins takes the precedence. When neither value is defined, the default
        number of bins is 20. Computation speed is always O(N).

        Signature:
            /*, int > 0 OR None, int > 0 OR float > 0 OR None/
                -> tuple(tuple(int OR float, int >= 0))
    
        Args:
            NBins: (keyword) int > 0 OR None; the desired number of bins
            BinSize: (keyword) int > 0 OR float > 0 OR None; the desired bin
                size, ignored is NBins is passed as not None value
    
        Returns:
            tuple(tuple(int OR float, int >= 0)): the calculated histogram as
                tuple of pairs (nested tuples) of the central value and the
                associated frequency
    
        Raises:
            UT_TypeError: any keyword argument is of improper type
            UT_ValueError: any keyword argument is of the proper type but
                unacceptable value

        Version 1.0.0.1
        """
        Temp = of.GetHistogram(self.Values, NBins = NBins, BinSize= BinSize,
                                                SkipFrames = 2, DoCheck = False)
        Result = tuple((Key, Item) for Key, Item in Temp.items())
        return Result

    def generateZ_Score(self) -> Self:
        """
        Generates a z-score distribution based on the currently stored data
        preserving the data points order; i.e. x[i] -> z[i]= (x[i] - <x>) / sig.

        Note that even for all real number data (all errors are zeros) the mean
        is calculated already with uncertainty, i.e. as MeasuredValue class
        instance, thus all z[i] generated as MeasuredValue (with uncertainty)
        class instances. Furthermore, SE of <x> and Sigma are calculated as
        FullSE and FullSigma to account for the uncertainties (if present) of
        the original distribution's values.

        Signature:
            None -> Statistics1D

        Returns:
            Statisitics1D: a new instance of the class, storing the z-score
                distribution

        Version 1.0.0.0
        """
        Mean = self.Mean
        SE = self.FullSE
        Mean = bf.MeasuredValue(Mean, SE)
        Sigma = self.FullSigma
        NewData = list((Value - Mean) / Sigma for Value in self)
        return self.__class__(NewData)

    def generateZ_ScorePure(self) -> Self:
        """
        Generates a z-score distribution based on the currently stored data
        preserving the data points order; i.e. x[i] -> z[i]= (x[i] - <x>) / sig.

        This is a 'pure' version of z-score generator, which ignores the
        uncertainties of the stored values. Thus, Var(z) = 1 is guaranteed, and
        all generated z-values have no uncertainties.

        Signature:
            None -> Statistics1D

        Returns:
            Statisitics1D: a new instance of the class, storing the z-score
                distribution

        Version 1.0.0.0
        """
        Mean = self.Mean
        Sigma = self.Sigma
        NewData = list((Value - Mean) / Sigma for Value in self.Values)
        return self.__class__(NewData)

class Statistics2D:
    """
    Data storage class encapsulating 2D data set and ensuring its immutability.
    The statistical properties are calculated 'on demand', cached and interfaced
    via read-only properties (attributes).

    Supports len(), iter() and getitem(Index: int) protocols, thus can be used
    in 'for loop' and enumerate().

    Must be instantiated with two sequences of (a mix of) real numbers or
    instances of classes implementing 'measurements with uncertainty' of the
    same length.

    Properties:
        Name: str; arbitrary identifier of the data set
        X: (read-only) Statistics1D; the stored X data sub-set
        Y: (read-only) Statistics1D; the stored Y data sub-set
        N: (read-only) int > 0; the length of the data set (number of points)
        Cov: (read-only) int OR float; covariance of the data set
        Pearson: (read-only) int OR float; Pearson's correlation coefficient r
            of the data set
        Spearman: (read-only) int OR float; Spearman rank correlation
            coefficient rho of the data set
        Kendall: (read-only) int OR float; Kendall rank correlation coefficient
            tau-b of the data set
        Summary: (read-only) str; the summary of the statistical properties of
            the data set
    
    Version 1.1.1.0
    """
    
    #special methods

    def __init__(self, DataX: bf.TGenericSequence,
                                            DataY: bf.TGenericSequence) -> None:
        """
        Initialization method. Perfroms the input data sanity check, extaction
        of the 'means' and uncertainties of the measurements, and encapsulation
        of the data.

        Signature:
            seq(int OR float OR phyqus_lib.base_classes.MeasuredValue),
                seq(int OR float OR phyqus_lib.base_classes.MeasuredValue)
                    -> None

        Args:
            DataX: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue);
                generic sequence of the measurements data to be stored as X
                sub-set
            DataY: seq(int OR float OR phyqus_lib.base_classes.MeasuredValue);
                generic sequence of the measurements data to be stored as X
                sub-set
            
        Raises:
            UT_TypeError: any of the arguments is not a sequence of real numbers
                or measurements with uncertainty
            UT_ValueError: any of the passed sequences is empty, or they have
                unequal length
        
        Version 1.0.1.0
        """
        self._Data = dict()
        try:
            self._Data['X'] = Statistics1D(DataX)
        except (UT_TypeError, UT_ValueError) as err1:
            Message = f'{err1.getMessage()} - X data'
            if isinstance(err1, UT_TypeError):
                err = UT_TypeError(1, int, SkipFrames = 1)
            else:
                err = UT_ValueError(1, 'whatever', SkipFrames = 1)
            err.setMessage(Message)
            raise err from None
        try:
            self._Data['Y'] = Statistics1D(DataY)
        except (UT_TypeError, UT_ValueError) as err1:
            Message = f'{err1.getMessage()} - Y data'
            if isinstance(err1, UT_TypeError):
                err = UT_TypeError(1, int, SkipFrames = 1)
            else:
                err = UT_ValueError(1, 'whatever', SkipFrames = 1)
            err.setMessage(Message)
            raise err from None
        LengthX = self.X.N
        LengthY = self.Y.N
        if LengthX != LengthY:
            raise UT_ValueError(LengthX, f'== {LengthY} - sequences length',
                                                                SkipFrames = 1)
        self._Properties = {Key : None for Key in ['Cov', 'Pearson', 'Spearman',
                                                            'Kendall', 'Name']}
    
    def __str__(self) -> str:
        """
        'Magic' method returning the string representaton of the instance as
        the string '{class name}({value of Name property})'.
        
        Signature:
            None -> str
        
        Version 1.0.1.0
        """
        return f'{self.__class__.__name__}({self.Name})'
    
    def __repr__(self) -> str:
        """
        'Magic' method returning the string representaton of the instance as
        the string '<{class name}({value of Name property}) at {id}>'.
        
        Signature:
            None -> str
        
        Version 1.0.1.0
        """
        IdHex = hex(id(self))
        return f'<{self.__class__.__name__}({self.Name}) at {IdHex}>'

    def __len__(self) -> int:
        """
        'Magic' method returning the stored data sample size, basically the
        same as the getter property self.N.

        Signature:
            None -> int >= 0
        
        Version 1.0.0.0
        """
        return self.N

    def __iter__(self) -> Generator[tuple[TNumber, TNumber], None, None]:
        """
        'Magic' method implementing looping through the stored data points as
        in 'for Item in Sequence'.

        Signature:
            None -> gen(None -> tuple(int OR float OR MeasuredValue,
                                                int OR float OR MeasuredValue))
        
        Returns:
            gen(None -> tuple(int OR float OR MeasuredValue,
                int OR float OR MeasuredValue)); a generator function
                returning a rtuple of values, corresponding to the stored X-
                and Y- data points with the same indexes.
        
        Version 1.0.0.0
        """
        for Index, Value in enumerate(self._Data['X']):
            yield (Value, self._Data['Y'][Index])

    def __getitem__(self, Index: int) -> tuple[TNumber, TNumber]:
        """
        'Magic' method to retrieve a stored data point by its positional index.

        Signature:
            int -> tuple(int OR float OR MeasuredValue, 
                int OR float OR MeasuredValue)
        
        Version 1.0.0.0
        """
        return (self._Data['X'][Index], self._Data['Y'][Index])
    
    #public API

    #+ properties

    @property
    def Name(self) -> Union[str, None]:
        """
        Getter property to access the string identificator assigned to the data
        set. The defualt (initial) value is None.

        Signature:
            None -> str OR None
        
        Version 1.0.0.0
        """
        return self._Properties['Name']
    
    @Name.setter
    def Name(self, Value: Any) -> None:
        """
        Setter property for the string identificator of the data set. Any passed
        value is converted into a string.

        Singature:
            type A -> None
        
        Version 1.0.0.0
        """
        self._Properties['Name'] = str(Value)

    @property
    def X(self) -> Statistics1D:
        """
        Read-only property returning the stored X data set

        Signature:
            None -> Statistics1D
        
        Version 1.0.0.0
        """
        return self._Data['X']
    
    @property
    def Y(self) -> Statistics1D:
        """
        Read-only property returning the stored Y data set

        Signature:
            None -> Statistics1D
        
        Version 1.0.0.0
        """
        return self._Data['Y']

    @property
    def N(self) -> int:
        """
        Read-only property returning the length of the stored data set.

        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        return self.X.N
    
    @property
    def Cov(self) -> int:
        """
        Read-only property returning the covariance of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Cov'] is None:
            self._Properties['Cov'] = bf.GetCovariance(self.X.Values,
                                                self.Y.Values, DoCheck = False)
        return self._Properties['Cov']
    
    @property
    def Pearson(self) -> int:
        """
        Read-only property returning the Pearson's coefficient of correlation r
        of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Pearson'] is None:
            self._Properties['Pearson'] = bf.GetPearsonR(self.X.Values,
                                                self.Y.Values, DoCheck = False)
        return self._Properties['Pearson']
    
    @property
    def Spearman(self) -> int:
        """
        Read-only property returning the Spearman coefficient of rank
        correlation rho of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Spearman'] is None:
            self._Properties['Spearman'] = of.GetSpearman(self.X.Values,
                                                self.Y.Values, DoCheck = False)
        return self._Properties['Spearman']
    
    @property
    def Kendall(self) -> int:
        """
        Read-only property returning the Kendall coefficient of rank correlation
        tau-b of the stored data set.

        Signature:
            None -> int OR float
        
        Version 1.0.0.0
        """
        if self._Properties['Kendall'] is None:
            self._Properties['Kendall'] = of.GetKendall(self.X.Values,
                                                self.Y.Values, DoCheck = False)
        return self._Properties['Kendall']
    
    @property
    def Summary(self) -> str:
        """
        Read-only property to generate human-reaadble, multi-line, TSV format
        tabulated report listing all relevant statistical properties of the
        stored data set (as entire population).

        Signature:
            None -> str
        
        Version 1.0.1.0
        """
        Separator = '=========================================================='
        if self.Name is None:
            Result = Separator
        else:
            Result = '{}\nName:\t{}'.format(Separator, self.Name)
        Result = '\n'.join([Result,
                '\n'.join(f'{Key}:\t{getattr(self, Key)}' for Key in
                        ['Cov', 'Pearson', 'Spearman', 'Kendall',]),
                            'X data sub-set', self.X.Summary,
                                'Y data sub-set', self.Y.Summary, Separator])
        return Result