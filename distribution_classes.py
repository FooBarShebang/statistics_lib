#usr/bin/python3
"""
Module statistics_lib.distribution_classes

Classes:
    ContinuousDistributionABC
    DiscreteDistributionABC
    Z_Distribution
    Gaussian
"""

__version__= '1.0.0.0'
__date__ = '21-03-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import math
import abc

from random import random as base_random

from typing import ClassVar, Tuple

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

import statistics_lib.special_functions as sf

#+ classes

class ContinuousDistributionABC(abc.ABC):
    """
    Abstact base class for the continuous distributions. The specific
    sub-classes must implement all methods and properties, which are abstract.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) int OR float
        Max: (read-only) int OR float
        Mean: (read-only) int OR float
        Median: (read-only) int OR float
        Q1: (read-only) int OR float
        Q2: (read-only) int OR float
        Var: (read-only) int OR float
        Sigma: (read-only) int OR float
        Skew: (read-only) int OR float
        Kurt: (read-only) int OR float
    
    Methods:
        pdf(x)
            int OR float -> float >= 0
        cdf(x)
            int OR float -> 0 < float < 1 OR 0 <= int <= 1
        qf()
            0 < float < 1 -> int OR float
        getQuantile(k, m)
            int > 0, int > 0 -> float OR int
        getHistogram()
            int OR float, int OR float, int > 1
                -> tuple(tuple(int OR float, float >= 0))
        random()
            None -> int OR float
    
    Version 1.0.0.0
    """
    
    #class 'private' fields
    
    _Min: ClassVar[sf.TReal] = - math.inf
    
    _Max: ClassVar[sf.TReal] = math.inf
    
    # 'private' instance methods
    
    @abc.abstractmethod
    def _pdf(self, x: sf.TReal) -> float:
        """
        The placeholder for the actual implementation of the PDF / PMF function,
        which must be properly implemented in each sub-class using the following
        signature:
            int OR float -> float >= 0
        """
        pass
    
    @abc.abstractmethod
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The placeholder for the actual implementation of the CDF function,
        which must be properly implemented in each sub-class using the following
        signature:
            int OR float -> 0 < float < 1 OR 0 <= int <= 1
        """
        pass
    
    @abc.abstractmethod
    def _qf(self, x: float) -> sf.TReal:
        """
        The placeholder for the actual implementation of the ICDF / QF function,
        which must be properly implemented in each sub-class using the following
        signature:
           0 < float < 1 -> int OR float
        """
        pass
    
    #+ special methods
    
    def __str__(self) -> str:
        """
        'Magic' method returning the string representaton of the instance as
        the string containing the name of the distribution and the parameters
        within parenthesis.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return self.Name
    
    def __repr__(self) -> str:
        """
        'Magic' method returning the string representaton of the instance as
        the string '<{name}({parameters}) at {id}>'.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return '<{} at {}>'.format(self.Name, hex(id(self)))
    
    #public properties
    
    @property
    def Name(self) -> str:
        """
        Getter method to access the name and parameters of the distribution.
        
        Signature:
            None -> str
        
        Returns:
            str: string identifier of the distribution in the form
                '{Name}(parameter = value, ...)'
        Version 1.0.0.0
        """
        BaseName = self.__class__.__name__.split('.')[-1]
        Result = '{}('.format(BaseName)
        if hasattr(self, '_Parameters'):
            Result += ', '.join(['{} = {}'.format(Key, Value)
                                    for Key, Value in self._Parameters.items()])
        Result += ')'
        return Result
    
    @property
    def Min(self) -> sf.TReal:
        """
        Getter property for the minimum value of the range of the random
        variable values.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self._Min
    
    @property
    def Max(self) -> sf.TReal:
        """
        Getter property for the maximum value of the range of the random
        variable values.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self._Max
    
    @abc.abstractproperty
    def Mean(self) -> sf.TReal:
        """
        Prototype for the getter property for the arithmetic mean of the
        distribution.
        
        Sub-classes must implement it with a signature:
            None -> float OR int
        """
        pass
    
    @abc.abstractproperty
    def Median(self) -> sf.TReal:
        """
        Prototype for the getter property for the median of the distribution.
        
        Sub-classes must implement it with a signature:
            None -> float OR int
        """
        pass
    
    @abc.abstractproperty
    def Q1(self) -> sf.TReal:
        """
        Prototype for the getter property for the first quartile of the
        distribution.
        
        Sub-classes must implement it with a signature:
            None -> float OR int
        """
        pass
    
    @abc.abstractproperty
    def Q3(self) -> sf.TReal:
        """
        Prototype for the getter property for the third quartile of the
        distribution.
        
        Sub-classes must implement it with a signature:
            None -> float OR int
        """
        pass
    
    @abc.abstractproperty
    def Var(self) -> sf.TReal:
        """
        Prototype for the getter property for the variance of the distribution.
        
        Sub-classes must implement it with a signature:
            None -> float OR int
        """
        pass
    
    @abc.abstractproperty
    def Sigma(self) -> sf.TReal:
        """
        Prototype for the getter property for the standard deviation of the
        distribution.
        
        Sub-classes must implement it with a signature:
            None -> float OR int
        """
        pass
    
    @abc.abstractproperty
    def Skew(self) -> sf.TReal:
        """
        Prototype for the getter property for the skewness of the distribution.
        
        Sub-classes must implement it with a signature:
            None -> float OR int
        """
        pass
    
    @abc.abstractproperty
    def Kurt(self) -> sf.TReal:
        """
        Prototype for the getter property for the excess kurtosis of the
        distribution.
        
        Sub-classes must implement it with a signature:
            None -> float OR int
        """
        pass
    
    #public instance methods
    
    def pdf(self, x: sf.TReal) -> float:
        """
        Calculates the probability density function for the given value x of the
        random variable X, which is the shape of the distribution.
        
        Signature:
            int OR float -> float >= 0
        
        Args:
            x: int OR float; value of the random variable
        
        Raises:
            UT_TypeError: the argument is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(x, (int, float)):
            raise UT_TypeError(x, (int, float), SkipFrames = 1)
        if x < self.Min or x > self.Max:
            Result = 0
        else:
            Result = self._pdf(x)
        return Result
    
    def cdf(self, x: sf.TReal) -> sf.TReal:
        """
        Calculates the cummulative distribution function for the given value x
        of the random variable X, i.e. Pr[X <= x].
        
        Signature:
            int OR float -> 0 < float < 1 OR 0 <= int <= 1
        
        Args:
            x: int OR float; value of the random variable
        
        Raises:
            UT_TypeError: the argument is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(x, (int, float)):
            raise UT_TypeError(x, (int, float), SkipFrames = 1)
        if x <= self.Min:
            Result = 0
        elif x >= self.Max:
            Result = 1
        else:
            Result = self._cdf(x)
        return Result
    
    def qf(self, p: float) -> sf.TReal:
        """
        Calculates the inverse cummulative distribution function, a.k.a.
        quantile function, i.e the value x of the random variable X for which
        the p = Pr[X <= x], where p is the passed probability value.
        
        Signature:
            0 < float < 1 -> int OR float
        
        Args:
            p: 0 < float < 1; the cummulative probility value
        
        Raises:
            UT_TypeError: the argument is not a floating point number
            UT_ValueError: the argument is not in the range (0, 1)
        
        Version 1.0.0.0
        """
        if not isinstance(p, float):
            raise UT_TypeError(p, float, SkipFrames = 1)
        if p <= 0 or p >= 1:
            raise UT_ValueError(p, 'in range (0, 1)', SkipFrames = 1)
        return self._qf(p)
    
    def getQuantile(self, k: int, m: int) -> sf.TReal:
        """
        Calculates the k-th of m-quantile, where 0 < k < m, which is a short-
        hand for qf(k/m).
        
        Signature:
            int > 0, int > 0 -> float OR int
        
        Args:
            k: int > 0; the quantile index
            m: int > 0; the total number of quantiles
        
        Raises:
            UT_TypeError: the argument is not a floating point number
            UT_ValueError: the argument is not in the range (0, 1)
        
        Version 1.0.0.0
        """
        if not isinstance(k, int):
            raise UT_TypeError(k, int, SkipFrames = 1)
        if not isinstance(m, int):
            raise UT_TypeError(m, int, SkipFrames = 1)
        if k < 0:
            raise UT_ValueError(k, '> 0 - quantile index', SkipFrames = 1)
        if m <= k:
            raise UT_ValueError(k, '< {} - index of quantile'.format(m),
                                                                SkipFrames = 1)
        return self._qf(k / m)
    
    def random(self) -> sf.TReal:
        """
        Generates a random value from the distribution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        while True:
            p = base_random()
            if p > 0:
                break
        return self._qf(p)
    
    def getHistogram(self, minb: sf.TReal, maxb: sf.TReal, NBins: int) -> Tuple[
                                                Tuple[sf.TReal, float], ...]:
        """
        Calculates the (partial) histogram of the distribution using the
        specified number of bins of the same width, whith the central values
        of the bins being between the specificed min and max values.
        
        Signature:
            int OR float, int OR float, int > 1
                -> tuple(tuple(int OR float, float >= 0))
        
        Args:
            minb: int OR float; the cental value of the minimal values bin
            maxb: int OR float; the cental value of the maximal values bin
            NBins: int > 1; the number of bins
        
        tuple(tuple(int OR float, float >= 0)): the calculated histogram as
                tuple of pairs (nested tuples) of the central value and the
                associated frequency
        
        Raises:
            UT_TypeError: either min or max argument is not a real number, OR
                number of bins is not an integer
            UT_ValueError: min argument is greater then or equal to max
                argument, OR number of bins is less than 2
        
        Version 1.0.0.0
        """
        if not isinstance(minb, (int, float)):
            raise UT_TypeError(minb, (int, float), SkipFrames = 1)
        if not isinstance(maxb, (int, float)):
            raise UT_TypeError(maxb, (int, float), SkipFrames = 1)
        if not isinstance(NBins, int):
            raise UT_TypeError(NBins, int, SkipFrames = 1)
        if minb >= maxb:
            raise UT_ValueError(minb, '< {} - min and max values'.format(maxb),
                                                                SkipFrames = 1)
        if NBins < 2:
            raise UT_ValueError(NBins, '> 1 - number of bins', SkipFrames=  1)
        S = (maxb - minb) / (NBins - 1)
        Right = minb - 0.5 * S
        RightCDF = self.cdf(Right)
        Result = list()
        for k in range(NBins):
            LeftCDF = RightCDF
            Right = minb + (k + 0.5) * S
            RightCDF = self.cdf(Right)
            Centre = minb + k * S
            Result.append((Centre, RightCDF - LeftCDF))
        return tuple(Result)

