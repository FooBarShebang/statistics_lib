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
            Left = Sorted[Index] - FLOAT_CHECK_PRECISION
            Right = Sorted[Index + 1] + FLOAT_CHECK_PRECISION
            TestResult = self.TestFunction(BaseInput)
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                TestCheck = self.CheckFunction(BaseInput, n = 4,
                                                        method = 'inclusive')[0]
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
            Left = Sorted[Index] - FLOAT_CHECK_PRECISION
            Right = Sorted[Index + 1] + FLOAT_CHECK_PRECISION
            TestResult = self.TestFunction(TestInput)
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                TestCheck = self.CheckFunction(BaseInput, n = 4,
                                                        method = 'inclusive')[0]
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
            Left = Sorted[Index] - FLOAT_CHECK_PRECISION
            Right = Sorted[Index + 1] + FLOAT_CHECK_PRECISION
            TestResult = self.TestFunction(BaseInput)
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                TestCheck = self.CheckFunction(BaseInput, n = 4,
                                                    method = 'inclusive')[-1]
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
            Left = Sorted[Index] - FLOAT_CHECK_PRECISION
            Right = Sorted[Index + 1] + FLOAT_CHECK_PRECISION
            TestResult = self.TestFunction(TestInput)
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                TestCheck = self.CheckFunction(BaseInput, n = 4,
                                                    method = 'inclusive')[-1]
                self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(tuple(TestInput))
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Left)
            self.assertLessEqual(TestResult, Right)
            if self.ExtraCheck:
                self.assertAlmostEqual(TestResult, TestCheck,
                                                places = FLOAT_CHECK_PRECISION)

