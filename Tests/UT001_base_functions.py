#usr/bin/python3
"""
Module statistics_lib.Tests.UT001_base_functions

Set of unit tests on the module stastics_lib.base_functions. See the test plan /
report TE001_base_functions.md
"""


__version__= '1.0.0.0'
__date__ = '10-02-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import unittest
import random
import statistics
import math

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.base_functions as test_module

from phyqus_lib.base_classes import MeasuredValue

#globals

FLOAT_CHECK_PRECISION = 8 #digits after comma

DELTA_PRECISION = 0.0001 # 1E-4

#helper functions

def CheckSE(Data):
    """
    Calculates SE using statistics.pstdev() function.
    """
    return statistics.pstdev(Data) / math.sqrt(len(Data))

def CheckMoment2(Data):
    """
    Calculates the second non-central moment.
    """
    return sum(pow(Item, 2) for Item in Data) / len(Data)

def CheckFullSE(Means, Errors):
    """
    Calculates the total uncertainty of the mean.
    """
    Variance = statistics.pvariance(Means)
    MSSE = CheckMoment2(Errors)
    Length = len(Means)
    Result = math.sqrt((Variance + MSSE) /  Length)
    return Result

def CheckSkewP(Data):
    """
    Calculates the population skewness
    """
    Mean = statistics.mean(Data)
    Sigma = statistics.pstdev(Data)
    Length = len(Data)
    Sum = sum(pow((Item - Mean) / Sigma, 3) for Item in Data)
    Result = Sum / Length
    return Result

def CheckSkewS(Data):
    """
    Calculates the population skewness
    """
    Mean = statistics.mean(Data)
    Sigma = statistics.pstdev(Data)
    Length = len(Data)
    Sum = sum(pow((Item - Mean) / Sigma, 3) for Item in Data)
    Result = math.sqrt((Length - 1) / Length) * Sum / (Length - 2)
    return Result

def CheckKurtP(Data):
    """
    Calculates the population excess kurtosis
    """
    Mean = statistics.mean(Data)
    Sigma = statistics.pstdev(Data)
    Length = len(Data)
    Sum = sum(pow((Item - Mean) / Sigma, 4) for Item in Data)
    Result = Sum / Length - 3
    return Result

def CheckKurtS(Data):
    """
    Calculates the sample excess kurtosis
    """
    Mean = statistics.mean(Data)
    Sigma = statistics.pstdev(Data)
    Length = len(Data)
    Sum = sum(pow((Item - Mean) / Sigma, 4) for Item in Data)
    Kurt = Sum / Length
    Corr1 = (Length * Length - 1) / ((Length - 2) * (Length - 3))
    Corr2 = ((Length - 1) * (Length - 1)) / ((Length - 2) * (Length - 3))
    Result = Corr1 * Kurt - 3 * Corr2
    return Result

def CheckCovariance(DataX, DataY):
    """
    Calculates the covariance of two sequences
    """
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 10:
        Result = statistics.correlation(DataX, DataY)
    else:
        MeanX = statistics.mean(DataX)
        MeanY = statistics.mean(DataY)
        Length = len(DataX)
        Sum = sum((Item - MeanX) * (DataY[Index] - MeanY)
                                            for Index, Item in enumerate(DataX))
        Result = Sum / Length
    return Result

def CheckCorrelation(DataX, DataY):
    """
    Calculates the Pearson correlation of two sequences
    """
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 10:
        Result = statistics.correlation(DataX, DataY)
    else:
        Cov = CheckCovariance(DataX, DataY)
        SigmaX = statistics.pstdev(DataX)
        SigmaY = statistics.pstdev(DataY)
        Result = Cov / (SigmaX * SigmaY)
    return Result

#classes

#+ test cases

