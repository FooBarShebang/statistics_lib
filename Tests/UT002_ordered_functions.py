#usr/bin/python3
"""
Module statistics_lib.Tests.UT002_ordered_functions

Set of unit tests on the module stastics_lib.base_functions. See the test plan /
report TE002_ordered_functions.md
"""


__version__= '1.0.0.0'
__date__ = '17-02-2022'
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

import statistics_lib.ordered_functions as test_module

from phyqus_lib.base_classes import MeasuredValue

#globals

FLOAT_CHECK_PRECISION = 8 #digits after comma

#classes

#+ test cases

class Test_GetMin(unittest.TestCase):
    """
    Unit-test class implementing testing of the function GetMin() from the
    module statistics_lib.ordered_functions.

    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-210.
    Covers the requirements REQ-FUN-201, REQ-FUN-210, REQ-AWM-200, REQ-AWM-201.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.GetMin)
        cls.CheckFunction = staticmethod(min)
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

        Implements test TEST-T-201.
        Covers the requirement REQ-AWM-200.
        """
        for Temp in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestFunction(Temp)

    def test_ValueError(self) -> None:
        """
        Checks that sub-class of ValueError is raised with proper input data
        type but wrong value.

        Implements test TEST-T-202.
        Covers the requirement REQ-AWM-201.
        """
        with self.assertRaises(ValueError):
            self.TestFunction([]) #empty sequence

    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-200, TEST-T-210.
        Covers the requirement REQ-FUN-201, REQ-FUN-210.
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

class Test_GetMax(Test_GetMin):
    """
    Unit-test class implementing testing of the function GetMax() from the
    module statistics_lib.ordered_functions.

    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-220.
    Covers the requirements REQ-FUN-201, REQ-FUN-220, REQ-AWM-200, REQ-AWM-201.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetMax)
        cls.CheckFunction = staticmethod(max)

class Test_GetMedian(Test_GetMin):
    """
    Unit-test class implementing testing of the function GetMedian() from the
    module statistics_lib.ordered_functions.

    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-230.
    Covers the requirements REQ-FUN-201, REQ-FUN-230, REQ-AWM-200, REQ-AWM-201.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetMedian)
        cls.CheckFunction = staticmethod(statistics.median)

class Test_GetFirstQuartile(Test_GetMin):
    """
    Unit-test class implementing testing of the function GetFirstQuartile() from
    the module statistics_lib.ordered_functions.

    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-240.
    Covers the requirements REQ-FUN-201, REQ-FUN-240, REQ-AWM-200, REQ-AWM-201.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetFirstQuartile)
        cls.ExtraCheck = sys.version_info[0] >= 3 and sys.version_info[1] >= 8
        if cls.ExtraCheck:
            cls.CheckFunction = staticmethod(statistics.quantiles)
    
    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-200, TEST-T-240.
        Covers the requirement REQ-FUN-201, REQ-FUN-240.
        """
        for BaseInput in [self.AllInt, self.AllFloat, self.Mixed]:
            Sorted = sorted(BaseInput)
            N = len(Sorted)
            Index = (N-1) // 4
            Left = Sorted[Index]
            Right = Sorted[Index + 1]
            TestResult = self.TestFunction(BaseInput)
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                TestCheck = self.CheckFunction(BaseInput, n = 4)[0]
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(BaseInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
        for TestInput, BaseInput in ((self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
            Sorted = sorted(BaseInput)
            N = len(Sorted)
            Index = (N-1) // 4
            Left = Sorted[Index]
            Right = Sorted[Index + 1]
            TestResult = self.TestFunction(TestInput)
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                TestCheck = self.CheckFunction(BaseInput, n = 4)[0]
                self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(TestInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
    
    def test_EdgeCase(self):
        """
        Checks that ValueError sub-class exception is raised if the sequence is
        only 1 element long.
        
        Implements test TEST-T-202.
        Covers the requirement REQ-AWM-201.
        """
        for Item in [(1, ), (1.0, ), (MeasuredValue(1), ), [1], [1.0],
                                                            [MeasuredValue(1)]]:
            with self.assertRaises(ValueError):
                self.TestFunction(Item)

class Test_GetThirdQuartile(Test_GetFirstQuartile):
    """
    Unit-test class implementing testing of the function GetFirstQuartile() from
    the module statistics_lib.ordered_functions.

    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-250.
    Covers the requirements REQ-FUN-201, REQ-FUN-250, REQ-AWM-200, REQ-AWM-201.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetThirdQuartile)
        if cls.ExtraCheck:
            cls.CheckFunction = staticmethod(statistics.quantiles)
    
    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-200, TEST-T-250.
        Covers the requirement REQ-FUN-201, REQ-FUN-250.
        """
        for BaseInput in [self.AllInt, self.AllFloat, self.Mixed]:
            Sorted = sorted(BaseInput)
            N = len(Sorted)
            Index = ((N-1) * 3) // 4
            Left = Sorted[Index]
            Right = Sorted[Index + 1]
            TestResult = self.TestFunction(BaseInput)
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                TestCheck = self.CheckFunction(BaseInput, n = 4)[-1]
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(BaseInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
        for TestInput, BaseInput in ((self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
            Sorted = sorted(BaseInput)
            N = len(Sorted)
            Index = ((N-1) * 3) // 4
            Left = Sorted[Index]
            Right = Sorted[Index + 1]
            TestResult = self.TestFunction(TestInput)
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                TestCheck = self.CheckFunction(BaseInput, n = 4)[-1]
                self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(TestInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMin)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMax)

TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMedian)

TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_GetFirstQuartile)

TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_GetThirdQuartile)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.ordered_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)