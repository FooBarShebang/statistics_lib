#usr/bin/python3
"""
Module statistics_lib.inverse_distributions

Provides classes implementing a number of inverse and ratio distributions. All
classes have properties returning the basic statistical properties of the
distribution: mean, median, the first and the third quartile, variance and
standard deviation, skewness and excess kurtosis. They also have methods to
calculate PDF / PMF and CDF for a given value, QF and a generic k-th of m
quantile, with 0 < k < m, as well as a histogram of the distribution within
specific bounds and with the specified number of bins. The parameters of a
distribution are defined during instantiation, and they can be changed later via
setter properties.

Classes:
    InverseGaussian
    InverseGamma
    InverseChiSquared
    ScaledInverseChiSquared
    Cauchy
    Levy
"""

__version__= '1.0.0.0'
__date__ = '29-04-2022'
__status__ = 'Production'

#imports

#+ standard library

import sys
import os
import math

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

from statistics_lib.distribution_classes import ContinuousDistributionABC as BC

# classes

class InverseGaussian(BC):
    """
    Implementation of the inverse Gaussian distribution. Must be instantiated
    with two positive real number arguments: mean and shape.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float > 0
        Max: (read-only) float = math.inf
        Mean: float > 0  OR int > 0
        Median: (read-only) float > 0
        Q1: (read-only) float > 0
        Q2: (read-only) float > 0
        Var: (read-only) float > 0
        Sigma: (read-only) float > 0
        Skew: (read-only) float > 0
        Kurt: (read-only) float > 0
        Shape: float > 0 OR int > 0
    
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
            None -> float > 0
    
    Version 1.0.0.0
    """

    #class 'private' fields
    
    _Min: ClassVar[sf.TReal] = 2 * sys.float_info.min

    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int > 0 OR float > 0 -> float >= 0
        
        Version 1.0.0.0
        """
        Mean = self.Mean
        Shape = self.Shape
        z = 0.5 * Shape * math.pow((x / Mean - 1), 2) / x
        if z > 300:
            Result = 0.0
        else:
            Temp = 0.5 * Shape / (math.pi * math.pow(x, 3))
            Result = math.sqrt(Temp) * math.exp(-z)
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        Version 1.0.0.0
        """
        Mean = self.Mean
        Shape = self.Shape
        z1 = math.sqrt(0.5 * Shape / x) * (x / Mean - 1)
        z2 = math.sqrt(0.5 * Shape / x) * (x / Mean + 1)
        Result = 0.5 * (1 + math.erf(z1))
        Result += 0.5 * math.exp(2 * Shape / Mean) * (1 + math.erf(-z2))
        return Result

    #special methods
    
    def __init__(self, Mean: sf.TReal, Shape: sf.TReal) -> None:
        """
        Initialization. Sets the parameters of the distribution.
        
        Signature:
            int > 0 OR float > 0, int > 0 OR float > 0 -> None
        
        Args:
            Mean: int > 0 OR float > 0; the mean parameter of the distribution
            Shape: int > 0 OR float > 0; the shape parameter of the distribution

        Raises:
            UT_TypeError: any of the passed values is not a real number
            UT_ValueError: any of the passed values is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Mean, (int, float)):
            raise UT_TypeError(Mean, (int, float), SkipFrames = 1)
        if not isinstance(Shape, (int, float)):
            raise UT_TypeError(Shape, (int, float), SkipFrames = 1)
        if Mean <= 0:
            raise UT_ValueError(Mean, '> 0 - mean parameter', SkipFrames = 1)
        if Shape <= 0:
            raise UT_ValueError(Shape, '> 0 - sigma parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Mean'] = Mean
        self._Parameters['Shape'] = Shape
        self._Cached = dict()
        self._Cached['Median'] = None# cahed median value
        self._Cached['Q1'] = None #cached first quartile
        self._Cached['Q3'] = None #cached third quartile

    #public properties
    
    @property
    def Mean(self) -> sf.TReal:
        """
        Property for the arithmetic mean of the distribution, which is also the
        parameter of the distibution.
        
        Signature:
            None -> float > 0 OR int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Mean']
    
    @Mean.setter
    def Mean(self, Value: sf.TReal) -> None:
        """
        Setter method for the mean parameter of the distribution.
        
        Signature:
            float > 0 OR int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - mean parameter', SkipFrames = 1)
        self._Parameters['Mean'] = Value
        for Key in self._Cached.keys():
            self._Cached[Key] = None
    
    @property
    def Shape(self) -> sf.TReal:
        """
        Property for the shape parameter of the distribution.
        
        Signature:
            None -> float > 0 OR int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Shape']
    
    @Shape.setter
    def Shape(self, Value: sf.TReal) -> None:
        """
        Setter method for the shape parameter of the distribution.
        
        Signature:
            float > 0 OR int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - shape parameter', SkipFrames = 1)
        self._Parameters['Shape'] = Value
        for Key in self._Cached.keys():
            self._Cached[Key] = None
    
    @property
    def Var(self) -> float:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> float > 0
        
        Version 1.0.0.0
        """
        return math.pow(self.Mean, 3) / self.Shape

    @property
    def Skew(self) -> float:
        """
        Getter property for the skewness of the distribution.
        
        Signature:
            None -> float >0
        
        Version 1.0.0.0
        """
        return 3 * math.sqrt(self.Mean / self.Shape)
    
    @property
    def Kurt(self) -> float:
        """
        Getter property for the excess kurtosis of the distribution.
        
        Signature:
            None -> float > 0
        
        Version 1.0.0.0
        """
        return 15.0 * self.Mean / self.Shape

