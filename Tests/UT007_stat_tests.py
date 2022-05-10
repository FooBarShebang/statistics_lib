#usr/bin/python3
"""
Module statistics_lib.Tests.UT007_stat_tests

Set of unit tests on the module stastics_lib.stat_tests. See the test
plan / report TE007_stat_tests.md
"""


__version__= '1.0.0.0'
__date__ = '10-05-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import unittest
import math
import random

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.stat_tests as test_module

from statistics_lib.data_classes import Statistics1D

from statistics_lib.distribution_classes import Gaussian, Z_Distribution
from statistics_lib.distribution_classes import Student, F_Distribution
from statistics_lib.distribution_classes import ChiSquared

class Test_TestResult(unittest.TestCase):
    """
    Unittests for TestResult class from the module statistics_lib.stat_tests.
    
    Implements tests: TEST-T-7B0.
    
    Covers requirements: REQ-FUN-7B0, REQ-FUN-7B1.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        
        Version 1.0.0.0
        """
        cls.TestClass = test_module.TestResult
    
    def test_TestName_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        
        Version 1.0.0.0
        """
        for gItem in [1, -2.0, [1,2], (2.0, 1), int, str, float, bool, {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass(gItem, 'test', 'test', 2.1, 0.95, (None, 2.0))
    
    def test_DataName_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        
        Version 1.0.0.0
        """
        for gItem in [1, -2.0, [1,2], (2.0, 1), int, str, float, bool, {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass('test', gItem, 'test', 2.1, 0.95, (None, 2.0))
    
    def test_ModelName_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        
        Version 1.0.0.0
        """
        for gItem in [1, -2.0, [1,2], (2.0, 1), int, str, float, bool, {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass('test', 'test', gItem, 2.1, 0.95, (None, 2.0))
    
    def test_TestValue_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        
        Version 1.0.0.0
        """
        for gItem in ['-2.0', [1,2], (2.0, 1), int, str, float, bool, {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass('test', 'test', 'test', gItem, 0.95, (None, 2.0))
    
    def test_CDF_Value_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        
        Version 1.0.0.0
        """
        for gItem in [1, '-2.0', [1, 2], (2.0, 1), int, str, float, bool,
                                                                    {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass('test', 'test', 'test', 2.1, gItem, (None, 2.0))
    
    def test_CritValues_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        
        Version 1.0.0.0
        """
        for gItem in [1, '-2.0', [1, 2], (2.0, 1, 3), int, str, float, bool,
                                    {'a':1}, (2.0, ), (None, None), ('1', 1)]:
            with self.assertRaises(TypeError):
                self.TestClass('test', 'test', 'test', 2.1, 0.95, gItem)
    
    def test_CDF_Value_ValueError(self):
        """
        Additional test - checks the sanity checks on the input values.
        
        Version 1.0.0.0
        """
        for _ in range(100):
            Value1 = random.randint(1, 5)
            if random.random() > 0.5:
                Value1 *= -1
            Value1 += random.random()
            with self.assertRaises(ValueError):
                self.TestClass('test', 'test', 'test', 2.1, Value1, (None, 2.0))
        with self.assertRaises(ValueError):
            self.TestClass('test', 'test', 'test', 2.1, 0.0, (None, 2.0))
        with self.assertRaises(ValueError):
            self.TestClass('test', 'test', 'test', 2.1, 1.0, (None, 2.0))
    
    def test_CritValues_ValueError(self):
        """
        Additional test - checks the sanity checks on the input values.
        
        Version 1.0.0.0
        """
        for _ in range(100):
            Value1 = random.randint(-5, 5)
            if random.random() > 0.5:
                Value1 += random.random()
            Value2 = Value1 - 0.1 - random.random() - random.randint(0, 10)
            gItem = (Value1, Value2)
            with self.assertRaises(ValueError):
                self.TestClass('test', 'test', 'test', 2.1, 0.95, gItem)
    
    def test_IsRejected(self):
        """
        Checks the functionality of the getter property IsRejected.
        
        Test IDs: TEST-T-7B0.
        Requirement IDs: REQ-FUN-7B0, REQ-FUN-7B1.
        
        Version 1.0.0.0
        """
        #2-sided - failed
        objTest = self.TestClass('test', 'test', 'test', 1.0, 0.6, (0.5, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        del objTest
        #2-sided - passed - on the edge
        objTest = self.TestClass('test', 'test', 'test', 2.0, 0.6, (0.5, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
        objTest = self.TestClass('test', 'test', 'test', 0.5, 0.6, (0.5, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
        #2-sided - passed - more extreme than critical
        objTest = self.TestClass('test', 'test', 'test', 2.5, 0.6, (0.5, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
        objTest = self.TestClass('test', 'test', 'test', 0.4, 0.6, (0.5, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
        #1-sided right-tailed - failed
        objTest = self.TestClass('test', 'test', 'test', 1.0, 0.6, (None, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        del objTest
        #1-sided right-tailed - passed - on the edge
        objTest = self.TestClass('test', 'test', 'test', 2.0, 0.6, (None, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
        #1-sided right-tailed - passed - above critical
        objTest = self.TestClass('test', 'test', 'test', 2.5, 0.6, (None, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
        #1-sided left-tailed - failed
        objTest = self.TestClass('test', 'test', 'test', 1.0, 0.6, (0.5, None))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        del objTest
        #1-sided left-tailed - passed - on the edge
        objTest = self.TestClass('test', 'test', 'test', 0.5, 0.6, (0.5, None))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
        #1-sided left-tailed - passed - below critical
        objTest = self.TestClass('test', 'test', 'test', 0.3, 0.6, (0.5, None))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
        #1-sided right-tailed special - failed
        objTest = self.TestClass('test', 'test', 'test', 1.0, 0.6, (2.0, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        del objTest
        #1-sided right-tailed special - passed - on the edge
        objTest = self.TestClass('test', 'test', 'test', 2.0, 0.6, (2.0, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
        #1-sided right-tailed special - passed - above critical
        objTest = self.TestClass('test', 'test', 'test', 2.5, 0.6, (2.0, 2.0))
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        del objTest
    
    def test_p_Value(self):
        """
        Checks the functionality of the getter property p_Value.
        
        Test IDs: TEST-T-7B0.
        Requirement IDs: REQ-FUN-7B0, REQ-FUN-7B1.
        
        Version 1.0.0.0
        """
        #2-sided
        #+ special case - exactly median
        objTest = self.TestClass('test', 'test', 'test', 2.5, 0.5, (1.0, 2.0))
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, 1.0)
        del objTest
        #+ general cases
        for _ in range(10):
            #above median
            fValue = 0.5 * (1 + random.random())
            if fValue >= 1.0:
                fValue = 0.99
            elif fValue <= 0.5:
                fValue = 0.51
            objTest = self.TestClass('test', 'test', 'test', 2.5, fValue,
                                                                    (1.0, 2.0))
            self.assertIsInstance(objTest.p_Value, float)
            self.assertLess(objTest.p_Value, 1.0)
            self.assertGreater(objTest.p_Value, 0.0)
            self.assertAlmostEqual(objTest.p_Value, 2 * (1 - fValue))
            del objTest
            #below median
            fValue = 0.5 * random.random()
            if fValue <= 0.0:
                fValue = 0.01
            objTest = self.TestClass('test', 'test', 'test', 2.5, fValue,
                                                                    (1.0, 2.0))
            self.assertIsInstance(objTest.p_Value, float)
            self.assertLess(objTest.p_Value, 1.0)
            self.assertGreater(objTest.p_Value, 0.0)
            self.assertAlmostEqual(objTest.p_Value, 2 * fValue)
            del objTest
        #1-sided right-tailed
        for _ in range(10):
            fValue = 0.05 + 0.9 * random.random()
            objTest = self.TestClass('test', 'test', 'test', 2.5, fValue,
                                                                    (None, 2.0))
            self.assertIsInstance(objTest.p_Value, float)
            self.assertLess(objTest.p_Value, 1.0)
            self.assertGreater(objTest.p_Value, 0.0)
            self.assertAlmostEqual(objTest.p_Value, 1.0 - fValue)
            del objTest
        #1-sided right-tailed special
        for _ in range(10):
            fValue = 0.05 + 0.9 * random.random()
            objTest = self.TestClass('test', 'test', 'test', 2.5, fValue,
                                                                    (2.0, 2.0))
            self.assertIsInstance(objTest.p_Value, float)
            self.assertLess(objTest.p_Value, 1.0)
            self.assertGreater(objTest.p_Value, 0.0)
            self.assertAlmostEqual(objTest.p_Value, 1.0 - fValue)
            del objTest
        #1-sided left-tailed
        for _ in range(10):
            fValue = 0.05 + 0.9 * random.random()
            objTest = self.TestClass('test', 'test', 'test', 2.5, fValue,
                                                                    (2.0, None))
            self.assertIsInstance(objTest.p_Value, float)
            self.assertLess(objTest.p_Value, 1.0)
            self.assertGreater(objTest.p_Value, 0.0)
            self.assertAlmostEqual(objTest.p_Value, fValue)
            del objTest
    
    def test_Report(self):
        """
        Checks that the getter property Report always returns a string value.
        
        Test IDs: TEST-T-7B0.
        Requirement IDs: REQ-FUN-7B0, REQ-FUN-7B1.
        
        Version 1.0.0.0
        """
        for _ in range(10):
            CDF_Value = 0.05 + 0.9 * random.random()
            LeftBound = random.randint(-4, 3) + random.random()
            RightBound = LeftBound + random.randint(1, 3) + random.random()
            TestValue = random.randint(-6, 8) + random.random()
            CritValues = (LeftBound, RightBound)
            #2-sided
            objTest = self.TestClass('test', 'test', 'test', TestValue,
                                                        CDF_Value, CritValues)
            Report = objTest.Report
            self.assertIsInstance(Report, str)
            self.assertGreater(len(Report), 0)
            del objTest
            #1-sided right-tailed
            CritValues = (None, RightBound)
            objTest = self.TestClass('test', 'test', 'test', TestValue,
                                                        CDF_Value, CritValues)
            Report = objTest.Report
            self.assertIsInstance(Report, str)
            self.assertGreater(len(Report), 0)
            del objTest
            #1-sided right-tailed special
            CritValues = (RightBound, RightBound)
            objTest = self.TestClass('test', 'test', 'test', TestValue,
                                                        CDF_Value, CritValues)
            Report = objTest.Report
            self.assertIsInstance(Report, str)
            self.assertGreater(len(Report), 0)
            del objTest
            #1-sided left-tailed
            CritValues = (LeftBound, None)
            objTest = self.TestClass('test', 'test', 'test', TestValue,
                                                        CDF_Value, CritValues)
            Report = objTest.Report
            self.assertIsInstance(Report, str)
            self.assertGreater(len(Report), 0)
            del objTest

class Test_z_test(unittest.TestCase):
    """
    Unit tests for the function z_test from the module
    statistics_lib.stat_tests.
    
    Implements tests: TEST-T-710, TEST-T-700, TEST-T-701 and TEST-T-702.
    
    Covers requirements: REQ-FUN-710, REQ-AWM-700, REQ-AWM-701, REQ-SIO-700,
    REQ-SIO-701 and REQ-SIO-702.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        
        Version 1.0.0.0
        """
        cls.TestFunction = staticmethod(test_module.z_test)
        cls.PMean = random.randint(-2, 1) + random.random()
        cls.PSigma = 0.5 + random.random()
        cls.Length = random.randint(10, 20)
        objGenerator = Gaussian(cls.PMean, cls.PSigma)
        cls.Data = Statistics1D([objGenerator.random()
                                                    for _ in range(cls.Length)])
        cls.BadDataType = (1, 1.0, [1, 2.0], (1, 3), int, float, list, tuple,
                                            bool, True, None, {'a':1}, 'test')
        cls.NotReal = ([1, 2.0], (1, 3), int, float, list, tuple, bool,
                                                None, {'a':1}, cls.Data, 'test')
        cls.NotFloat = ([1, 2.0], (1, 3), int, float, list, tuple, bool, True,
                                            None, {'a':1}, cls.Data, 'test', 1)
        cls.Model = Z_Distribution()
    
    @classmethod
    def tearDownClass(cls) -> None:
        del cls.Data
        cls.Data = None
    
    def test_TypeError(self):
        """
        Checks that TypeError (or its sub-class) is raised in response to the
        unexpected / inappropriate data type of, at least, one argument.
        
        Test ID: TEST-T-700
        Requirement ID: REQ-AWM-700
        
        Version 1.0.0.0
        """
        for gItem in self.BadDataType:
            #Data argument
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, 1.0, 0.5, test_module.GT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, 1.0, 0.5, test_module.LT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, 1.0, 0.5, test_module.NEQ_TEST)
            #Type argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, 0.5, gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, 0.5, gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, 0.5, gItem)
        for gItem in self.NotReal:
            #Mean argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, gItem, 0.5, test_module.GT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, gItem, 0.5, test_module.LT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, gItem, 0.5, test_module.NEQ_TEST)
            #Sigma argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, gItem, test_module.GT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, gItem, test_module.LT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, gItem, test_module.NEQ_TEST)
        for gItem in self.NotFloat:
            #Confidence keyword argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, 0.5, test_module.GT_TEST,
                                                            Confidence = gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, 0.5, test_module.LT_TEST,
                                                            Confidence = gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, 0.5, test_module.NEQ_TEST,
                                                            Confidence = gItem)

    def test_ValueError(self):
        """
        Checks that ValueError (or its sub-class) is raised in response to the
        unexpected / inappropriate value of, at least, one argument.
        
        Test ID: TEST-T-701
        Requirement ID: REQ-AWM-701
        
        Version 1.0.0.0
        """
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data, 1.0, 0, test_module.GT_TEST)
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data, 1.0, 0.0, test_module.GT_TEST)
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data, 1.0, 0.5, test_module.GT_TEST,
                                                            Confidence = 0.0)
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data, 1.0, 0.5, test_module.GT_TEST,
                                                            Confidence = 1.0)
        for _ in range(10):
            gValue = random.randint(1, 10)
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, 1.0, -gValue, test_module.GT_TEST)
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, 1.0, -gValue + random.random(),
                                                            test_module.GT_TEST)
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, 1.0, 0.5, test_module.GT_TEST,
                                        Confidence = gValue + random.random())
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, 1.0, 0.5, test_module.GT_TEST,
                                        Confidence = -gValue + random.random())
        #special case
        Data = Statistics1D([1])
        with self.assertRaises(ValueError):
            self.TestFunction(Data, 1.0, 0.5, test_module.GT_TEST)
    
    def test_GreaterTest(self):
        """
        Checks the implementation of the 1-sided right-tailed test.
        
        Test ID: TEST-T-710 and TEST-T-702
        Requirement ID: REQ-FUN-710, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        TestValue = math.sqrt(self.Length) * (self.Data.Mean - self.PMean)
        TestValue /= self.PSigma
        p_Value = 1 - self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data, self.PMean, self.PSigma,
                                                            test_module.GT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        if p_Value <= 0.05:
            self.assertTrue(objTest.IsRejected)
        else:
            self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to fail due to too high confidence level
        Confidence = 1 - 0.5 * p_Value
        objTest = self.TestFunction(self.Data, self.PMean, self.PSigma,
                                test_module.GT_TEST, Confidence = Confidence)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too low confidence level
        Confidence = 0.9 * (1 - p_Value)
        objTest = self.TestFunction(self.Data, self.PMean, self.PSigma,
                                test_module.GT_TEST, Confidence = Confidence)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        CritValue = self.Model.qf(0.95)
        #make sure to fail due to too high population mean
        Mean = self.Data.Mean - 0.9*self.PSigma*CritValue/math.sqrt(self.Length)
        objTest = self.TestFunction(self.Data, Mean, self.PSigma,
                                                            test_module.GT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too low population mean
        Mean = self.Data.Mean - 1.1*self.PSigma*CritValue/math.sqrt(self.Length)
        objTest = self.TestFunction(self.Data, Mean, self.PSigma,
                                                            test_module.GT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        if self.Data.Mean < self.PMean:
            Mean = 2 * self.Data.Mean - self.PMean
        elif self.Data.Mean > self.PMean:
            Mean = self.PMean
        else:
            Mean = self.Data.Mean - 0.1 * self.PSigma
        #make sure to fail due to too high population variance
        Sigma=1.1 * math.sqrt(self.Length) * (self.Data.Mean - Mean) / CritValue
        objTest = self.TestFunction(self.Data, Mean, Sigma, test_module.GT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too low population variance
        Sigma=0.9 * math.sqrt(self.Length) * (self.Data.Mean - Mean) / CritValue
        objTest = self.TestFunction(self.Data, Mean, Sigma, test_module.GT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
    
    def test_LessTest(self):
        """
        Checks the implementation of the 1-sided left-tailed test.
        
        Test ID: TEST-T-710 and TEST-T-702
        Requirement ID: REQ-FUN-710, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        TestValue = math.sqrt(self.Length) * (self.Data.Mean - self.PMean)
        TestValue /= self.PSigma
        p_Value = self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data, self.PMean, self.PSigma,
                                                            test_module.LT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        if p_Value <= 0.05:
            self.assertTrue(objTest.IsRejected)
        else:
            self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to fail due to too high confidence level
        Confidence = 1 - 0.5 * p_Value
        objTest = self.TestFunction(self.Data, self.PMean, self.PSigma,
                                test_module.LT_TEST, Confidence = Confidence)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too low confidence level
        Confidence = 0.9 * (1 - p_Value)
        objTest = self.TestFunction(self.Data, self.PMean, self.PSigma,
                                test_module.LT_TEST, Confidence = Confidence)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        CritValue = self.Model.qf(0.05)
        #make sure to fail due to too low population mean
        Mean = self.Data.Mean - 0.9*self.PSigma*CritValue/math.sqrt(self.Length)
        objTest = self.TestFunction(self.Data, Mean, self.PSigma,
                                                        test_module.LT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too high population mean
        Mean = self.Data.Mean - 1.1*self.PSigma*CritValue/math.sqrt(self.Length)
        objTest = self.TestFunction(self.Data, Mean, self.PSigma,
                                                        test_module.LT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        if self.Data.Mean > self.PMean:
            Mean = 2 * self.Data.Mean - self.PMean
        elif self.Data.Mean < self.PMean:
            Mean = self.PMean
        else:
            Mean = self.Data.Mean + 0.1 * self.PSigma
        #make sure to fail due to too high population variance
        Sigma=1.1 * math.sqrt(self.Length) * (self.Data.Mean - Mean)/ CritValue
        objTest= self.TestFunction(self.Data, Mean, Sigma, test_module.LT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too low population variance
        Sigma=0.9 * math.sqrt(self.Length) * (self.Data.Mean - Mean)/ CritValue
        objTest= self.TestFunction(self.Data, Mean, Sigma, test_module.LT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
    
    def test_NotEqualTest(self):
        """
        Checks the implementation of the 2-sided test.
        
        Test ID: TEST-T-710 and TEST-T-702
        Requirement ID: REQ-FUN-710, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        TestValue = math.sqrt(self.Length) * (self.Data.Mean - self.PMean)
        TestValue /= self.PSigma
        CDF = self.Model.cdf(TestValue)
        if CDF < 0.5:
            p_Value = 2 * self.Model.cdf(TestValue)
        else:
            p_Value = 2 * (1 - CDF)
        objTest = self.TestFunction(self.Data, self.PMean, self.PSigma,
                                                        test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        if p_Value <= 0.05:
            self.assertTrue(objTest.IsRejected)
        else:
            self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to fail due to too high confidence level
        Confidence = 1 - 0.5 * p_Value
        objTest = self.TestFunction(self.Data, self.PMean, self.PSigma,
                                test_module.NEQ_TEST, Confidence = Confidence)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too low confidence level
        Confidence = 0.9 * (1 - p_Value)
        objTest = self.TestFunction(self.Data, self.PMean, self.PSigma,
                                test_module.NEQ_TEST, Confidence = Confidence)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        CritValue = self.Model.qf(0.025)
        #make sure to fail due to too low difference with the population mean
        Mean = self.Data.Mean - 0.9*self.PSigma*CritValue/math.sqrt(self.Length)
        objTest = self.TestFunction(self.Data, Mean, self.PSigma,
                                                        test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        Mean = self.Data.Mean + 0.9*self.PSigma*CritValue/math.sqrt(self.Length)
        objTest = self.TestFunction(self.Data, Mean, self.PSigma,
                                                        test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too high difference with the population mean
        Mean = self.Data.Mean - 1.1*self.PSigma*CritValue/math.sqrt(self.Length)
        objTest = self.TestFunction(self.Data, Mean, self.PSigma,
                                                        test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        Mean = self.Data.Mean + 1.1*self.PSigma*CritValue/math.sqrt(self.Length)
        objTest = self.TestFunction(self.Data, Mean, self.PSigma,
                                                        test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        if self.Data.Mean > self.PMean:
            Mean = 2 * self.Data.Mean - self.PMean
        elif self.Data.Mean < self.PMean:
            Mean = self.PMean
        else:
            Mean = self.Data.Mean + 0.1 * self.PSigma
        #make sure to fail due to too high population variance
        Sigma=1.1 * math.sqrt(self.Length) * (self.Data.Mean - Mean)/ CritValue
        objTest= self.TestFunction(self.Data, Mean, Sigma, test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too low population variance
        Sigma=0.9 * math.sqrt(self.Length) * (self.Data.Mean - Mean)/ CritValue
        objTest= self.TestFunction(self.Data, Mean, Sigma, test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_TestResult)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_z_test)

TestSuite = unittest.TestSuite()

TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting statistics_lib.stat_tests module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)