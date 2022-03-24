#usr/bin/python3
"""
Module statistics_lib.distribution_classes

Classes:
    ContinuousDistributionABC
    DiscreteDistributionABC
    Z_Distribution
    Gaussian
    Exponential
    Student
    ChiSquare
    Gamma
    Erlang
"""

__version__= '1.0.0.0'
__date__ = '24-03-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os
import math
import abc

from random import random as base_random

from typing import ClassVar, Tuple, Union

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
    
    def _qf(self, x: float) -> sf.TReal:
        """
        The actual (internal) implementation of the ICDF / QF function. This
        is the default option using bisection if the ICDF cannot be easily
        calculated using simple or special mathematical functions.
        
        Signature:
           0 < float < 1 -> int OR float
        
        Version 1.0.0.0
        """
        Sigma = self.Sigma
        Min = self.Min
        Max = self.Max
        Precision = 1.0E-8
        Point = self.Mean #check self.Mean
        y = self._cdf(Point)
        if abs(y - x) <= Precision: #instant hit
            Result = Point
        else: #need to find an interval below or above self.Mean -> find a frame
            #+ self.Sigma width at max, where the value lays
            Result = None
            if y < x: #between self.Mean and self.Max
                Left = Point
                while Left < Max:
                    Right = min(Left + Sigma, Max)
                    z = self._cdf(Right)
                    if abs(z - x) <= Precision: #found solution
                        Result = Right
                        break
                    elif z > x: #found frame
                        break
                    Left = Right
            else: #between self.Min and self.Mean
                Right = Point
                while Right > Min:
                    Left = max(Right - Sigma, Min)
                    z = self._cdf(Left)
                    if abs(z - x) <= Precision: #found solution
                        Result = Left
                        break
                    elif z < x: #found frame
                        break
                    Right = Left
            if Result is None: #only frame is found, not the solution
                #narrow it down by bisection until the difference in either
                #+ probability or in the value (position) is below the precision
                Point = 0.5 * (Left + Right)
                while (Right - Left) > Precision:
                    y = self._cdf(Point)
                    if abs(y - x) <= Precision: #found solution
                        Result = Point
                        break
                    elif y > x:
                        Right = Point
                    else:
                        Left = Point
                    Point = 0.5 * (Left + Right)
        return Result
    
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
        if x < self.Min or x >= self.Max:
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
        if k <= 0:
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
    
    #private instance methods
    
    def _qf(self, x: float) -> sf.TReal:
        """
        The actual (internal) implementation of the ICDF / QF function. This
        is the default option using bisection if the ICDF cannot be easily
        calculated using simple or special mathematical functions.
        
        Signature:
           0 < float < 1 -> int OR float
        
        Version 1.0.0.0
        """
        Sigma = self.Sigma
        Min = self.Min
        Max = self.Max
        Precision = 1.0E-8
        #check for x <= self.pdf(self.Min)
        y = self._pdf(Min)
        if abs(y - x) <= Precision: #instant hit
            Result = Min
        elif y > x: #just below self.Min - use linear extrapolation
            Result = Min - 1 + x /y
        else: #between self.Min and self.Max
            Point = round(self.Mean) #check self.Mean
            y = self._cdf(Point) 
            if abs(y - x) <= Precision: #instant hit
                Result = Point
            else: # below or above self.Mean -> find a frame self.Sigma width
                #+ at max, where the value lays
                Result = None
                if y < x: #shift towards self.Max
                    Left = Point
                    while Left < Max:
                        Right = min(round(Left + Sigma), Max)
                        z = self._cdf(Right)
                        if abs(z - x) <= Precision: #found solution
                            Result = Right
                            break
                        elif z > x: #found the frame
                            break
                        Left = Right
                else: #shift towards self.Min
                    Right = Point
                    while Right > Min:
                        Left = max(round(Right - Sigma), Min)
                        z = self._cdf(Left)
                        if abs(z - x) <= Precision: #found solution
                            Result = Left
                            break
                        elif z < x: #found the frame
                            break
                        Right = Left
                if Result is None:
                    #a frame with width <= self.Sigma is found - narrow it down
                    #+ to a single step = 1 using bisection
                    Point = round(0.5 * (Left + Right))
                    while (Right - Left) > 1:
                        y = self._cdf(Point)
                        if abs(y - x) <= Precision: #found solution
                            Result = Point
                            break
                        elif y > x:
                            Right = Point
                        else:
                            Left = Point
                        Point = round(0.5 * (Left + Right))
                    else: #solution is still not found
                        #+ use linear interpolation between two integer steps
                        LeftCDF = self._cdf(Left)
                        Slope = self._cdf(Right) - LeftCDF
                        Result = Left + (x - LeftCDF) / Slope
        return Result
    
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
        x_floor = int(math.floor(x))
        if x_floor >= self.Max:
            Result = 1
        elif x_floor < self.Min:
            Result = 0
        else:
            Result = self._cdf(x_floor)
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
        return Result
    
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
        Setter method for the mean parameter of the distribution.
        
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
            None -> float > 0  OR int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Sigma']
    
    @Sigma.setter
    def Sigma(self, Value: sf.TReal) -> None:
        """
        Setter method for the sigma parameter of the distribution.
        
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
            raise UT_ValueError(Value, '> 0 - sigma parameter', SkipFrames = 1)
        self._Parameters['Sigma'] = Value

class Exponential(ContinuousDistributionABC):
    """
    Implementation of the exponential distribution. Must be instantiated with
    a single positive real number argument.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float = 0
        Max: (read-only) float = math.inf
        Mean: (read-only) float
        Median: (read-only) float
        Q1: (read-only) float
        Q2: (read-only) float
        Var: (read-only) float
        Sigma: (read-only) float
        Skew: (read-only) float
        Kurt: (read-only) float
        Rate: int > 0 OR float > 0
    
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
    
    #class 'private' fields
    
    _Min: ClassVar[sf.TReal] = 0
    
    #special methods
    
    def __init__(self, Rate: sf.TReal) -> None:
        """
        Initialization. Set the single parameter of the distribution - the
        positive rate.
        
        Signature:
            int > 0 OR float > 0 -> None
        
        Args:
            Rate: int > 0 OR float > 0; the single parameter of the distribution
        
        Raises:
            UT_TypeError: the argument is neither int nor float
            UT_ValueError: the argument is zero or negaive
        
        Version 1.0.0.0
        """
        if not isinstance(Rate, (int, float)):
            raise UT_TypeError(Rate, (int, float), SkipFrames = 1)
        if Rate <= 0:
            raise UT_ValueError(Rate, '> 0 - rate parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Rate'] = Rate
    
    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int OR float -> float >= 0
        
        Version 1.0.0.0
        """
        Rate = self.Rate
        Result = math.exp(- Rate * x) * Rate
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        1.0.0.0
        """
        Result = 1 - math.exp(- self.Rate * x)
        return Result
    
    def _qf(self, p: float) -> sf.TReal:
        """
        The actual implementation of the ICDF / QF function.
        
        Signature:
           0 < float < 1 -> int OR float
        
        Version 1.0.0.0
        """
        Result = - math.log(1 - p) / self.Rate
        return Result
    
    #public properties
    
    @property
    def Rate(self) -> sf.TReal:
        """
        Property for the rate parameter of the distribution.
        
        Signature:
            None -> int > 0 OR float > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Rate']
    
    @Rate.setter
    def Rate(self, Value: sf.TReal) -> None:
        """
        Setter method for the rate parameter of the distribution.
        
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
            raise UT_ValueError(Value, '> 0 - rate parameter', SkipFrames = 1)
        self._Parameters['Rate'] = Value
    
    @property
    def Mean(self) -> float:
        """
        Getter property for the arithmetic mean of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 1 / self.Rate
    
    @property
    def Median(self) -> sf.TReal:
        """
        Getter property for the median of the distribution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        Result = - math.log(0.5) / self.Rate
        return Result
    
    @property
    def Q1(self) -> float:
        """
        Getter property for the first quartile of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        Result = - math.log(0.75) / self.Rate
        return Result
    
    @property
    def Q3(self) -> float:
        """
        Getter property for the third quartile of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        Result = - math.log(0.25) / self.Rate
        return Result
    
    @property
    def Var(self) -> sf.TReal:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return 1 / (self.Rate * self.Rate)
    
    @property
    def Sigma(self) -> float:
        """
        Getter property for the standard deviation of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 1 / self.Rate
    
    @property
    def Skew(self) -> float:
        """
        Getter property for the skewness of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 2.0
    
    @property
    def Kurt(self) -> float:
        """
        Getter property for the excess kurtosis of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 6.0

class Student(ContinuousDistributionABC):
    """
    Implementation of the Student's t-distribution. Must be instantiated with
    a single positive real number argument.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float = - math.inf
        Max: (read-only) float = math.inf
        Mean: (read-only) float = 0 OR None
        Median: (read-only) float = 0
        Q1: (read-only) float
        Q2: (read-only) float
        Var: (read-only) float OR None
        Sigma: (read-only) float OR None
        Skew: (read-only) float OR None
        Kurt: (read-only) float OR None
        Degree: int > 0 OR float > 0
    
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
    
    def __init__(self, Degree: sf.TReal) -> None:
        """
        Initialization. Set the single parameter of the distribution - the
        positive number as the number of degrees of freedom (not necessarily an
        integer).
        
        Signature:
            int > 0 OR float > 0 -> None
        
        Args:
            Degree: int > 0 OR float > 0; the single parameter of the
                distribution
        
        Raises:
            UT_TypeError: the argument is neither int nor float
            UT_ValueError: the argument is zero or negaive
        
        Version 1.0.0.0
        """
        if not isinstance(Degree, (int, float)):
            raise UT_TypeError(Degree, (int, float), SkipFrames = 1)
        if Degree <= 0:
            raise UT_ValueError(Degree, '> 0 - rate parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Degree'] = Degree
        self._Cached = dict()
        Temp = math.lgamma(0.5 * (Degree + 1)) - math.lgamma(0.5 * Degree)
        Temp -= 0.5 * math.log(Degree * math.pi)
        self._Cached['Factor'] = math.exp(Temp) #correction factor for PDF
        self._Cached['Q1'] = None #cached first quartile
        self._Cached['Q3'] = None #cached third quartile
    
    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int OR float -> float >= 0
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        Factor = self._Cached['Factor']
        Result = Factor * math.pow(1 + x * x / Degree, - 0.5*(Degree + 1))
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        1.0.0.0
        """
        Degree = self.Degree
        #---
        def inner(x: sf.TReal) -> float:
            """
            Closure to wrap a call to incomplete regularized beta function.
            """
            z = Degree / (Degree + x * x)
            x = 0.5 * Degree
            y = 0.5
            Value = 0 #TODO call Iz(x,y) = B(z; x, y) / B(x, y)
            return Value
        #---
        if x > 0:
            Result = 1 - inner(x)
        elif x < 0:
            Result = inner(x)
        else:
            Result = 0
        return Result
    
    def _qf(self, p: float) -> sf.TReal:
        """
        The actual implementation of the ICDF / QF function.
        
        Signature:
           0 < float < 1 -> int OR float
        
        Version 1.0.0.0
        """
        if p == 0.5:
            Result = 0
        else:
            Degree = self.Degree
            if Degree == 1:
                Result = math.tan(math.pi * (p - 0.5))
            elif Degree == 2:
                Result = math.sqrt(0.5 * (p * (1 -p)))
            elif Degree == 4:
                a = math.sqrt(4 * p * (1 - p))
                q = math.sqrt(math.cos(math.acos(a) / 3) / a - 1)
                if p > 0.5:
                    Result = q
                else:
                    Result = -q
            else:
                Result = super()._qf(p)
        return Result
    
    #public properties
    
    @property
    def Degree(self) -> sf.TReal:
        """
        Property for the number of degrees of freedom parameter of the
        distribution.
        
        Signature:
            None -> int > 0 OR float > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Degree']
    
    @Degree.setter
    def Degree(self, Value: sf.TReal) -> None:
        """
        Setter method for the number of degrees of freedom parameter of the
        distribution.
        
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
            raise UT_ValueError(Value, '> 0 - rate parameter', SkipFrames = 1)
        self._Parameters['Degree'] = Value
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        Temp = math.lgamma(0.5 * (Value + 1)) - math.lgamma(0.5 * Value)
        Temp -= 0.5 * math.log(Value * math.pi)
        self._Cached['Factor'] = math.exp(Temp)
    
    @property
    def Mean(self) -> Union[float, None]:
        """
        Getter property for the arithmetic mean of the distribution.
        
        Signature:
            None -> float OR None
        
        Returns:
            float = 0.0: number of degrees of freedom > 1
            None: number of degrees of freedom is in the interval (0, 1]
        
        Version 1.0.0.0
        """
        if self.Degree > 1:
            Result = 0
        else:
            Result = None
        return Result
    
    @property
    def Median(self) -> float:
        """
        Getter property for the median of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 0.0
    
    @property
    def Q1(self) -> float:
        """
        Getter property for the first quartile of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        if self._Cached['Q1'] is None:
            Result = self._qf(0.25)
            self._Cached['Q1'] = Result
        else:
            Result = self._Cached['Q1']
        return Result
    
    @property
    def Q3(self) -> float:
        """
        Getter property for the third quartile of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        if self._Cached['Q3'] is None:
            Result = self._qf(0.75)
            self._Cached['Q3'] = Result
        else:
            Result = self._Cached['Q3']
        return Result
    
    @property
    def Var(self) -> Union[float, None]:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> float OR None
        
        Returns:
            float = 0.0: number of degrees of freedom > 2
            float = math.inf: number of degrees of freedom is in the interval
                (1, 2]
            None: number of degrees of freedom is in the interval (0, 1]
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        if Degree > 2:
            Result = Degree / (Degree - 2)
        elif Degree > 1:
            Result = math.inf
        else:
            Result = None
        return Result
    
    @property
    def Sigma(self) -> Union[float, None]:
        """
        Getter property for the standard deviation of the distribution.
        
        Signature:
            None -> float OR None
        
        Returns:
            float = 0.0: number of degrees of freedom > 2
            float = math.inf: number of degrees of freedom is in the interval
                (1, 2]
            None: number of degrees of freedom is in the interval (0, 1]
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        if Degree > 2:
            Result = math.sqrt(Degree / (Degree - 2))
        elif Degree > 1:
            Result = math.inf
        else:
            Result = None
        return Result
    
    @property
    def Skew(self) -> Union[float, None]:
        """
        Getter property for the skewness of the distribution.
        
        Signature:
            None -> float OR None
        
        Returns:
            float = 0.0: number of degrees of freedom > 3
            None: number of degrees of freedom is in the interval (0, 3]
        
        Version 1.0.0.0
        """
        if self.Degree > 3:
            Result = 0
        else:
            Result = None
        return Result
    
    @property
    def Kurt(self) -> Union[float, None]:
        """
        Getter property for the excess kurtosis of the distribution.
        
        Signature:
            None -> float OR None
        
        Returns:
            float: number of degrees of freedom > 4
            float = math.inf: number of degrees of freedom is in the interval
                (2, 4]
            None: number of degrees of freedom is in the interval (0, 2]
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        if Degree > 4:
            Result = 6 / (Degree - 4)
        elif Degree > 2:
            Result = math.inf
        else:
            Result = None
        return Result

