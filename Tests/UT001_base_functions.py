#usr/bin/python3
"""
Module statistics_lib.Tests.UT001_base_functions

Set of unit tests on the module stastics_lib.base_functions. See the test plan /
report TE001_base_functions.md
"""


__version__= '1.0.0.0'
__date__ = '08-02-2022'
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

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMean)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_GetVarianceP)

TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_GetStdevP)

TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_GetVarianceS)

TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_GetStdevS)

TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_GetSE)

TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMeanSqrSE)

TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(Test_GetFullSE)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6, TestSuite7, TestSuite8])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.base_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