class DiscreteDistributionABC(ContinuousDistributionABC):
    """
    Abstact base class for the discrete distributions. The specific sub-classes
    must implement all methods and properties, which are abstract.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) int >= 0
        Max: (read-only) int > 0
        Mean: (read-only) int OR float
        Median: (read-only) int OR float
        Q1: (read-only) int OR float
        Q2: (read-only) int OR float
        Var: (read-only) int OR float
        Sigma: (read-only) int OR float
        Skew: (read-only) int OR float
        Kurt: (read-only) int OR float
    
    Methods:
        pdf(x)
            int OR float -> float >= 0
        cdf(x)
            int OR float -> 0 < float < 1 OR 0 <= int <= 1
        qf()
            0 < float < 1 -> int OR float
        getQuantile(k, m)
            int > 0, int > 0 -> float OR int
        getHistogram()
            int OR float, int OR float, int > 1
                -> tuple(tuple(int OR float, float >= 0))
        random()
            None -> int
    
    Version 1.0.0.0
    """
    
    #class 'private' fields
    
    _Min: ClassVar[int] = 0
    
    _Max: ClassVar[sf.TReal] = math.inf
    
    #public instance methods
    
    def pdf(self, x: sf.TReal) -> float:
        """
        Calculates the probability mass function for the given value x of the
        random variable X, which is Pr[X = x].
        
        Signature:
            int OR float -> float >= 0
        
        Args:
            x: int OR float; value of the random variable
        
        Raises:
            UT_TypeError: the argument is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(x, (int, float)):
            raise UT_TypeError(x, (int, float), SkipFrames = 1)
        if x < self.Min or x > self.Max:
            Result = 0
        elif not isinstance(x, int):
            Result = 0
        else:
            Result = self._pdf(x)
        return Result
    
    def cdf(self, x: sf.TReal) -> sf.TReal:
        """
        Calculates the cummulative distribution function for the given value x
        of the random variable X, i.e. Pr[X <= x].
        
        Signature:
            int OR float -> 0 < float < 1 OR 0 <= int <= 1
        
        Args:
            x: int OR float; value of the random variable
        
        Raises:
            UT_TypeError: the argument is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(x, (int, float)):
            raise UT_TypeError(x, (int, float), SkipFrames = 1)
        if x <= self.Min:
            Result = 0
        elif x >= self.Max:
            Result = 1
        else:
            Result = self._cdf(int(math.floor(x)))
        return Result
    
    def random(self) -> int:
        """
        Generates a random value from the distribution.
        
        Signature:
            None -> int
        
        Version 1.0.0.0
        """
        while True:
            p = base_random()
            if p > 0:
                break
        return int(math.ceil(self._qf(p)))