class ChiSquare(Student):
    """
    Implementation of the chi-square distribution. Must be instantiated with
    a single positive integer number argument.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float >= 0
        Max: (read-only) float = math.inf
        Mean: (read-only) int
        Median: (read-only) float OR int
        Q1: (read-only) float OR int
        Q2: (read-only) float OR int
        Var: (read-only) int
        Sigma: (read-only) float
        Skew: (read-only) float
        Kurt: (read-only) float
        Degree: int > 0
    
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
    
    #class 'private' fields
    
    _Min: ClassVar[sf.TReal] = 0
    
    #special methods
    
    def __init__(self, Degree: int) -> None:
        """
        Initialization. Set the single parameter of the distribution - the
        positive number as the number of degrees of freedom (not necessarily an
        integer).
        
        Signature:
            int > 0 -> None
        
        Args:
            Degree: int > 0; the single parameter of the distribution
        
        Raises:
            UT_TypeError: the argument is neither int nor float
            UT_ValueError: the argument is zero or negaive
        
        Version 1.0.0.0
        """
        if not isinstance(Degree, int):
            raise UT_TypeError(Degree, int, SkipFrames = 1)
        if Degree < 1:
            raise UT_ValueError(Degree, '> 0 - rate parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Degree'] = Degree
        self._Cached = dict()
        Temp = math.gamma(Degree / 2) * math.pow(2, Degree / 2)
        self._Cached['Factor'] = 1 / Temp #correction factor for PDF
        self._Cached['Q1'] = None #cached first quartile
        self._Cached['Q3'] = None #cached third quartile
        self._Cached['Median'] = None
        if Degree == 1: #override the class attribute, make open > 0 interval
            self._Min = sys.float_info.epsilon
    
    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int OR float -> float >= 0
        
        Version 1.0.0.0
        """
        k = self.Degree
        Result=self._Cached['Factor'] * math.pow(x, 0.5*k - 1) * math.exp(- x/2)
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        1.0.0.0
        """
        Result = 0 #call regularized lower incomplete gamma function P(k/2, x/2)
        return Result
    
    def _qf(self, p: float) -> sf.TReal:
        """
        The actual implementation of the ICDF / QF function using the default
        bisection algorithm.
        
        Signature:
           0 < float < 1 -> int OR float
        
        Version 1.0.0.0
        """
        return super()._qf(p)
    
    #public properties
    
    @property
    def Degree(self) -> int:
        """
        Property for the number of degrees of freedom parameter of the
        distribution.
        
        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Degree']
    
    @Degree.setter
    def Degree(self, Value: int) -> None:
        """
        Setter method for the number of degrees of freedom parameter of the
        distribution.
        
        Signature:
            int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not an integer number
            UT_ValueError: passed value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Value, int):
            raise UT_TypeError(Value, int, SkipFrames = 1)
        if Value < 1:
            raise UT_ValueError(Value, '> 0 - rate parameter', SkipFrames = 1)
        self._Parameters['Degree'] = Value
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        Temp = math.gamma(Value / 2) * math.pow(2, Value / 2)
        self._Cached['Factor'] = 1 / Temp
        if Value == 1: #override the class attribute, make open > 0 interval
            self._Min = sys.float_info.epsilon
        else: # > 1 - makes the interval closed
            self._Min = 0
    
    @property
    def Mean(self) -> int:
        """
        Getter property for the arithmetic mean of the distribution.
        
        Signature:
            None -> int
        
        Version 1.0.0.0
        """
        return self.Degree
    
    @property
    def Median(self) -> float:
        """
        Getter property for the median of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        if self._Cached['Median'] is None:
            Result = self._qf(0.5)
            self._Cached['Median'] = Result
        else:
            Result = self._Cached['Median']
        return Result
    
    @property
    def Var(self) -> int:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> int
        
        Version 1.0.0.0
        """
        return 2 * self.Degree
    
    @property
    def Sigma(self) -> float:
        """
        Getter property for the standard deviation of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return math.sqrt(2 * self.Degree)
    
    @property
    def Skew(self) -> float:
        """
        Getter property for the skewness of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return math.sqrt(8) / self.Degree
    
    @property
    def Kurt(self) -> float:
        """
        Getter property for the excess kurtosis of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return 12 / self.Degree

