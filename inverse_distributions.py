#usr/bin/python3
"""
Module statistics_lib.inverse_distributions

Classes:
    InverseGaussinan
    InverseGamma
    InverseChiSquared
    ScaledInverseChiSquared
    Cauchy
    Levy
"""

__version__= '1.0.0.0'
__date__ = '28-04-2022'
__status__ = 'Development'

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
        
        1.0.0.0
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
            UT_TypeError: any of the passed value is not a real number
            UT_ValueError: sigma value is not positive
        
        Version 1.0.0.0
        """
        if not isinstance(Mean, (int, float)):
            raise UT_TypeError(Mean, (int, float), SkipFrames = 1)
        if not isinstance(Shape, (int, float)):
            raise UT_TypeError(Shape, (int, float), SkipFrames = 1)
        if Mean <= 0:
            raise UT_ValueError(Shape, '> 0 - mean parameter', SkipFrames = 1)
        if Shape <= 0:
            raise UT_ValueError(Shape, '> 0 - sigma parameter', SkipFrames = 1)
        self._Parameters = dict()
        self._Parameters['Mean'] = Mean
        self._Parameters['Shape'] = Shape

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
    
    @property
    def Var(self) -> sf.TReal:
        """
        Getter property for the variance of the distribution.
        
        Signature:
            None -> float > 0 OR int > 0
        
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
        Mean: (read-only) float > 0 OR int > 0 OR None
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

class InverseChiSquared(BC):
    """
    Implementation of the inverse chi-squared distribution. Must be instantiated
    with a positive real number argument - degree of freedom.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float > 0
        Max: (read-only) float = math.inf
        Mean: (read-only) float > 0 OR int > 0 OR None
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

class ScaledInverseChiSquared(InverseChiSquared):
    """
    Implementation of the scaled inverse chi-squared distribution. Must be
    instantiated with two positive real number arguments: degree of freedom and
    scale.
    
    Properties:
        Name: (read-only) str
        Min: (read-only) float > 0
        Max: (read-only) float = math.inf
        Mean: (read-only) float > 0 OR int > 0 OR None
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
        Median: (read-only) float OR int
        Q1: (read-only) float OR int
        Q2: (read-only) float OR int
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