class InverseGamma(BC):
    """
    Implementation of the inverse Gamma distribution. Must be instantiated
    with two positive real number arguments: shape and scale.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float > 0
        Max: (read-only) float = math.inf
        Mean: (read-only) float > 0 OR None
        Median: (read-only) float > 0
        Q1: (read-only) float > 0
        Q2: (read-only) float > 0
        Var: (read-only) float > 0 OR None
        Sigma: (read-only) float > 0 OR None
        Skew: (read-only) float > 0 OR None
        Kurt: (read-only) float > 0 OR None
        Shape: float > 0 OR int > 0
        Scale: float > 0 OR int > 0
    
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
            None -> float > 0
    
    Version 1.0.0.0
    """

    #class 'private' fields
    
    _Min: ClassVar[sf.TReal] = 2 * sys.float_info.min

    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int > 0 OR float > 0 -> float >= 0
        
        Version 1.0.0.0
        """
        Scale = self.Scale
        Shape = self.Shape
        z = Scale / x
        if z > 300:
            Result = 0.0
        else:
            Temp = self._Cached['Factor'] - (Shape + 1) * math.log(x) - z
            Result = math.exp(Temp)
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        Version 1.0.0.0
        """
        Scale = self.Scale
        Shape = self.Shape
        Result = sf.upper_gamma_reg(Shape, Scale / x)
        return Result

    #special methods
    
    def __init__(self, Shape: sf.TReal, Scale: sf.TReal) -> None:
        """
        Initialization. Sets the parameters of the distribution.
        
        Signature:
            int > 0 OR float > 0, int > 0 OR float > 0 -> None
        
        Args:
            Shape: int > 0 OR float > 0; the shape parameter of the distribution
            Scale: int > 0 OR float > 0; the scale parameter of the distribution

        Raises:
            UT_TypeError: any of the passed values is not a real number
            UT_ValueError: any of the passed values is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Scale, (int, float)):
            raise UT_TypeError(Scale, (int, float), SkipFrames = 1)
        if not isinstance(Shape, (int, float)):
            raise UT_TypeError(Shape, (int, float), SkipFrames = 1)
        if Scale <= 0:
            raise UT_ValueError(Scale, '> 0 - scale parameter', SkipFrames = 1)
        if Shape <= 0:
            raise UT_ValueError(Shape, '> 0 - sigma parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Scale'] = Scale
        self._Parameters['Shape'] = Shape
        self._Cached = dict()
        self._Cached['Median'] = None# cahed median value
        self._Cached['Q1'] = None #cached first quartile
        self._Cached['Q3'] = None #cached third quartile
        self._Cached['Factor'] = Shape * math.log(Scale) - math.lgamma(Shape)

    #public properties
    
    @property
    def Scale(self) -> sf.TReal:
        """
        Property for the scale parameter of the distibution.
        
        Signature:
            None -> float > 0 OR int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Scale']
    
    @Scale.setter
    def Scale(self, Value: sf.TReal) -> None:
        """
        Setter method for the scale parameter of the distribution.
        
        Signature:
            float > 0 OR int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - scale parameter', SkipFrames = 1)
        self._Parameters['Scale'] = Value
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        Scale = Value
        Shape = self.Shape
        self._Cached['Factor'] = Shape * math.log(Scale) - math.lgamma(Shape)
    
    @property
    def Shape(self) -> sf.TReal:
        """
        Property for the shape parameter of the distribution.
        
        Signature:
            None -> float > 0 OR int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Shape']
    
    @Shape.setter
    def Shape(self, Value: sf.TReal) -> None:
        """
        Setter method for the shape parameter of the distribution.
        
        Signature:
            float > 0 OR int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - shape parameter', SkipFrames = 1)
        self._Parameters['Shape'] = Value
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        Scale = self.Scale
        Shape = Value
        self._Cached['Factor'] = Shape * math.log(Scale) - math.lgamma(Shape)
    
    @property
    def Mean(self) -> Union[float, None]:
        """
        Getter property for the arithmetic mean of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: shape parameter > 1
            None: shape parameter is in the interval (0, 1]
        
        Version 1.0.0.0
        """
        Shape = self.Shape
        Scale = self.Scale
        if Shape > 1:
            Result = Scale / (Shape - 1)
        else:
            Result = None
        return Result

    @property
    def Var(self) -> Union[float, None]:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: shape parameter > 2
            None: shape parameter is in the interval (0, 2]

        Version 1.0.0.0
        """
        Shape = self.Shape
        Scale = self.Scale
        if Shape > 2:
            Result = math.pow(Scale / (Shape - 1), 2) / (Shape - 2)
        else:
            Result = None
        return Result
    
    @property
    def Sigma(self) -> Union[float, None]:
        """
        Getter property for the standard deviation of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: shape parameter > 2
            None: shape parameter is in the interval (0, 2]

        Version 1.0.0.0
        """
        Shape = self.Shape
        Scale = self.Scale
        if Shape > 2:
            Result = (Scale / (Shape - 1)) / math.sqrt(Shape - 2)
        else:
            Result = None
        return Result

    @property
    def Skew(self) -> Union[float, None]:
        """
        Getter property for the skewness of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: shape parameter > 3
            None: shape parameter is in the interval (0, 3]

        Version 1.0.0.0
        """
        Shape = self.Shape
        if Shape > 3:
            Result = 4.0 * math.sqrt(Shape - 2) / (Shape - 3)
        else:
            Result = None
        return Result
    
    @property
    def Kurt(self) -> Union[float, None]:
        """
        Getter property for the excess kurtosis of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: shape parameter > 4
            None: shape parameter is in the interval (0, 4]

        Version 1.0.0.0
        """
        Shape = self.Shape
        if Shape > 4:
            Result = 6.0 * (5 * Shape - 11) / ((Shape - 3) * (Shape - 4))
        else:
            Result = None
        return Result

