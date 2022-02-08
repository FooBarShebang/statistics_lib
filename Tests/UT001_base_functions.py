#usr/bin/python3
"""
Module statistics_lib.Tests.UT001_base_functions

Set of unit tests on the module stastics_lib.base_functions. See the test plan /
report TE001_base_functions.md
"""


__version__= '1.0.0.0'
__date__ = '07-02-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import unittest
import random
import statistics

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


#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMean)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_GetVarianceP)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.base_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