class Test_Basis(unittest.TestCase):
    """
    Base class implementing the common testing for all functions (1D statistics)
    and the input data preparation.

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module._ExtractMeans)
        cls.CheckFunction = staticmethod(statistics.mean)
        cls.AllInt = [random.randint(-100, 100)
                                    for _ in range(random.randrange(5, 100))]
        cls.AllFloat = [random.uniform(-10.0, 10.0)
                                    for _ in range(random.randrange(5, 100))]
        cls.Mixed = list()
        for _ in range(random.randrange(10, 100)):
            Temp = random.random()
            if Temp >= 0.5:
                cls.Mixed.append(random.uniform(-10.0, 10.0))
            else:
                cls.Mixed.append(random.randint(-100, 100))
        MaxLength = max(len(cls.AllInt), len(cls.AllFloat), len(cls.Mixed))
        cls.Errors = [random.uniform(0.0, 3.0) for _ in range(MaxLength)]
        cls.IntErr = [MeasuredValue(Value, cls.Errors[i])
                                        for i, Value in enumerate(cls.AllInt)]
        cls.FloatErr = [MeasuredValue(Value, cls.Errors[i])
                                        for i, Value in enumerate(cls.AllFloat)]
        cls.MixedErr = [MeasuredValue(Value, cls.Errors[i])
                                        for i, Value in enumerate(cls.Mixed)]
        cls.TotalMixed = list()
        for Item in cls.MixedErr:
            Temp = random.random()
            if Temp >= 0.6:
                cls.TotalMixed.append(Item)
            else:
                cls.TotalMixed.append(Item.Value)
        cls.BadCases = [1, 2.0, 'asd', [1, '1'], ('b', 2.0), int, float, list,
                        tuple, {1:1, 2:2}, dict]
    
    def test_TypeError(self) -> None:
        """
        Checks that sub-class of TypeError is raised with improper input data
        type.

        Implements test TEST-T-101.
        Covers the requirement REQ-AWM-100.
        """
        for Temp in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestFunction(Temp)

    def test_ValueError(self) -> None:
        """
        Checks that sub-class of ValueError is raised with proper input data
        type but wrong value.

        Implements test TEST-T-102.
        Covers the requirement REQ-AWM-101.
        """
        with self.assertRaises(ValueError):
            self.TestFunction([]) #empty sequence

    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-100.
        Covers the requirement REQ-FUN-101.
        """
        for BaseInput in [self.AllInt, self.AllFloat, self.Mixed]:
            TestResult = self.TestFunction(BaseInput)
            self.assertIsInstance(TestResult, (int, float))
            TestCheck = self.CheckFunction(BaseInput)
            self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(BaseInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
        for TestInput, BaseInput in ((self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
            TestResult = self.TestFunction(TestInput)
            self.assertIsInstance(TestResult, (int, float))
            TestCheck = self.CheckFunction(BaseInput)
            self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(TestInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)

class Test_GetMean(Test_Basis):
    """
    Unit-tests of the function GetMean().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetMean)
    
    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequence of a single value.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for Item in [2, 3.4, MeasuredValue(3.2, 0.1)]:
            TestResult = self.TestFunction([Item])
            self.assertIsInstance(TestResult, (int, float))
            if isinstance(Item, (int, float)):
                self.assertAlmostEqual(TestResult, Item,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertAlmostEqual(TestResult, Item.Value,
                                                places = FLOAT_CHECK_PRECISION)

class Test_GetVarianceP(Test_Basis):
    """
    Unit-tests of the function GetVarianceP().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetVarianceP)
        cls.CheckFunction = staticmethod(statistics.pvariance)

    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequence of a single value.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for Item in [2, 3.4, MeasuredValue(3.2, 0.1)]:
            TestResult = self.TestFunction([Item])
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)

class Test_GetStdevP(Test_GetVarianceP):
    """
    Unit-tests of the function GetStevP().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetStdevP)
        cls.CheckFunction = staticmethod(statistics.pstdev)

class Test_GetVarianceS(Test_Basis):
    """
    Unit-tests of the function GetVarianceS().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetVarianceS)
        cls.CheckFunction = staticmethod(statistics.variance)

    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequence of a single value - sub-class of
        ValueError should be raised.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for Item in [2, 3.4, MeasuredValue(3.2, 0.1)]:
            with self.assertRaises(ValueError):
                self.TestFunction([Item])

class Test_GetStdevS(Test_GetVarianceS):
    """
    Unit-tests of the function GetMean().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetStdevS)
        cls.CheckFunction = staticmethod(statistics.stdev)

class Test_GetSE(Test_GetVarianceP):
    """
    Unit-tests of the function GetSE().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetSE)
        cls.CheckFunction = staticmethod(CheckSE)

class Test_GetMeanSqrSE(Test_Basis):
    """
    Unit-tests of the function GetMeanSqrSE().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetMeanSqrSE)
        cls.CheckFunction = staticmethod(CheckMoment2)
    
    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-100.
        Covers the requirement REQ-FUN-101.
        """
        for BaseInput in [self.AllInt, self.AllFloat, self.Mixed]:
            TestResult = self.TestFunction(BaseInput)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0, 
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(BaseInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0, 
                                                places = FLOAT_CHECK_PRECISION)
        for TestInput in (self.IntErr, self.FloatErr, self.MixedErr):
            TestResult = self.TestFunction(TestInput)
            self.assertIsInstance(TestResult, (int, float))
            BaseInput = [Item.SE for Item in TestInput]
            TestCheck = self.CheckFunction(BaseInput)
            self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(TestInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
        TestInput = self.TotalMixed
        BaseInput = list()
        for Item in TestInput:
            if hasattr(Item, 'SE'):
                BaseInput.append(Item.SE)
            else:
                BaseInput.append(0)
        TestCheck = self.CheckFunction(BaseInput)
        TestResult = self.TestFunction(TestInput)
        self.assertIsInstance(TestResult, (int, float))
        self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
        TestResult = self.TestFunction(tuple(TestInput))
        self.assertIsInstance(TestResult, (int, float))
        self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)