class InverseChiSquared(BC):
    """
    Implementation of the inverse chi-squared distribution. Must be instantiated
    with a positive real number argument - degree of freedom.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float > 0
        Max: (read-only) float = math.inf
        Mean: (read-only) float > 0 OR None
        Median: (read-only) float > 0
        Q1: (read-only) float > 0
        Q2: (read-only) float > 0
        Var: (read-only) float > 0 OR None
        Sigma: (read-only) float > 0 OR None
        Skew: (read-only) float > 0 OR None
        Kurt: (read-only) float > 0 OR None
        Degree: float > 0 OR int > 0
    
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
            None -> float > 0
    
    Version 1.0.0.0
    """

    #class 'private' fields
    
    _Min: ClassVar[sf.TReal] = 2 * sys.float_info.min

    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int > 0 OR float > 0 -> float >= 0
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        z = 0.5 / x
        if z > 300:
            Result = 0.0
        else:
            Temp = self._Cached['Factor'] - (0.5 * Degree + 1) * math.log(x) - z
            Result = math.exp(Temp)
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        Result = sf.upper_gamma_reg(0.5 * Degree, 0.5 / x)
        return Result

    #special methods
    
    def __init__(self, Degree: sf.TReal) -> None:
        """
        Initialization. Sets the parameter of the distribution.
        
        Signature:
            int > 0 OR float > 0 -> None
        
        Args:
            Degree: int > 0 OR float > 0; the degree of frredom parameter of the
                distribution

        Raises:
            UT_TypeError: the passed value is not a real number
            UT_ValueError: the passed value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Degree, (int, float)):
            raise UT_TypeError(Degree, (int, float), SkipFrames = 1)
        if Degree <= 0:
            raise UT_ValueError(Degree, '> 0 - degree of freedom parameter',
                                                                SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Degree'] = Degree
        self._Cached = dict()
        self._Cached['Median'] = None# cahed median value
        self._Cached['Q1'] = None #cached first quartile
        self._Cached['Q3'] = None #cached third quartile
        self._Cached['Factor']=-0.5*Degree*math.log(2) - math.lgamma(0.5*Degree)
    
    #public properties
    
    @property
    def Degree(self) -> sf.TReal:
        """
        Property for the degree of freedom parameter of the distibution.
        
        Signature:
            None -> float > 0 OR int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Degree']
    
    @Degree.setter
    def Degree(self, Value: sf.TReal) -> None:
        """
        Setter method for the degree of freedom parameter of the distribution.
        
        Signature:
            float > 0 OR int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - degree parameter', SkipFrames = 1)
        self._Parameters['Degree'] = Value
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        Degree = Value
        self._Cached['Factor']=-0.5*Degree*math.log(2) - math.lgamma(0.5*Degree)
    
    @property
    def Mean(self) -> Union[float, None]:
        """
        Getter property for the arithmetic mean of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: number of degrees of freedom > 2
            None: number of degrees of freedom is in the interval (0, 2]
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        if Degree > 2:
            Result = 1.0 / (Degree - 2)
        else:
            Result = None
        return Result

    @property
    def Var(self) -> Union[float, None]:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: number of degrees of freedom > 4
            None: number of degrees of freedom is in the interval (0, 4]

        Version 1.0.0.0
        """
        Degree = self.Degree
        if Degree > 4:
            Result = (2 / (Degree - 4)) / math.pow(Degree - 2, 2)
        else:
            Result = None
        return Result
    
    @property
    def Sigma(self) -> Union[float, None]:
        """
        Getter property for the standard deviation of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: number of degrees of freedom > 4
            None: number of degrees of freedom is in the interval (0, 4]

        Version 1.0.0.0
        """
        Degree = self.Degree
        if Degree > 4:
            Result = math.sqrt(2 / (Degree - 4)) / (Degree - 2)
        else:
            Result = None
        return Result

    @property
    def Skew(self) -> Union[float, None]:
        """
        Getter property for the skewness of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: number of degrees of freedom > 6
            None: number of degrees of freedom is in the interval (0, 6]

        Version 1.0.0.0
        """
        Degree = self.Degree
        if Degree > 6:
            Result = 4.0 * math.sqrt(2 * (Degree - 4)) / (Degree - 6)
        else:
            Result = None
        return Result
    
    @property
    def Kurt(self) -> Union[float, None]:
        """
        Getter property for the excess kurtosis of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: number of degrees of freedom > 6
            None: number of degrees of freedom is in the interval (0, 6]

        Version 1.0.0.0
        """
        Degree = self.Degree
        if Degree > 8:
            Result = 12.0 * (5 * Degree - 22) / ((Degree - 6) * (Degree - 8))
        else:
            Result = None
        return Result

class ScaledInverseChiSquared(InverseChiSquared):
    """
    Implementation of the scaled inverse chi-squared distribution. Must be
    instantiated with two positive real number arguments: degree of freedom and
    scale.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float > 0
        Max: (read-only) float = math.inf
        Mean: (read-only) float > 0 OR None
        Median: (read-only) float > 0
        Q1: (read-only) float > 0
        Q2: (read-only) float > 0
        Var: (read-only) float > 0 OR None
        Sigma: (read-only) float > 0 OR None
        Skew: (read-only) float > 0 OR None
        Kurt: (read-only) float > 0 OR None
        Degree: float > 0 OR int > 0
        Scale: float > 0 OR int > 0
    
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
            None -> float > 0
    
    Version 1.0.0.0
    """

    #class 'private' fields
    
    _Min: ClassVar[sf.TReal] = 2 * sys.float_info.min

    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int > 0 OR float > 0 -> float >= 0
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        Scale = self.Scale
        z = 0.5 * Scale * Degree / x
        if z > 300:
            Result = 0.0
        else:
            Temp = self._Cached['Factor'] - (0.5 * Degree + 1) * math.log(x) - z
            Result = math.exp(Temp)
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        Scale = self.Scale
        Result = sf.upper_gamma_reg(0.5 * Degree, 0.5 * Scale * Degree / x)
        return Result

    #special methods
    
    def __init__(self, Degree: sf.TReal, Scale: sf.TReal) -> None:
        """
        Initialization. Sets the parameter of the distribution.
        
        Signature:
            int > 0 OR float > 0, int > 0 OR float > 0 -> None
        
        Args:
            Degree: int > 0 OR float > 0; the degree of frredom parameter of the
                distribution
            Scale: int > 0 OR float > 0; the scale parameter of the distribution

        Raises:
            UT_TypeError: the passed value is not a real number
            UT_ValueError: the passed value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Degree, (int, float)):
            raise UT_TypeError(Degree, (int, float), SkipFrames = 1)
        if Degree <= 0:
            raise UT_ValueError(Degree, '> 0 - degree of freedom parameter',
                                                                SkipFrames = 1)
        if not isinstance(Scale, (int, float)):
            raise UT_TypeError(Scale, (int, float), SkipFrames = 1)
        if Scale <= 0:
            raise UT_ValueError(Scale, '> 0 - scale parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Degree'] = Degree
        self._Parameters['Scale'] = Scale
        self._Cached = dict()
        self._Cached['Median'] = None# cahed median value
        self._Cached['Q1'] = None #cached first quartile
        self._Cached['Q3'] = None #cached third quartile
        Temp = 0.5 * Degree * math.log(0.5 * Degree * Scale)
        self._Cached['Factor'] = Temp - math.lgamma(0.5 * Degree)
    
    #public properties
    
    @property
    def Degree(self) -> sf.TReal:
        """
        Property for the degree of freedom parameter of the distibution.
        
        Signature:
            None -> float > 0 OR int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Degree']
    
    @Degree.setter
    def Degree(self, Value: sf.TReal) -> None:
        """
        Setter method for the degree of freedom parameter of the distribution.
        
        Signature:
            float > 0 OR int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - degree parameter', SkipFrames = 1)
        self._Parameters['Degree'] = Value
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        Degree = Value
        Scale = self.Scale
        Temp = 0.5 * Degree * math.log(0.5 * Degree * Scale)
        self._Cached['Factor'] = Temp - math.lgamma(0.5 * Degree)
    
    @property
    def Scale(self) -> sf.TReal:
        """
        Property for the scale parameter of the distibution.
        
        Signature:
            None -> float > 0 OR int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Scale']
    
    @Scale.setter
    def Scale(self, Value: sf.TReal) -> None:
        """
        Setter method for the scale parameter of the distribution.
        
        Signature:
            float > 0 OR int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - scale parameter', SkipFrames = 1)
        self._Parameters['Scale'] = Value
        for Key in self._Cached.keys():
            self._Cached[Key] = None
        Degree = self.Degree
        Scale = Value
        Temp = 0.5 * Degree * math.log(0.5 * Degree * Scale)
        self._Cached['Factor'] = Temp - math.lgamma(0.5 * Degree)
    
    @property
    def Mean(self) -> Union[float, None]:
        """
        Getter property for the arithmetic mean of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: number of degrees of freedom > 2
            None: number of degrees of freedom is in the interval (0, 2]
        
        Version 1.0.0.0
        """
        Degree = self.Degree
        Scale = self.Scale
        if Degree > 2:
            Result = Degree * Scale / (Degree - 2)
        else:
            Result = None
        return Result

    @property
    def Var(self) -> Union[float, None]:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: number of degrees of freedom > 4
            None: number of degrees of freedom is in the interval (0, 4]

        Version 1.0.0.0
        """
        Degree = self.Degree
        Scale = self.Scale
        if Degree > 4:
            Result=2 * math.pow(Scale * Degree / (Degree - 2), 2) / (Degree - 4)
        else:
            Result = None
        return Result
    
    @property
    def Sigma(self) -> Union[float, None]:
        """
        Getter property for the standard deviation of the distribution.
        
        Signature:
            None -> float > 0 OR None
        
        Returns:
            float > 0: number of degrees of freedom > 4
            None: number of degrees of freedom is in the interval (0, 4]

        Version 1.0.0.0
        """
        Degree = self.Degree
        Scale = self.Scale
        if Degree > 4:
            Result = math.sqrt(2 / (Degree - 4)) * Degree * Scale / (Degree - 2)
        else:
            Result = None
        return Result

class Cauchy(BC):
    """
    Implementation of the Cauchy distribution. Must be instantiated with two
    real number arguments: location and scale, whereas the scale must be
    positive.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float = - math.inf
        Max: (read-only) float = math.inf
        Mean: (read-only) None
        Median: (read-only) float OR int
        Q1: (read-only) float OR int
        Q2: (read-only) float OR int
        Var: (read-only) None
        Sigma: (read-only) None
        Skew: (read-only) None
        Kurt: (read-only) None
        Location: float OR int
        Scale: float > 0 OR int > 0
    
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
            None -> float > 0
    
    Version 1.0.0.0
    """

    #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int > 0 OR float > 0 -> float >= 0
        
        Version 1.0.0.0
        """
        Location = self.Location
        Scale = self.Scale
        Temp = Scale * (1 + math.pow((x - Location) / Scale, 2)) * math.pi
        Result = 1 / Temp
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        Version 1.0.0.0
        """
        Location = self.Location
        Scale = self.Scale
        Result = 0.5 + math.atan((x - Location) / Scale) / math.pi
        return Result
    
    def _qf(self, x: float) -> sf.TReal:
        """
        The actual (internal) implementation of the ICDF / QF function.
        
        Signature:
           0 < float < 1 -> int OR float
        
        Version 1.0.0.0
        """
        Location = self.Location
        Scale = self.Scale
        Result = Location + Scale * math.tan(math.pi * (x - 0.5))
        return Result

    #special methods
    
    def __init__(self, Location: sf.TReal, Scale: sf.TReal) -> None:
        """
        Initialization. Sets the parameter of the distribution.
        
        Signature:
            int OR float, int > 0 OR float > 0 -> None
        
        Args:
            Location: int OR float ; the location parameter of the distribution
            Scale: int > 0 OR float > 0; the scale parameter of the distribution

        Raises:
            UT_TypeError: the passed value is not a real number
            UT_ValueError: the passed value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Location, (int, float)):
            raise UT_TypeError(Location, (int, float), SkipFrames = 1)
        if not isinstance(Scale, (int, float)):
            raise UT_TypeError(Scale, (int, float), SkipFrames = 1)
        if Scale <= 0:
            raise UT_ValueError(Scale, '> 0 - scale parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Location'] = Location
        self._Parameters['Scale'] = Scale
    
    #public properties
    
    @property
    def Location(self) -> sf.TReal:
        """
        Property for the location parameter of the distibution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self._Parameters['Location']
    
    @Location.setter
    def Location(self, Value: sf.TReal) -> None:
        """
        Setter method for the location parameter of the distribution.
        
        Signature:
            float OR int -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        self._Parameters['Location'] = Value
    
    @property
    def Scale(self) -> sf.TReal:
        """
        Property for the scale parameter of the distibution.
        
        Signature:
            None -> float > 0 OR int > 0
        
        Version 1.0.0.0
        """
        return self._Parameters['Scale']
    
    @Scale.setter
    def Scale(self, Value: sf.TReal) -> None:
        """
        Setter method for the scale parameter of the distribution.
        
        Signature:
            float > 0 OR int > 0 -> None
        
        Raises:
            UT_TypeError: passed value is not a real number
        
        Version 1.0.0.0
        """
        if not isinstance(Value, (int, float)):
            raise UT_TypeError(Value, (int, float), SkipFrames = 1)
        if Value <= 0:
            raise UT_ValueError(Value, '> 0 - scale parameter', SkipFrames = 1)
        self._Parameters['Scale'] = Value
    
    @property
    def Mean(self) -> None:
        """
        Getter property for the arithmetic mean of the distribution, which is
        not defined as a moment.
        
        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        return None
    
    @property
    def Median(self) -> sf.TReal:
        """
        Getter property for the median value of the distribution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self.Location
    
    @property
    def Q1(self) -> sf.TReal:
        """
        Getter property for the first quartile value of the distribution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self.Location - self.Scale
    
    @property
    def Q3(self) -> sf.TReal:
        """
        Getter property for the third quartile value of the distribution.
        
        Signature:
            None -> float OR int
        
        Version 1.0.0.0
        """
        return self.Location + self.Scale

    @property
    def Var(self) -> None:
        """
        Getter property for the variance of the distribution, which is not
        defined as a moment.
        
        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        return None
    
    @property
    def Sigma(self) -> None:
        """
        Getter property for the standard deviation of the distribution, which is
        not defined as a moment.
        
        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        return None
    
    @property
    def Skew(self) -> None:
        """
        Getter property for the skewdness of the distribution, which is not
        defined as a moment.
        
        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        return None
    
    @property
    def Kurt(self) -> None:
        """
        Getter property for the excess kurtosis of the distribution, which is
        not defined as a moment.
        
        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        return None

class Levy(Cauchy):
    """
    Implementation of the Cauchy distribution. Must be instantiated with two
    real number arguments: location and scale, whereas the scale must be
    positive.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float OR int
        Max: (read-only) float = math.inf
        Mean: (read-only) float = math.inf
        Median: (read-only) float
        Q1: (read-only) float
        Q2: (read-only) float
        Var: (read-only) float  = math.inf
        Sigma: (read-only) float  = math.inf
        Skew: (read-only) None
        Kurt: (read-only) None
        Location: float OR int
        Scale: float > 0 OR int > 0
    
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
            None -> float > 0
    
    Version 1.0.0.0
    """

     #private methods
    
    def _pdf(self, x: sf.TReal) -> float:
        """
        The actual implementation of the PDF function.
        
        Signature
            int > 0 OR float > 0 -> float >= 0
        
        Version 1.0.0.0
        """
        Location = self.Location
        Scale = self.Scale
        if x > Location:
            z = 0.5 * Scale / (x - Location)
            if z > 300:
                Result = 0.0
            else:
                Temp =  1.5 * math.log(z) - z
                Result = 2 * math.exp(Temp) / (Scale * math.sqrt(math.pi))
        else:
            Result = 0.0
        return Result
    
    def _cdf(self, x: sf.TReal) -> sf.TReal:
        """
        The actual implementation of the CDF function.
        
        Signature:
            int OR float -> 0 < float < 1
        
        Version 1.0.0.0
        """
        Location = self.Location
        Scale = self.Scale
        z = math.sqrt(0.5 * Scale / (x - Location))
        Result = 1 - math.erf(z)
        return Result
    
    def _qf(self, x: float) -> sf.TReal:
        """
        The actual (internal) implementation of the ICDF / QF function.
        
        Signature:
           0 < float < 1 -> int OR float
        
        Version 1.0.0.0
        """
        Location = self.Location
        Scale = self.Scale
        Temp = math.pow(sf.inv_erf(1 - x) ,2)
        Result = Location + 0.5 * Scale / Temp
        return Result

    @property
    def Min(self) -> int:
        """
        Property for the minimum supported value of the distribution.
        
        Signature:
            None -> int >= 0
        
        Version 1.0.0.0
        """
        return self.Location
    
    @property
    def Mean(self) -> float:
        """
        Getter property for the arithmetic mean of the distribution, which is
        infinite as a moment.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return math.inf
    
    @property
    def Median(self) -> float:
        """
        Getter property for the median value of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return self.Location + self.Scale * 2.198109338
    
    @property
    def Q1(self) -> float:
        """
        Getter property for the first quartile value of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return self.Location + self.Scale * 0.75568443
    
    @property
    def Q3(self) -> float:
        """
        Getter property for the third quartile value of the distribution.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return self.Location + self.Scale * 9.849204322

    @property
    def Var(self) -> float:
        """
        Getter property for the variance of the distribution, which is inifinite
        as a moment.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return math.inf
    
    @property
    def Sigma(self) -> float:
        """
        Getter property for the standard deviation of the distribution, which is
        infinite as a moment.
        
        Signature:
            None -> float
        
        Version 1.0.0.0
        """
        return math.inf