class Z_Distribution(ContinuousDistributionABC):
    """
    Implementation of the Z-distribution, i.e. standard normal (Gaussian with
    mean = 0 and sigma = 1). Must be instantiated without arguments.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float = - math.inf
        Max: (read-only) float = math.inf
        Mean: (read-only) float = 0
        Median: (read-only) float = 0
        Q1: (read-only) float
        Q2: (read-only) float
        Var: (read-only) float
        Sigma: (read-only) float = 1.0
        Skew: (read-only) float = 0.0
        Kurt: (read-only) float = 0.0
    
    Methods:
        pdf(x)
            int OR float -> float >= 0
        cdf(x)
            int OR float -> 0 < float < 1
        qf()
            0 < float < 1 -> float
        getQuantile(k, m)
            int > 0, int > 0 -> float
        getHistogram()
            int OR float, int OR float, int > 1
                -> tuple(tuple(int OR float, float >= 0))
        random()
            None -> float
    
    Version 1.0.0.0
    """
    
    #special methods
    
    def __init__(self) -> None:
        """
        Initialization. Does nothing.
        
        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        pass
    
    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int OR float -> float >= 0
        
        Version 1.0.0.0
        """
        Sigma = self.Sigma
        z = (x - self.Mean) / Sigma
        Result = math.exp(-0.5 * z * z) / (Sigma * math.sqrt(2 * math.pi))
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        1.0.0.0
        """
        z = (x - self.Mean) / self.Sigma
        Result = 0.5 * (1 + math.erf(z / math.sqrt(2)))
    
    def _qf(self, p: float) -> sf.TReal:
        """
        The actual implementation of the ICDF / QF function.
        
        Signature:
           0 < float < 1 -> int OR float
        
        Version 1.0.0.0
        """
        Result = self.Mean + self.Sigma * math.sqrt(2) * sf.inv_erf(2 * p - 1)
        return Result
    
    #public properties
    
    @property
    def Mean(self) -> float:
        """
        Getter property for the arithmetic mean of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 0.0
    
    @property
    def Median(self) -> sf.TReal:
        """
        Getter property for the median of the distribution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self.Mean
    
    @property
    def Q1(self) -> float:
        """
        Getter property for the first quartile of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        Result = self.Mean - self.Sigma * 0.6744898
        return Result
    
    @property
    def Q3(self) -> float:
        """
        Getter property for the third quartile of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        Result = self.Mean + self.Sigma * 0.6744898
        return Result
    
    @property
    def Var(self) -> sf.TReal:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self.Sigma * self.Sigma
    
    @property
    def Sigma(self) -> float:
        """
        Getter property for the standard deviation of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 1.0
    
    @property
    def Skew(self) -> float:
        """
        Getter property for the skewness of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 0.0
    
    @property
    def Kurt(self) -> float:
        """
        Getter property for the excess kurtosis of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 0.0