class Test_GetFullSE(Test_Basis):
    """
    Unit-tests of the function GetFullSE().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetFullSE)
        cls.CheckFunction = staticmethod(CheckFullSE)
    
    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-100.
        Covers the requirement REQ-FUN-101.
        """
        for TestInput in [self.AllInt, self.AllFloat, self.Mixed]:
            TestResult = self.TestFunction(TestInput)
            self.assertIsInstance(TestResult, (int, float))
            BaseInput = [0 for _ in TestInput]
            TestCheck = self.CheckFunction(TestInput, BaseInput)
            self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(TestInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
        for TestInput, Means in ((self.IntErr, self.AllInt),
                                    (self.FloatErr, self.AllFloat),
                                     (self.MixedErr, self.Mixed)):
            TestResult = self.TestFunction(TestInput)
            self.assertIsInstance(TestResult, (int, float))
            BaseInput = [Item.SE for Item in TestInput]
            TestCheck = self.CheckFunction(Means, BaseInput)
            self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(TestInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
        TestInput = self.TotalMixed
        BaseInput = list()
        for Item in TestInput:
            if hasattr(Item, 'SE'):
                BaseInput.append(Item.SE)
            else:
                BaseInput.append(0)
        TestCheck = self.CheckFunction(self.Mixed, BaseInput)
        TestResult = self.TestFunction(TestInput)
        self.assertIsInstance(TestResult, (int, float))
        self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
        TestResult = self.TestFunction(tuple(TestInput))
        self.assertIsInstance(TestResult, (int, float))
        self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)

class Test_GetSkewnessP(Test_GetVarianceP):
    """
    Unit-tests of the function GetSkewnessP().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetSkewnessP)
        cls.CheckFunction = staticmethod(CheckSkewP)

class Test_GetSkewnessS(Test_Basis):
    """
    Unit-tests of the function GetSkewnessS().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetSkewnessS)
        cls.CheckFunction = staticmethod(CheckSkewS)
    
    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequence of one or two values - sub-class of
        ValueError should be raised.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for Item in [2, 3.4, MeasuredValue(3.2, 0.1)]:
            with self.assertRaises(ValueError):
                self.TestFunction([Item])
            with self.assertRaises(ValueError):
                self.TestFunction([Item, Item])

class Test_GetKurtosisP(Test_Basis):
    """
    Unit-tests of the function GetKurtosisP().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetKurtosisP)
        cls.CheckFunction = staticmethod(CheckKurtP)
    
    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequence of a single value.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for Item in [2, 3.4, MeasuredValue(3.2, 0.1)]:
            TestResult = self.TestFunction([Item])
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, -3,
                                                places = FLOAT_CHECK_PRECISION)

class Test_GetKurtosisS(Test_Basis):
    """
    Unit-tests of the function GetKurtosisS().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetKurtosisS)
        cls.CheckFunction = staticmethod(CheckKurtS)
    
    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequence of one, two or three values -
        sub-class of ValueError should be raised.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for Item in [2, 3.4, MeasuredValue(3.2, 0.1)]:
            with self.assertRaises(ValueError):
                self.TestFunction([Item])
            with self.assertRaises(ValueError):
                self.TestFunction([Item, Item])
            with self.assertRaises(ValueError):
                self.TestFunction([Item, Item, Item])