class Test_GetQuantile(Test_GetFirstQuartile):
    """
    Unit-test class implementing testing of the function GetQuantile() from the
    module statistics_lib.ordered_functions.

    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-260.
    Covers the requirements REQ-FUN-201, REQ-FUN-260, REQ-AWM-200, REQ-AWM-201.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetQuantile)
        if cls.ExtraCheck:
            cls.CheckFunction = staticmethod(statistics.quantiles)
    
    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested

        Implements test TEST-T-200, TEST-T-250.
        Covers the requirement REQ-FUN-201, REQ-FUN-250.
        """
        for TestInput, BaseInput in ((self.AllInt, self.AllInt),
                                        (self.AllFloat, self.AllFloat),
                                        (self.Mixed, self.Mixed),
                                        (self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
            Sorted = sorted(BaseInput)
            N = len(Sorted)
            for m in [4, 10, 25, 30, 100]:
                for k in range (1, m):
                    Index = ((N-1) * k) // m
                    Left = Sorted[Index] - FLOAT_CHECK_PRECISION
                    Right = Sorted[Index + 1] + FLOAT_CHECK_PRECISION
                    TestResult = self.TestFunction(TestInput, k, m)
                    self.assertIsInstance(TestResult, (int, float))
                    self.assertGreaterEqual(TestResult, Left)
                    self.assertLessEqual(TestResult, Right)
                    if self.ExtraCheck:
                        TestCheck = self.CheckFunction(BaseInput, n = m,
                                                    method = 'inclusive')[k-1]
                    self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
                    TestResult = self.TestFunction(tuple(TestInput), k, m)
                    self.assertIsInstance(TestResult, (int, float))
                    self.assertGreaterEqual(TestResult, Left)
                    self.assertLessEqual(TestResult, Right)
                    if self.ExtraCheck:
                        self.assertAlmostEqual(TestResult, TestCheck, 
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = self.TestFunction(TestInput, 0, m)
                self.assertIsInstance(TestResult, (int, float))
                self.assertEqual(TestResult, Sorted[0])
                TestResult = self.TestFunction(TestInput, m, m)
                self.assertIsInstance(TestResult, (int, float))
                self.assertEqual(TestResult, Sorted[-1])
    
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
                self.TestFunction(Item, 1, 2)
    
    def test_TypeError(self) -> None:
        """
        Checks that sub-class of TypeError is raised with improper input data
        type.

        Implements test TEST-T-201.
        Covers the requirement REQ-AWM-200.
        """
        for Temp in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestFunction(Temp, 1, 2)
        for k in [1.0, '1', [1], (1, 2), MeasuredValue(1), {1:1}]:
            with self.assertRaises(TypeError):
                self.TestFunction([1, 2, 3], k, 10)
            with self.assertRaises(TypeError):
                self.TestFunction([1, 2, 3], 1, k)

    def test_ValueError(self) -> None:
        """
        Checks that sub-class of ValueError is raised with proper input data
        type but wrong value.

        Implements test TEST-T-202.
        Covers the requirement REQ-AWM-201.
        """
        with self.assertRaises(ValueError):
            self.TestFunction([], 1, 2) #empty sequence
        for m in [0, -1, -10]:
            with self.assertRaises(ValueError):
                self.TestFunction([1, 2, 3], 1, m)
            with self.assertRaises(ValueError):
                self.TestFunction([1, 2, 3], m - 1, 4)
        for m in [4, 10, 25]:
            for k in [1, 4, 10]:
                with self.assertRaises(ValueError):
                    self.TestFunction([1, 2, 3], m + k , m)

class Test_GetHistogram(Test_GetMin):
    """
    Unit-test class implementing testing of the function GetHistogram() from the
    module statistics_lib.ordered_functions.

    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-270.
    Covers the requirements REQ-FUN-201, REQ-FUN-270, REQ-AWM-200, REQ-AWM-201.
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetHistogram)
    
    def test_TypeError(self) -> None:
        """
        Checks that sub-class of TypeError is raised with improper input data
        type.

        Implements test TEST-T-201.
        Covers the requirement REQ-AWM-200.
        """
        super().test_TypeError()
        for Value in ['1', 1.0, (1, ), [1], MeasuredValue(1), {1:1}]:
            with self.assertRaises(TypeError):
                self.TestFunction([1, 2, 3], NBins = Value)
        for Value in ['1', (1, ), [1], MeasuredValue(1), {1:1}]:
            with self.assertRaises(TypeError):
                self.TestFunction([1, 2, 3], BinSize = Value)

    def test_ValueError(self) -> None:
        """
        Checks that sub-class of ValueError is raised with proper input data
        type but wrong value.

        Implements test TEST-T-202.
        Covers the requirement REQ-AWM-201.
        """
        super().test_ValueError()
        for Value in [0, -1, -10]:
            with self.assertRaises(ValueError):
                self.TestFunction([1, 2, 3], NBins = Value)
        for Value in [0, -1, -0.5, -10]:
            with self.assertRaises(ValueError):
                self.TestFunction([1, 2, 3], BinSize = Value)
    
    def test_OkOperation(self) -> None:
        """
        Checks the normal operation mode of the function being tested with the
        default values of the keyword arguments.

        Implements test TEST-T-200, TEST-T-270.
        Covers the requirement REQ-FUN-201, REQ-FUN-270.
        """
        for TestInput, BaseInput in ((self.AllInt, self.AllInt),
                                        (self.AllFloat, self.AllFloat),
                                        (self.Mixed, self.Mixed),
                                        (self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
            TestResult = self.TestFunction(TestInput)
            self.assertIsInstance(TestResult, dict)
            self.assertEqual(len(TestResult), 20)
            Keys = list(TestResult.keys())
            Values = list(TestResult.values())
            Length = len(BaseInput)
            self.assertAlmostEqual(Keys[0], min(BaseInput),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(Keys[-1], max(BaseInput),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertEqual(sum(Values), Length)
            Step = round((Keys[-1] - Keys[0]) / 19, 16)
            for Index in range(1, len(Keys)):
                self.assertAlmostEqual(Keys[Index] - Keys[Index - 1], Step,
                                                places = FLOAT_CHECK_PRECISION)
            for Key in Keys:
                self.assertIsInstance(Key, (int, float))
                self.assertIsInstance(TestResult[Key], int)
                self.assertGreaterEqual(TestResult[Key], 0)
                N = 0
                for Item in BaseInput:
                    bCond1 = round(Item, 16) >= round(Key - 0.5 * Step, 16)
                    bCond2 = round(Item, 16) < round(Key + 0.5 * Step, 16)
                    if bCond1 and bCond2:
                        N += 1
                self.assertEqual(N, TestResult[Key])

    def test_OkBins(self) -> None:
        """
        Checks the normal operation mode of the function being tested with the
        desired number of bins requested

        Implements test TEST-T-200, TEST-T-270.
        Covers the requirement REQ-FUN-201, REQ-FUN-270.
        """
        for TestInput, BaseInput in ((self.AllInt, self.AllInt),
                                        (self.AllFloat, self.AllFloat),
                                        (self.Mixed, self.Mixed),
                                        (self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
            NBins = random.randint(10, 30)
            TestResult = self.TestFunction(TestInput, NBins = NBins)
            self.assertIsInstance(TestResult, dict)
            self.assertEqual(len(TestResult), NBins)
            Keys = list(TestResult.keys())
            Values = list(TestResult.values())
            Length = len(BaseInput)
            self.assertAlmostEqual(Keys[0], min(BaseInput),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(Keys[-1], max(BaseInput),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertEqual(sum(Values), Length)
            Step = round((Keys[-1] - Keys[0]) / (NBins - 1), 16)
            for Index in range(1, len(Keys)):
                self.assertAlmostEqual(Keys[Index] - Keys[Index - 1], Step,
                                                places = FLOAT_CHECK_PRECISION)
            for Key in Keys:
                self.assertIsInstance(Key, (int, float))
                self.assertIsInstance(TestResult[Key], int)
                self.assertGreaterEqual(TestResult[Key], 0)
                N = 0
                for Item in BaseInput:
                    bCond1 = round(Item, 16) >= round(Key - 0.5 * Step, 16)
                    bCond2 = round(Item, 16) < round(Key + 0.5 * Step, 16)
                    if bCond1 and bCond2:
                        N += 1
                self.assertEqual(N, TestResult[Key])
    
    def test_OkBinsSize(self) -> None:
        """
        Checks the normal operation mode of the function being tested with the
        desired number of bins requested and the bin size also requested

        Implements test TEST-T-200, TEST-T-270.
        Covers the requirement REQ-FUN-201, REQ-FUN-270.
        """
        for TestInput, BaseInput in ((self.AllInt, self.AllInt),
                                        (self.AllFloat, self.AllFloat),
                                        (self.Mixed, self.Mixed),
                                        (self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
            NBins = random.randint(10, 30)
            BinSize = (max(BaseInput) - min(BaseInput)) / 5
            TestResult = self.TestFunction(TestInput, NBins = NBins,
                                                            BinSize = BinSize)
            self.assertIsInstance(TestResult, dict)
            self.assertEqual(len(TestResult), NBins)
            Keys = list(TestResult.keys())
            Values = list(TestResult.values())
            Length = len(BaseInput)
            self.assertAlmostEqual(Keys[0], min(BaseInput),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(Keys[-1], max(BaseInput),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertEqual(sum(Values), Length)
            Step = round((Keys[-1] - Keys[0]) / (NBins - 1), 16)
            for Index in range(1, len(Keys)):
                self.assertAlmostEqual(Keys[Index] - Keys[Index - 1], Step,
                                                places = FLOAT_CHECK_PRECISION)
            for Key in Keys:
                self.assertIsInstance(Key, (int, float))
                self.assertIsInstance(TestResult[Key], int)
                self.assertGreaterEqual(TestResult[Key], 0)
                N = 0
                for Item in BaseInput:
                    bCond1 = round(Item, 16) >= round(Key - 0.5 * Step, 16)
                    bCond2 = round(Item, 16) < round(Key + 0.5 * Step, 16)
                    if bCond1 and bCond2:
                        N += 1
                self.assertEqual(N, TestResult[Key])
    
    def test_OkSize(self) -> None:
        """
        Checks the normal operation mode of the function being tested with the
        desired bin size requested.

        Implements test TEST-T-200, TEST-T-270.
        Covers the requirement REQ-FUN-201, REQ-FUN-270.
        """
        for TestInput, BaseInput in ((self.AllInt, self.AllInt),
                                        (self.AllFloat, self.AllFloat),
                                        (self.Mixed, self.Mixed),
                                        (self.IntErr, self.AllInt),
                                        (self.FloatErr, self.AllFloat),
                                        (self.MixedErr, self.Mixed),
                                        (self.TotalMixed, self.Mixed)):
            BinSize = (max(BaseInput) - min(BaseInput)) / random.randint(10, 30)
            TestResult = self.TestFunction(TestInput, BinSize = BinSize)
            self.assertIsInstance(TestResult, dict)
            NBins = len(TestResult)
            Check = (max(BaseInput) - min(BaseInput)) / BinSize
            self.assertLessEqual(NBins - 2, Check)
            self.assertGreaterEqual(NBins, Check)
            Keys = list(TestResult.keys())
            Values = list(TestResult.values())
            Length = len(BaseInput)
            self.assertLessEqual(Keys[0] - 0.5 * BinSize, min(BaseInput))
            self.assertGreater(Keys[0] + 0.5 * BinSize, min(BaseInput))
            self.assertLessEqual(Keys[-1] - 0.5 * BinSize, max(BaseInput))
            self.assertGreater(Keys[-1] + 0.5 * BinSize, max(BaseInput))
            self.assertEqual(sum(Values), Length)
            Step = round(BinSize, 16)
            for Index in range(1, len(Keys)):
                self.assertAlmostEqual(Keys[Index] - Keys[Index - 1], Step,
                                                places = FLOAT_CHECK_PRECISION)
            for Key in Keys:
                self.assertIsInstance(Key, (int, float))
                self.assertIsInstance(TestResult[Key], int)
                self.assertGreaterEqual(TestResult[Key], 0)
                N = 0
                for Item in BaseInput:
                    bCond1 = round(Item, 16) >= round(Key - 0.5 * Step, 16)
                    bCond2 = round(Item, 16) < round(Key + 0.5 * Step, 16)
                    if bCond1 and bCond2:
                        N += 1
                self.assertEqual(N, TestResult[Key])
    
    def test_EdgeCases(self) -> None:
        """
        Checks the edge cases, which must result in a single bin histogram.

        Implements test TEST-T-200, TEST-T-270.
        Covers the requirement REQ-FUN-201, REQ-FUN-270.
        """
        #same elements in the input
        for BaseInput in [[1], [2.5, 2.5], [3, 3, 3]]:
            DictCheck = {BaseInput[0] : len(BaseInput)}
            TestResult = self.TestFunction(BaseInput)
            self.assertDictEqual(TestResult, DictCheck)
            TestResult = self.TestFunction(BaseInput, NBins = 10)
            self.assertDictEqual(TestResult, DictCheck)
            TestResult = self.TestFunction(BaseInput, BinSize = 0.1)
            self.assertDictEqual(TestResult, DictCheck)
        #single bin is explicitely requested
        BaseInput = [1, 1.4, 2, 0.5, 1.3]
        DictCheck = {statistics.mean(BaseInput) : len(BaseInput)}
        TestResult = self.TestFunction(BaseInput, NBins = 1)
        self.assertDictEqual(TestResult, DictCheck)
        # single bin results from too broad bin size
        TestResult = self.TestFunction(BaseInput, BinSize = 5)
        self.assertDictEqual(TestResult, DictCheck)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMin)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMax)

TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMedian)

TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_GetFirstQuartile)

TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_GetThirdQuartile)

TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_GetQuantile)

TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_GetHistogram)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                        TestSuite6, TestSuite7])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.ordered_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)