class Gamma(ContinuousDistributionABC):
    """
    Implementation of the Gamma distribution. Must be instantiated with
    two positive real number arguments - shape and rate.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float > 0
        Max: (read-only) float = math.inf
        Mean: (read-only) float > 0
        Median: (read-only) float > 0
        Q1: (read-only) float > 0
        Q2: (read-only) float > 0
        Var: (read-only) float > 0
        Sigma: (read-only) float > 0
        Skew: (read-only) float > 0
        Kurt: (read-only) float > 0
        Shape: int > 0 OR float > 0
        Rate: int > 0 OR float > 0
    
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
    
    #class 'private' fields
    
    _Min: ClassVar[sf.TReal] = sys.float_info.epsilon
    
    #special methods
    
    def __init__(self, Shape: sf.TReal, Rate: sf.TReal) -> None:
        """
        Initialization. Set the shape and rate parameters of the distribution.
        
        Signature:
            int > 0 OR float > 0, int > 0 OR float > 0 -> None
        
        Args:
            Shape: int > 0 OR float > 0; the shape parameter of the distribution
            Rate: int > 0 OR float > 0; the rate parameter of the distribution
        
        Raises:
            UT_TypeError: either of the arguments is neither int nor float
            UT_ValueError: either of the arguments is zero or negaive
        
        Version 1.0.0.0
        """
        if not isinstance(Shape, (int, float)):
            raise UT_TypeError(Shape, (int, float), SkipFrames = 1)
        if Shape <= 0:
            raise UT_ValueError(Shape, '> 0 - shape parameter', SkipFrames = 1)
        if not isinstance(Rate, (int, float)):
            raise UT_TypeError(Rate, (int, float), SkipFrames = 1)
        if Rate <= 0:
            raise UT_ValueError(Rate, '> 0 - rate parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Shape'] = Shape
        self._Parameters['Rate'] = Rate
        self._Cached = dict()
        Temp = math.exp(Shape * math.log(Rate) - math.lgamma(Shape))
        self._Cached['Factor'] = Temp #correction factor for PDF
        self._Cached['Q1'] = None #cached first quartile
        self._Cached['Q3'] = None #cached third quartile
        self._Cached['Median'] = None
    
    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int OR float -> float >= 0
        
        Version 1.0.0.0
        """
        Shape = self._Parameters['Shape']
        Rate = self._Parameters['Rate']
        Factor = self._Cached['Factor']
        Result= Factor * math.pow(x, Shape - 1) * math.exp(- Rate * x)
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        1.0.0.0
        """
        Result = 0 #call regularized lower incomplete gamma function
        #+ P(Shape, x * Rate)
        return Result
    
    #public properties
    
    @property
    def Shape(self) -> sf.TReal:
        """
        Property for the shape parameter of the distribution.
        
        Signature:
            None -> int > 0 OR float > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Shape']
    
    @Shape.setter
    def Shape(self, Value: sf.TReal) -> None:
        """
        Setter method for the shape parameter of the distribution.
        
        Signature:
            int > 0 OR float > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
            UT_ValueError: passed value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - shape parameter', SkipFrames = 1)
        self._Parameters['Shape'] = Value
        Shape = Value
        Rate = self._Parameters['Rate']
        Temp = math.exp(Shape * math.log(Rate) - math.lgamma(Shape))
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        self._Cached['Factor'] = Temp
    
    #public properties
    
    @property
    def Rate(self) -> sf.TReal:
        """
        Property for the rate parameter of the distribution.
        
        Signature:
            None -> int > 0 OR float > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Rate']
    
    @Rate.setter
    def Rate(self, Value: sf.TReal) -> None:
        """
        Setter method for the rate parameter of the distribution.
        
        Signature:
            int > 0 OR float > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
            UT_ValueError: passed value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - rate parameter', SkipFrames = 1)
        self._Parameters['Rate'] = Value
        Rate = Value
        Shape = self._Parameters['Shape']
        Temp = math.exp(Shape * math.log(Rate) - math.lgamma(Shape))
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        self._Cached['Factor'] = Temp
    
    @property
    def Mean(self) -> float:
        """
        Getter property for the arithmetic mean of the distribution.
        
        Signature:
            None -> float > 0
        
        Version 1.0.0.0
        """
        Shape = self._Parameters['Shape']
        Rate = self._Parameters['Rate']
        Result = Shape / Rate
        return Result
    
    @property
    def Median(self) -> float:
        """
        Getter property for the median of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        if self._Cached['Median'] is None:
            Result = self._qf(0.5)
            self._Cached['Median'] = Result
        else:
            Result = self._Cached['Median']
        return Result
    
    @property
    def Q1(self) -> float:
        """
        Getter property for the first quartile of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        if self._Cached['Q1'] is None:
            Result = self._qf(0.25)
            self._Cached['Q1'] = Result
        else:
            Result = self._Cached['Q1']
        return Result
    
    @property
    def Q3(self) -> float:
        """
        Getter property for the third quartile of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        if self._Cached['Q3'] is None:
            Result = self._qf(0.75)
            self._Cached['Q3'] = Result
        else:
            Result = self._Cached['Q3']
        return Result
    
    @property
    def Var(self) -> float:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> float > 0
        
        Version 1.0.0.0
        """
        Shape = self._Parameters['Shape']
        Rate = self._Parameters['Rate']
        Result = Shape / (Rate * Rate)
        return Result
    
    @property
    def Sigma(self) -> float:
        """
        Getter property for the standard deviation of the distribution.
        
        Signature:
            None -> float > 0
        
        Version 1.0.0.0
        """
        Shape = self._Parameters['Shape']
        Rate = self._Parameters['Rate']
        Result = math.sqrt(Shape) / Rate
        return Result
    
    @property
    def Skew(self) -> float:
        """
        Getter property for the skewness of the distribution.
        
        Signature:
            None -> float > 0
        
        Version 1.0.0.0
        """
        Result = 2 / math.sqrt(self._Parameters['Shape'])
        return Result
    
    @property
    def Kurt(self) -> float:
        """
        Getter property for the excess kurtosis of the distribution.
        
        Signature:
            None -> float > 0
        
        Version 1.0.0.0
        """
        Result = 6 / self._Parameters['Shape']
        return Result

class Erlang(Gamma):
    """
    Implementation of the Erlang distribution. Must be instantiated with
    a positive integer argument - shape, and a positive real number argument -
    rate.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float = 0
        Max: (read-only) float = math.inf
        Mean: (read-only) float > 0
        Median: (read-only) float > 0
        Q1: (read-only) float > 0
        Q2: (read-only) float > 0
        Var: (read-only) float > 0
        Sigma: (read-only) float > 0
        Skew: (read-only) float > 0
        Kurt: (read-only) float > 0
        Shape: int > 0
        Rate: int > 0 OR float > 0
    
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
    
    #class 'private' fields
    
    _Min: ClassVar[int] = 0
    
    #special methods
    
    def __init__(self, Shape: int, Rate: sf.TReal) -> None:
        """
        Initialization. Set the shape and rate parameters of the distribution.
        
        Signature:
            int > 0, int > 0 OR float > 0 -> None
        
        Args:
            Shape: int > 0; the shape parameter of the distribution
            Rate: int > 0 OR float > 0; the rate parameter of the distribution
        
        Raises:
            UT_TypeError: either of the arguments is neither int nor float
            UT_ValueError: either of the arguments is zero or negaive
        
        Version 1.0.0.0
        """
        if not isinstance(Shape, int):
            raise UT_TypeError(Shape, int, SkipFrames = 1)
        if Shape < 1:
            raise UT_ValueError(Shape, '> 0 - shape parameter', SkipFrames = 1)
        if not isinstance(Rate, (int, float)):
            raise UT_TypeError(Rate, (int, float), SkipFrames = 1)
        if Rate <= 0:
            raise UT_ValueError(Rate, '> 0 - rate parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Shape'] = Shape
        self._Parameters['Rate'] = Rate
        self._Cached = dict()
        Temp = math.exp(Shape * math.log(Rate) - math.lgamma(Shape))
        self._Cached['Factor'] = Temp #correction factor for PDF
        self._Cached['Q1'] = None #cached first quartile
        self._Cached['Q3'] = None #cached third quartile
        self._Cached['Median'] = None
    
    #public properties
    
    @property
    def Shape(self) -> int:
        """
        Property for the shape parameter of the distribution.
        
        Signature:
            None -> int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Shape']
    
    @Shape.setter
    def Shape(self, Value: int) -> None:
        """
        Setter method for the shape parameter of the distribution.
        
        Signature:
            int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not an integer number
            UT_ValueError: passed value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Value, int):
            raise UT_TypeError(Value, int, SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - shape parameter', SkipFrames = 1)
        self._Parameters['Shape'] = Value
        Shape = Value
        Rate = self._Parameters['Rate']
        Temp = math.exp(Shape * math.log(Rate) - math.lgamma(Shape))
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        self._Cached['Factor'] = Temp