class Test_GetMoment(Test_Basis):
    """
    Unit-tests of the function GetMoment().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetMoment)
    
    def test_TypeError(self) -> None:
        """
        Checks that sub-class of TypeError is raised with improper input data
        type.

        Implements test TEST-T-101.
        Covers the requirement REQ-AWM-100.
        """
        for Temp in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, random.randint(1, 6))
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, random.randint(1, 6), IsCentral = True)
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, random.randint(1, 6), IsCentral = False)
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, random.randint(1, 6),
                                                            IsNormalized = True)
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, random.randint(1, 6), IsCentral = True,
                                                            IsNormalized = True)
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, random.randint(1, 6), IsCentral = False,
                                                            IsNormalized = True)
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, random.randint(1, 6),
                                                        IsNormalized = False)
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, random.randint(1, 6), IsCentral = True,
                                                        IsNormalized = False)
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, random.randint(1, 6), IsCentral = False,
                                                        IsNormalized = False)
        for Power in [1.0, '1', [1], (1, 2), MeasuredValue(1), {1:1}]:
            with self.assertRaises(TypeError):
                self.TestFunction(self.AllInt, Power)
            with self.assertRaises(TypeError):
                self.TestFunction(self.AllInt, Power, IsCentral = True)
            with self.assertRaises(TypeError):
                self.TestFunction(self.AllInt, Power, IsCentral = False)
            with self.assertRaises(TypeError):
                self.TestFunction(self.AllInt, Power, IsNormalized = True)
            with self.assertRaises(TypeError):
                self.TestFunction(self.AllInt, Power, IsCentral = True,
                                                            IsNormalized = True)
            with self.assertRaises(TypeError):
                self.TestFunction(self.AllInt, Power, IsCentral = False,
                                                            IsNormalized = True)
            with self.assertRaises(TypeError):
                self.TestFunction(self.AllInt, Power, IsNormalized = False)
            with self.assertRaises(TypeError):
                self.TestFunction(self.AllInt, Power, IsCentral = True,
                                                        IsNormalized = False)
            with self.assertRaises(TypeError):
                self.TestFunction(self.AllInt, Power, IsCentral = False,
                                                        IsNormalized = False)

    def test_ValueError(self) -> None:
        """
        Checks that sub-class of ValueError is raised with proper input data
        type but wrong value.

        Implements test TEST-T-102.
        Covers the requirement REQ-AWM-101.
        """
        with self.assertRaises(ValueError):
            self.TestFunction([], random.randint(1, 6)) #empty sequence
        for FlagA in [True, False]:
            for FlagB in [True, False]:
                with self.assertRaises(ValueError):
                    self.TestFunction([], random.randint(1, 6),
                                        IsCentral = FlagA, IsNormalized = FlagB)
        for Power in range(-6, 1): #negative powers
            with self.assertRaises(ValueError):
                self.TestFunction(self.AllInt, Power)
            for FlagA in [True, False]:
                for FlagB in [True, False]:
                    with self.assertRaises(ValueError):
                        self.TestFunction(self.AllInt, Power,
                                        IsCentral = FlagA, IsNormalized = FlagB)
        for Power in range(1, 6): #non-central normalized constant sequence
            with self.assertRaises(ValueError):
                self.TestFunction([1, 1, 1], Power, IsCentral = False,
                                                            IsNormalized = True)
    
    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-100.
        Covers the requirement REQ-FUN-101.
        """
        for Power in range(1, 6):
            for TestInput, BaseInput in ((self.AllInt, self.AllInt),
                                        (self.AllFloat, self.AllFloat),
                                        (self.Mixed, self.Mixed),
                                        (self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
                Length = len(BaseInput)
                Sigma = statistics.pstdev(BaseInput)
                Mean = statistics.mean(BaseInput)
                #non-central not normalized
                TestResult = self.TestFunction(TestInput, Power)
                self.assertIsInstance(TestResult, (int, float))
                TestCheck = sum(pow(Item, Power) for Item in BaseInput) / Length
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                        delta = DELTA_PRECISION)
                TestResult = self.TestFunction(tuple(TestInput), Power)
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                        delta = DELTA_PRECISION)
                #non-central normalized
                TestResult = self.TestFunction(TestInput, Power,
                                                            IsNormalized = True)
                self.assertIsInstance(TestResult, (int, float))
                TestCheck = sum(pow(Item / Sigma, Power)
                                                for Item in BaseInput) / Length
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = self.TestFunction(tuple(TestInput), Power,
                                                            IsNormalized = True)
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
                #central not normalized
                TestResult = self.TestFunction(TestInput, Power,
                                                            IsCentral = True)
                self.assertIsInstance(TestResult, (int, float))
                TestCheck = sum(pow(Item - Mean, Power)
                                                for Item in BaseInput) / Length
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                        delta = DELTA_PRECISION)
                TestResult = self.TestFunction(tuple(TestInput), Power,
                                                            IsCentral = True)
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                        delta = DELTA_PRECISION)
                #central normalized
                TestResult = self.TestFunction(TestInput, Power,
                                        IsCentral = True, IsNormalized = True)
                self.assertIsInstance(TestResult, (int, float))
                TestCheck = sum(pow((Item - Mean) / Sigma, Power)
                                                for Item in BaseInput) / Length
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = self.TestFunction(tuple(TestInput), Power,
                                        IsCentral = True, IsNormalized = True)
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
    
    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequence of a single value and constant values
        sequences.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for Power in range(1, 6):
            for Item in [2, 3.4, MeasuredValue(3.2, 0.1)]:
                #non-central not normalized
                TestResult = self.TestFunction([Item], Power)
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, pow(Item, Power),
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = self.TestFunction([Item], Power, IsCentral = False,
                                                        IsNormalized = False)
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, pow(Item, Power),
                                                places = FLOAT_CHECK_PRECISION)
                #central not normalized
                TestResult = self.TestFunction([Item], Power, IsCentral = True)
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = self.TestFunction([Item], Power, IsCentral = True,
                                                        IsNormalized = False)
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
                #central normalized
                TestResult = self.TestFunction([Item], Power, IsCentral = True,
                                                            IsNormalized = True)
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
        for _ in range(10):
            Const = random.random() + random.randint(-3, 4)
            Length = random.randint(2, 10)
            Array1 = [Const for _ in range(Length)]
            Power = random.randint(1, 6)
            TestCheck = pow(Const, Power)
            #non-central not normalized
            TestResult = self.TestFunction(Array1, Power)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(Array1, Power, IsCentral = False,
                                                        IsNormalized = False)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
            #central not normalized
            TestResult = self.TestFunction(Array1, Power, IsCentral = True)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(Array1, Power, IsCentral = True,
                                                        IsNormalized = False)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            #central normalized
            TestResult = self.TestFunction(Array1, Power, IsCentral = True,
                                                            IsNormalized = True)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)