class Gaussian(Z_Distribution):
    """
    Implementation of the generic Gaussian distribution. Must be instantiated
    with two arguments: mean and sigma.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float = - math.inf
        Max: (read-only) float = math.inf
        Mean: float OR int
        Median: (read-only) float OR int
        Q1: (read-only) float
        Q2: (read-only) float
        Var: (read-only) float OR int
        Sigma: float > 0 OR int > 0
        Skew: (read-only) float = 0.0
        Kurt: (read-only) float = 0.0
    
    Methods:
        pdf(x)
            int OR float -> float >= 0
        cdf(x)
            int OR float -> 0 < float < 1
        qf()
            0 < float < 1 -> float
        getQuantile(k, m)
            int > 0, int > 0 -> float
        getHistogram()
            int OR float, int OR float, int > 1
                -> tuple(tuple(int OR float, float >= 0))
        random()
            None -> float
    
    Version 1.0.0.0
    """
    
    #special methods
    
    def __init__(self, Mean: sf.TReal, Sigma: sf.TReal) -> None:
        """
        Initialization. Sets the parameters of the distribution.
        
        Signature:
            int OR float, int > 0 OR float > 0 -> None
        
        Raises:
            UT_TypeError: any of the passed value is not a real number
            UT_ValueError: sigma value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Mean, (int, float)):
            raise UT_TypeError(Mean, (int, float), SkipFrames = 1)
        if not isinstance(Sigma, (int, float)):
            raise UT_TypeError(Sigma, (int, float), SkipFrames = 1)
        if Sigma <= 0:
            raise UT_ValueError(Sigma, '> 0 - sigma parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Mean'] = Mean
        self._Parameters['Sigma'] = Sigma
    
    #public properties
    
    @property
    def Mean(self) -> float:
        """
        Property for the arithmetic mean of the distribution, which is also the
        parameter of the distibution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self._Parameters['Mean']
    
    @Mean.setter
    def Mean(self, Value: sf.TReal) -> None:
        """
        Setter method for the mean parameter of the distribtion.
        
        Signature:
            float OR int -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        self._Parameters['Mean'] = Value
    
    @property
    def Sigma(self) -> float:
        """
        Property for the standard deviation of the distribution, which is also
        the sigma parameter of the distribution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self._Parameters['Sigma']
    
    @Sigma.setter
    def Sigma(self, Value: sf.TReal) -> None:
        """
        Setter method for the sigma parameter of the distribtion.
        
        Signature:
            float > 0 OR int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
            UT_ValueError: passed value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0', SkipFrames = 1)
        self._Parameters['Sigma'] = Value