class Test_GetCovariance(Test_Basis):
    """
    Unit-tests of the function GetCovariance().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetCovariance)
        cls.CheckFunction = staticmethod(CheckCovariance)
    
    def test_TypeError(self) -> None:
        """
        Checks that sub-class of TypeError is raised with improper input data
        type.

        Implements test TEST-T-101.
        Covers the requirement REQ-AWM-100.
        """
        for Temp in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, [1, 1])
            with self.assertRaises(TypeError):
                self.TestFunction([1, 1], Temp)
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, Temp)
    
    def test_ValueError(self) -> None:
        """
        Checks that sub-class of ValueError is raised with proper input data
        type but wrong value.

        Implements test TEST-T-102.
        Covers the requirement REQ-AWM-101.
        """
        with self.assertRaises(ValueError):
            self.TestFunction([], [1, 1])
        with self.assertRaises(ValueError):
            self.TestFunction([1, 1], [])
        with self.assertRaises(ValueError):
            self.TestFunction([], [])
        for _ in range(10):
            Array1 = [random.randint(1, 5) for _ in range(random.randint(1, 5))]
            Array2 = list(Array1)
            Array2.extend([random.randint(1, 5)
                                        for _ in range(random.randint(1, 5))])
            with self.assertRaises(ValueError):
                self.TestFunction(Array1, Array2)
            with self.assertRaises(ValueError):
                self.TestFunction(Array2, Array1)
    
    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-100.
        Covers the requirement REQ-FUN-101.
        """
        for TestInputX, BaseInputX in ((self.AllInt, self.AllInt),
                                        (self.AllFloat, self.AllFloat),
                                        (self.Mixed, self.Mixed),
                                        (self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
            for TestInputY, BaseInputY in ((self.AllInt, self.AllInt),
                                        (self.AllFloat, self.AllFloat),
                                        (self.Mixed, self.Mixed),
                                        (self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
                MinLength = min(len(BaseInputX), len(BaseInputY))
                CheckResult = self.CheckFunction(BaseInputX[:MinLength],
                                                        BaseInputY[:MinLength])
                TestResult = self.TestFunction(TestInputX[:MinLength],
                                                        TestInputY[:MinLength])
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, CheckResult,
                                                places= FLOAT_CHECK_PRECISION)
                TestResult = self.TestFunction(tuple(TestInputX[:MinLength]),
                                                tuple(TestInputY[:MinLength]))
                self.assertIsInstance(TestResult, (int, float))
                self.assertAlmostEqual(TestResult, CheckResult,
                                                places= FLOAT_CHECK_PRECISION)
    
    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequences of a single value and 1 or both
        sequences being constant.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for _ in range(10):
            Value = random.random()
            self.assertEqual(self.TestFunction([Value], [Value]), 0)
            Length = random.randint(2, 100)
            Value1 = [1 for _ in range(Length)]
            Value2 = [random.random() for _ in range(Length)]
            self.assertEqual(self.TestFunction(Value1, Value2), 0)
            self.assertEqual(self.TestFunction(Value2, Value1), 0)
            self.assertEqual(self.TestFunction(Value1, Value1), 0)

class Test_GetPearsonR(Test_GetCovariance):
    """
    Unit-tests of the function GetPearsonR().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetPearsonR)
        cls.CheckFunction = staticmethod(CheckCorrelation)
    
    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequences of a single value and 1 or both
        sequences being constant.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for _ in range(10):
            Value = random.random()
            self.assertEqual(self.TestFunction([Value], [Value]), 1)
            Length = random.randint(2, 100)
            Value1 = [1 for _ in range(Length)]
            Value2 = [random.random() for _ in range(Length)]
            self.assertEqual(self.TestFunction(Value1, Value2), 0)
            self.assertEqual(self.TestFunction(Value2, Value1), 0)
            self.assertEqual(self.TestFunction(Value1, Value1), 1)

class Test_GetMoment2(Test_Basis):
    """
    Unit-tests of the function GetMoment2().

    Implements tests: TEST-T-100, TEST-T-101, TEST-T-102
    Covers the requirements REQ-FUN-101, REQ-AWM-100 and REQ-AWM-101.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetMoment2)
    
    def test_TypeError(self) -> None:
        """
        Checks that sub-class of TypeError is raised with improper input data
        type.

        Implements test TEST-T-101.
        Covers the requirement REQ-AWM-100.
        """
        for PowerX in range(1, 4):
            for PowerY in range(1, 4):
                for Temp in self.BadCases:
                    with self.assertRaises(TypeError):
                        self.TestFunction(Temp, [1, 1, 1], PowerX, PowerY)
                    with self.assertRaises(TypeError):
                        self.TestFunction([1, 1, 1], Temp, PowerX, PowerY)
                    with self.assertRaises(TypeError):
                        self.TestFunction(Temp, Temp, PowerX, PowerY)
                    for FlagA in [True, False]:
                        for FlagB in [True, False]:
                            with self.assertRaises(TypeError):
                                self.TestFunction(Temp, [1, 1, 1], PowerX,
                                                    PowerY, IsCentral = FlagA,
                                                        IsNormalized = FlagB)
                            with self.assertRaises(TypeError):
                                self.TestFunction([1, 1, 1], Temp, PowerX,
                                                    PowerY, IsCentral = FlagA,
                                                        IsNormalized = FlagB)
                            with self.assertRaises(TypeError):
                                self.TestFunction(Temp, Temp, PowerX,
                                                    PowerY, IsCentral = FlagA,
                                                        IsNormalized = FlagB)
        for PowerX in [1.0, '1', [1], (1, 2), MeasuredValue(1), {1:1}]:
            for PowerY in range(1, 4):
                with self.assertRaises(TypeError):
                    self.TestFunction(self.AllInt, self.AllInt, PowerX, PowerY)
                with self.assertRaises(TypeError):
                    self.TestFunction(self.AllInt, self.AllInt, PowerY, PowerX)
                with self.assertRaises(TypeError):
                    self.TestFunction(self.AllInt, self.AllInt, PowerX, PowerX)
                for FlagA in [True, False]:
                    for FlagB in [True, False]:
                        with self.assertRaises(TypeError):
                            self.TestFunction(self.AllInt, self.AllInt, PowerX,
                                                    PowerY, IsCentral = FlagA,
                                                        IsNormalized = FlagB)
                        with self.assertRaises(TypeError):
                            self.TestFunction(self.AllInt, self.AllInt, PowerY,
                                                    PowerX, IsCentral = FlagA,
                                                        IsNormalized = FlagB)
                        with self.assertRaises(TypeError):
                            self.TestFunction(self.AllInt, self.AllInt, PowerX,
                                                    PowerX, IsCentral = FlagA,
                                                        IsNormalized = FlagB)
    
    def test_ValueError(self) -> None:
        """
        Checks that sub-class of ValueError is raised with proper input data
        type but wrong value.

        Implements test TEST-T-102.
        Covers the requirement REQ-AWM-101.
        """
        for PowerX in range(1, 4):
            for PowerY in range(1, 4):
                #empty sequences
                with self.assertRaises(ValueError):
                    self.TestFunction(self.AllInt, [], PowerX, PowerY)
                with self.assertRaises(ValueError):
                    self.TestFunction([], self.AllInt, PowerX, PowerY)
                with self.assertRaises(ValueError):
                    self.TestFunction([], self.AllInt, PowerX, PowerY)
                for FlagA in [True, False]:
                    for FlagB in [True, False]:
                        with self.assertRaises(ValueError):
                            self.TestFunction(self.AllInt, [], PowerX, PowerY,
                                        IsCentral = FlagA, IsNormalized = FlagB)
                        with self.assertRaises(ValueError):
                            self.TestFunction([], self.AllInt, PowerX, PowerY,
                                        IsCentral = FlagA, IsNormalized = FlagB)
                        with self.assertRaises(ValueError):
                            self.TestFunction([], self.AllInt, PowerX, PowerY,
                                        IsCentral = FlagA, IsNormalized = FlagB)
                for _ in range(5): #unequal sequences
                    Array1 = [random.randint(1, 5)
                                        for _ in range(random.randint(1, 5))]
                    Array2 = list(Array1)
                    Array2.extend([random.randint(1, 5)
                                        for _ in range(random.randint(1, 5))])
                    with self.assertRaises(ValueError):
                        self.TestFunction(Array1, Array2, PowerX, PowerY)
                    with self.assertRaises(ValueError):
                        self.TestFunction(Array2, Array1, PowerX, PowerY)
                    for FlagA in [True, False]:
                        for FlagB in [True, False]:
                            with self.assertRaises(ValueError):
                                self.TestFunction(Array1, Array2, PowerX,
                                                    PowerY, IsCentral = FlagA,
                                                        IsNormalized = FlagB)
                            with self.assertRaises(ValueError):
                                self.TestFunction(Array2, Array1, PowerX,
                                                    PowerY, IsCentral = FlagA,
                                                        IsNormalized = FlagB)
        for PowerX in range(-8, 1): #negative powers
            with self.assertRaises(ValueError):
                self.TestFunction(self.AllInt, self.AllInt, PowerX,
                                                        random.randint(1, 5))
            with self.assertRaises(ValueError):
                self.TestFunction(self.AllInt, self.AllInt,
                                                random.randint(1, 5), PowerX)
            with self.assertRaises(ValueError):
                self.TestFunction(self.AllInt, self.AllInt, PowerX, PowerX)
            for FlagA in [True, False]:
                for FlagB in [True, False]:
                    with self.assertRaises(ValueError):
                        self.TestFunction(self.AllInt, self.AllInt, PowerX,
                                                        random.randint(1, 5))
                    with self.assertRaises(ValueError):
                        self.TestFunction(self.AllInt, self.AllInt,
                                                random.randint(1, 5), PowerX)
                    with self.assertRaises(ValueError):
                        self.TestFunction(self.AllInt, self.AllInt, PowerX,
                                                                        PowerX)
        Array1 = [1 for _ in range(len(self.AllInt))]
        for PowerX in range(1, 4): #Non-central normalized of constant sequence
            for PowerY in range(1, 4):
                with self.assertRaises(ValueError):
                    self.TestFunction(Array1, self.AllInt, PowerX, PowerY,
                                        IsCentral = False, IsNormalized = True)
                with self.assertRaises(ValueError):
                    self.TestFunction(self.AllInt, Array1, PowerX, PowerY,
                                        IsCentral = False, IsNormalized = True)
                with self.assertRaises(ValueError):
                    self.TestFunction(Array1, Array1, PowerX, PowerY,
                                        IsCentral = False, IsNormalized = True)
    
    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-100.
        Covers the requirement REQ-FUN-101.
        """
        for PowerX in range(1, 4):
            for PowerY in range(1, 4):
                for TestInputX, BaseInputX in ((self.AllInt, self.AllInt),
                                                (self.AllFloat, self.AllFloat),
                                                (self.Mixed, self.Mixed),
                                                (self.IntErr, self.AllInt),
                                                (self.FloatErr, self.AllFloat),
                                                (self.MixedErr, self.Mixed),
                                                (self.TotalMixed, self.Mixed)):
                    for TestInputY, BaseInputY in ((self.AllInt, self.AllInt),
                                                (self.AllFloat, self.AllFloat),
                                                (self.Mixed, self.Mixed),
                                                (self.IntErr, self.AllInt),
                                                (self.FloatErr, self.AllFloat),
                                                (self.MixedErr, self.Mixed),
                                                (self.TotalMixed, self.Mixed)):
                        Length = min(len(BaseInputX), len(BaseInputY))
                        SigmaX = statistics.pstdev(BaseInputX[:Length])
                        MeanX = statistics.mean(BaseInputX[:Length])
                        SigmaY = statistics.pstdev(BaseInputY[:Length])
                        MeanY = statistics.mean(BaseInputY[:Length])
                        #non-central not normalized
                        TestResult = self.TestFunction(TestInputX[:Length],
                                            TestInputY[:Length], PowerX, PowerY)
                        self.assertIsInstance(TestResult, (int, float))
                        TestCheck = sum(
                                pow(Item, PowerX) * pow(BaseInputY[i], PowerY)
                                    for i,Item in enumerate(BaseInputX[:Length])
                                                                    ) / Length
                        self.assertAlmostEqual(TestResult, TestCheck, 
                                                        delta = DELTA_PRECISION)
                        TestResult=self.TestFunction(tuple(TestInputX[:Length]),
                                                    tuple(TestInputY[:Length]),
                                                                PowerX, PowerY)
                        self.assertIsInstance(TestResult, (int, float))
                        self.assertAlmostEqual(TestResult, TestCheck, 
                                                        delta = DELTA_PRECISION)
                        #non-central normalized
                        TestResult = self.TestFunction(TestInputX[:Length],
                                            TestInputY[:Length], PowerX, PowerY,
                                                            IsNormalized = True)
                        self.assertIsInstance(TestResult, (int, float))
                        TestCheck = sum(
                                pow(Item / SigmaX, PowerX) * pow(
                                        BaseInputY[i] / SigmaY, PowerY)
                                    for i,Item in enumerate(BaseInputX[:Length])
                                                                    ) / Length
                        self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
                        TestResult=self.TestFunction(tuple(TestInputX[:Length]),
                                                    tuple(TestInputY[:Length]),
                                                        PowerX, PowerY,
                                                            IsNormalized = True)
                        self.assertIsInstance(TestResult, (int, float))
                        self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
                        #central not normalized
                        TestResult = self.TestFunction(TestInputX[:Length],
                                            TestInputY[:Length], PowerX, PowerY,
                                                            IsCentral = True)
                        self.assertIsInstance(TestResult, (int, float))
                        TestCheck = sum(
                                    pow(Item - MeanX, PowerX) * pow(
                                        BaseInputY[i] - MeanY, PowerY)
                                    for i,Item in enumerate(BaseInputX[:Length])
                                                                    ) / Length
                        self.assertAlmostEqual(TestResult, TestCheck, 
                                                        delta = DELTA_PRECISION)
                        TestResult=self.TestFunction(tuple(TestInputX[:Length]),
                                                    tuple(TestInputY[:Length]),
                                                            PowerX, PowerY,
                                                            IsCentral = True)
                        self.assertIsInstance(TestResult, (int, float))
                        self.assertAlmostEqual(TestResult, TestCheck, 
                                                        delta = DELTA_PRECISION)
                        #central normalized
                        TestResult = self.TestFunction(TestInputX[:Length],
                                            TestInputY[:Length], PowerX, PowerY,
                                        IsCentral = True, IsNormalized = True)
                        self.assertIsInstance(TestResult, (int, float))
                        TestCheck = sum(
                                pow((Item - MeanX) / SigmaX, PowerX) * pow(
                                    (BaseInputY[i] - MeanY) / SigmaY, PowerY)
                                    for i,Item in enumerate(BaseInputX[:Length])
                                                                    ) / Length
                        self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
                        TestResult=self.TestFunction(tuple(TestInputX[:Length]),
                                                    tuple(TestInputY[:Length]),
                                                        PowerX, PowerY,
                                        IsCentral = True, IsNormalized = True)
                        self.assertIsInstance(TestResult, (int, float))
                        self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
    
    def test_EdgeCase(self) -> None:
        """
        Checks the edge case of a sequence of a single value and constant values
        sequences.

        Implements tests: TEST-T-100.
        Covers the requirements REQ-FUN-101.
        """
        for PowerX in range(1, 4):
            for PowerY in range(1, 4):
                for Item in [2, 3.4, MeasuredValue(3.2, 0.1)]:
                    TestCheck = pow(Item, PowerX) * pow(Item, PowerY)
                    #non-central not normalized
                    TestResult = self.TestFunction([Item], [Item], PowerX,
                                                                        PowerY)
                    self.assertIsInstance(TestResult, (int, float))
                    self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
                    TestResult = self.TestFunction([Item], [Item], PowerX,
                                                        PowerY,
                                                        IsCentral = False,
                                                        IsNormalized = False)
                    self.assertIsInstance(TestResult, (int, float))
                    self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
                    #central not normalized
                    TestResult = self.TestFunction([Item], [Item], PowerX,
                                                    PowerY, IsCentral = True)
                    self.assertIsInstance(TestResult, (int, float))
                    self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
                    TestResult = self.TestFunction([Item], [Item], PowerX,
                                                    PowerY, IsCentral = True,
                                                        IsNormalized = False)
                    self.assertIsInstance(TestResult, (int, float))
                    self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
                    #central normalized
                    TestResult = self.TestFunction([Item], [Item], PowerX,
                                                    PowerY, IsCentral = True,
                                                            IsNormalized = True)
                    self.assertIsInstance(TestResult, (int, float))
                    self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
        for _ in range(10):
            Const = random.random() + random.randint(-3, 4)
            Array1 = [Const for _ in range(len(self.AllInt))]
            PowerX = random.randint(1, 4)
            PowerY = random.randint(1, 4)
            TestCheck1 = sum(pow(Const, PowerX) * pow(Item, PowerY)
                                        for Item in self.AllInt) / len(Array1)
            TestCheck2 = sum(pow(Const, PowerY) * pow(Item, PowerX)
                                        for Item in self.AllInt) / len(Array1)
            TestCheck3 = pow(Const, PowerX) * pow(Const, PowerY)
            #non-central not normalized
            TestResult = self.TestFunction(Array1, self.AllInt, PowerX, PowerY)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck1,
                                                    delta = DELTA_PRECISION)
            TestResult = self.TestFunction(Array1, self.AllInt, PowerX, PowerY,
                                                        IsCentral = False,
                                                        IsNormalized = False)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck1,
                                                    delta = DELTA_PRECISION)
            TestResult = self.TestFunction(self.AllInt, Array1, PowerX, PowerY)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck2,
                                                    delta = DELTA_PRECISION)
            TestResult = self.TestFunction(self.AllInt, Array1, PowerX, PowerY,
                                                        IsCentral = False,
                                                        IsNormalized = False)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck2,
                                                    delta = DELTA_PRECISION)
            TestResult = self.TestFunction(Array1, Array1, PowerX, PowerY)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck3,
                                                    delta = DELTA_PRECISION)
            TestResult = self.TestFunction(Array1, Array1, PowerX, PowerY,
                                                        IsCentral = False,
                                                        IsNormalized = False)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, TestCheck3,
                                                    delta = DELTA_PRECISION)
            #central not normalized
            TestResult = self.TestFunction(Array1, self.AllInt, PowerX, PowerY,
                                                            IsCentral = True)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(self.AllInt, Array1, PowerX, PowerY,
                                                            IsCentral = True)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(Array1, Array1, PowerX, PowerY,
                                                            IsCentral = True)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(Array1, self.AllInt, PowerX, PowerY,
                                                            IsCentral = True,
                                                        IsNormalized = False)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(self.AllInt, Array1, PowerX, PowerY,
                                                            IsCentral = True,
                                                        IsNormalized = False)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(Array1, Array1, PowerX, PowerY,
                                                            IsCentral = True,
                                                        IsNormalized = False)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            #central normalized
            TestResult = self.TestFunction(Array1, self.AllInt, PowerX, PowerY,
                                                            IsCentral = True,
                                                            IsNormalized = True)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(self.AllInt, Array1, PowerX, PowerY,
                                                            IsCentral = True,
                                                            IsNormalized = True)
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, 0,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(Array1, Array1, PowerX, PowerY,
                                                            IsCentral = True,
                                                            IsNormalized = True)


#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMean)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_GetVarianceP)

TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_GetStdevP)

TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_GetVarianceS)

TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_GetStdevS)

TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_GetSE)

TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMeanSqrSE)

TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(Test_GetFullSE)

TestSuite9 = unittest.TestLoader().loadTestsFromTestCase(Test_GetSkewnessP)

TestSuite10 = unittest.TestLoader().loadTestsFromTestCase(Test_GetSkewnessS)

TestSuite11 = unittest.TestLoader().loadTestsFromTestCase(Test_GetKurtosisP)

TestSuite12 = unittest.TestLoader().loadTestsFromTestCase(Test_GetKurtosisS)

TestSuite13 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMoment)

TestSuite14 = unittest.TestLoader().loadTestsFromTestCase(Test_GetCovariance)

TestSuite15 = unittest.TestLoader().loadTestsFromTestCase(Test_GetPearsonR)

TestSuite16 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMoment2)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6, TestSuite7, TestSuite8, TestSuite9, TestSuite10,
                    TestSuite11, TestSuite12, TestSuite13, TestSuite14,
                    TestSuite15, TestSuite16])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.base_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
