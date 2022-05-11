#usr/bin/python3
"""
Module statistics_lib.Tests.UT007_stat_tests

Set of unit tests on the module stastics_lib.stat_tests. See the test
plan / report TE007_stat_tests.md
"""


__version__= '1.0.0.0'
__date__ = '11-05-2022'
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
        """
        Cleaning up after the tests. Done only once.
        
        Version 1.0.0.0
        """
        del cls.Data
        cls.Data = None
        del cls.Model
        cls.Model = None
    
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

class Test_t_test(unittest.TestCase):
    """
    Unit tests for the function t_test from the module
    statistics_lib.stat_tests.
    
    Implements tests: TEST-T-720, TEST-T-700, TEST-T-701 and TEST-T-702.
    
    Covers requirements: REQ-FUN-720, REQ-AWM-700, REQ-AWM-701, REQ-SIO-700,
    REQ-SIO-701 and REQ-SIO-702.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        
        Version 1.0.0.0
        """
        cls.TestFunction = staticmethod(test_module.t_test)
        cls.PMean = random.randint(-2, 1) + random.random()
        Sigma = 0.5 + random.random()
        cls.Length = random.randint(10, 20)
        objGenerator = Gaussian(cls.PMean, Sigma)
        cls.Data = Statistics1D([objGenerator.random()
                                                    for _ in range(cls.Length)])
        cls.BadDataType = (1, 1.0, [1, 2.0], (1, 3), int, float, list, tuple,
                                            bool, True, None, {'a':1}, 'test')
        cls.NotReal = ([1, 2.0], (1, 3), int, float, list, tuple, bool,
                                                None, {'a':1}, cls.Data, 'test')
        cls.NotFloat = ([1, 2.0], (1, 3), int, float, list, tuple, bool, True,
                                            None, {'a':1}, cls.Data, 'test', 1)
        cls.Model = Student(Degree = cls.Length - 1)
    
    @classmethod
    def tearDownClass(cls) -> None:
        """
        Cleaning up after the tests. Done only once.
        
        Version 1.0.0.0
        """
        del cls.Data
        cls.Data = None
        del cls.Model
        cls.Model = None
    
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
                self.TestFunction(gItem, 1.0, test_module.GT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, 1.0, test_module.LT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, 1.0, test_module.NEQ_TEST)
            #Type argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, gItem)
        for gItem in self.NotReal:
            #Mean argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, gItem, test_module.GT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, gItem, test_module.LT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, gItem, test_module.NEQ_TEST)
        for gItem in self.NotFloat:
            #Confidence keyword argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, test_module.GT_TEST,
                                                            Confidence = gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, test_module.LT_TEST,
                                                            Confidence = gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 1.0, test_module.NEQ_TEST,
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
            self.TestFunction(self.Data, 1.0, test_module.GT_TEST,
                                                            Confidence = 0.0)
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data, 1.0, test_module.GT_TEST,
                                                            Confidence = 1.0)
        for _ in range(10):
            gValue = random.randint(1, 10)
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, 1.0, test_module.GT_TEST,
                                        Confidence = gValue + random.random())
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, 1.0, test_module.GT_TEST,
                                        Confidence = -gValue + random.random())
        #special case
        Data = Statistics1D([1])
        with self.assertRaises(ValueError):
            self.TestFunction(Data, 1.0, test_module.GT_TEST)
    
    def test_GreaterTest(self):
        """
        Checks the implementation of the 1-sided right-tailed test.
        
        Test ID: TEST-T-720 and TEST-T-702
        Requirement ID: REQ-FUN-720, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        Sigma = self.Data.FullSigma
        TestValue = math.sqrt(self.Length - 1) * (self.Data.Mean - self.PMean)
        TestValue /= Sigma
        p_Value = 1 - self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data, self.PMean, test_module.GT_TEST)
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
        objTest = self.TestFunction(self.Data, self.PMean,
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
        objTest = self.TestFunction(self.Data, self.PMean,
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
        Mean=self.Data.Mean - 0.9*Sigma * CritValue / math.sqrt(self.Length - 1)
        objTest = self.TestFunction(self.Data, Mean, test_module.GT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too low population mean
        Mean=self.Data.Mean - 1.1*Sigma * CritValue / math.sqrt(self.Length - 1)
        objTest = self.TestFunction(self.Data, Mean, test_module.GT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
    
    def test_LessTest(self):
        """
        Checks the implementation of the 1-sided left-tailed test.
        
        Test ID: TEST-T-720 and TEST-T-702
        Requirement ID: REQ-FUN-720, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        Sigma = self.Data.FullSigma
        TestValue = math.sqrt(self.Length - 1) * (self.Data.Mean - self.PMean)
        TestValue /= Sigma
        p_Value = self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data, self.PMean, test_module.LT_TEST)
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
        objTest = self.TestFunction(self.Data, self.PMean,
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
        objTest = self.TestFunction(self.Data, self.PMean,
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
        Mean=self.Data.Mean - 0.9*Sigma * CritValue / math.sqrt(self.Length - 1)
        objTest = self.TestFunction(self.Data, Mean, test_module.LT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too high population mean
        Mean=self.Data.Mean - 1.1*Sigma * CritValue / math.sqrt(self.Length - 1)
        objTest = self.TestFunction(self.Data, Mean, test_module.LT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
    
    def test_NotEqualTest(self):
        """
        Checks the implementation of the 2-sided test.
        
        Test ID: TEST-T-720 and TEST-T-702
        Requirement ID: REQ-FUN-720, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        Sigma = self.Data.FullSigma
        TestValue = math.sqrt(self.Length - 1) * (self.Data.Mean - self.PMean)
        TestValue /= Sigma
        CDF = self.Model.cdf(TestValue)
        if CDF < 0.5:
            p_Value = 2 * self.Model.cdf(TestValue)
        else:
            p_Value = 2 * (1 - CDF)
        objTest = self.TestFunction(self.Data, self.PMean, test_module.NEQ_TEST)
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
        objTest = self.TestFunction(self.Data, self.PMean,
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
        objTest = self.TestFunction(self.Data, self.PMean,
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
        Mean=self.Data.Mean - 0.9*Sigma * CritValue / math.sqrt(self.Length - 1)
        objTest = self.TestFunction(self.Data, Mean, test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        Mean=self.Data.Mean + 0.9*Sigma * CritValue / math.sqrt(self.Length - 1)
        objTest = self.TestFunction(self.Data, Mean, test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too high difference with the population mean
        Mean=self.Data.Mean - 1.1*Sigma * CritValue / math.sqrt(self.Length - 1)
        objTest = self.TestFunction(self.Data, Mean, test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        Mean=self.Data.Mean + 1.1*Sigma * CritValue / math.sqrt(self.Length - 1)
        objTest = self.TestFunction(self.Data, Mean, test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)

class Test_chi_squared_test(unittest.TestCase):
    """
    Unit tests for the function chi_squared_test from the module
    statistics_lib.stat_tests.
    
    Implements tests: TEST-T-730, TEST-T-700, TEST-T-701 and TEST-T-702.
    
    Covers requirements: REQ-FUN-730, REQ-AWM-700, REQ-AWM-701, REQ-SIO-700,
    REQ-SIO-701 and REQ-SIO-702.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        
        Version 1.0.0.0
        """
        cls.TestFunction = staticmethod(test_module.chi_squared_test)
        Mean = random.randint(-2, 1) + random.random()
        cls.PSigma = 0.5 + random.random()
        cls.Length = random.randint(10, 20)
        objGenerator = Gaussian(Mean, cls.PSigma)
        cls.Data = Statistics1D([objGenerator.random()
                                                    for _ in range(cls.Length)])
        cls.BadDataType = (1, 1.0, [1, 2.0], (1, 3), int, float, list, tuple,
                                            bool, True, None, {'a':1}, 'test')
        cls.NotReal = ([1, 2.0], (1, 3), int, float, list, tuple, bool,
                                                None, {'a':1}, cls.Data, 'test')
        cls.NotFloat = ([1, 2.0], (1, 3), int, float, list, tuple, bool, True,
                                            None, {'a':1}, cls.Data, 'test', 1)
        cls.Model = ChiSquared(Degree = cls.Length - 1)
    
    @classmethod
    def tearDownClass(cls) -> None:
        """
        Cleaning up after the tests. Done only once.
        
        Version 1.0.0.0
        """
        del cls.Data
        cls.Data = None
        del cls.Model
        cls.Model = None
    
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
                self.TestFunction(gItem, 0.5, test_module.GT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, 0.5, test_module.LT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, 0.5, test_module.NEQ_TEST)
            #Type argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 0.5, gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 0.5, gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 0.5, gItem)
        for gItem in self.NotReal:
            #Sigma argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, gItem, test_module.GT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, gItem, test_module.LT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, gItem, test_module.NEQ_TEST)
        for gItem in self.NotFloat:
            #Confidence keyword argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 0.5, test_module.GT_TEST,
                                                            Confidence = gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 0.5, test_module.LT_TEST,
                                                            Confidence = gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data, 0.5, test_module.NEQ_TEST,
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
            self.TestFunction(self.Data, 0, test_module.GT_TEST)
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data, 0.0, test_module.GT_TEST)
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data, 0.5, test_module.GT_TEST,
                                                            Confidence = 0.0)
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data, 0.5, test_module.GT_TEST,
                                                            Confidence = 1.0)
        for _ in range(10):
            gValue = random.randint(1, 10)
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, -gValue, test_module.GT_TEST)
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, -gValue + random.random(),
                                                            test_module.GT_TEST)
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, 0.5, test_module.GT_TEST,
                                        Confidence = gValue + random.random())
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data, 0.5, test_module.GT_TEST,
                                        Confidence = -gValue + random.random())
        #special case
        Data = Statistics1D([1])
        with self.assertRaises(ValueError):
            self.TestFunction(Data, 0.5, test_module.GT_TEST)
    
    def test_GreaterTest(self):
        """
        Checks the implementation of the 1-sided right-tailed test.
        
        Test ID: TEST-T-730 and TEST-T-702
        Requirement ID: REQ-FUN-730, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        TestValue= self.Length * self.Data.FullVar / (self.PSigma * self.PSigma)
        p_Value = 1 - self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data, self.PSigma, test_module.GT_TEST)
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
        objTest = self.TestFunction(self.Data, self.PSigma,
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
        objTest = self.TestFunction(self.Data, self.PSigma,
                                test_module.GT_TEST, Confidence = Confidence)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        CritValue = self.Model.qf(0.95)
        #make sure to fail due to too high population variance
        Sigma= 1.1 * math.sqrt(self.Data.N / CritValue) * self.Data.FullSigma
        objTest = self.TestFunction(self.Data, Sigma, test_module.GT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too low population variance
        Sigma= 0.9 * math.sqrt(self.Data.N / CritValue) * self.Data.FullSigma
        objTest = self.TestFunction(self.Data, Sigma, test_module.GT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
    
    def test_LessTest(self):
        """
        Checks the implementation of the 1-sided left-tailed test.
        
        Test ID: TEST-T-730 and TEST-T-702
        Requirement ID: REQ-FUN-730, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        TestValue= self.Length * self.Data.FullVar / (self.PSigma * self.PSigma)
        p_Value = self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data, self.PSigma, test_module.LT_TEST)
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
        objTest = self.TestFunction(self.Data, self.PSigma,
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
        objTest = self.TestFunction(self.Data, self.PSigma,
                                test_module.LT_TEST, Confidence = Confidence)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        CritValue = self.Model.qf(0.05)
        #make sure to fail due to too low population variance
        Sigma= 0.9 * math.sqrt(self.Data.N / CritValue) * self.Data.FullSigma
        objTest= self.TestFunction(self.Data, Sigma, test_module.LT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to pass due to too high population variance
        Sigma= 1.1 * math.sqrt(self.Data.N / CritValue) * self.Data.FullSigma
        objTest= self.TestFunction(self.Data, Sigma, test_module.LT_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
    
    def test_NotEqualTest(self):
        """
        Checks the implementation of the 2-sided test.
        
        Test ID: TEST-T-730 and TEST-T-702
        Requirement ID: REQ-FUN-730, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        TestValue= self.Length * self.Data.FullVar / (self.PSigma * self.PSigma)
        CDF = self.Model.cdf(TestValue)
        if CDF < 0.5:
            p_Value = 2 * self.Model.cdf(TestValue)
        else:
            p_Value = 2 * (1 - CDF)
        objTest= self.TestFunction(self.Data, self.PSigma, test_module.NEQ_TEST)
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
        objTest = self.TestFunction(self.Data, self.PSigma,
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
        objTest = self.TestFunction(self.Data, self.PSigma,
                                test_module.NEQ_TEST, Confidence = Confidence)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertAlmostEqual(objTest.p_Value, p_Value)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        CritValue = self.Model.qf(0.025)
        #make sure to pass due to too high population variance
        Sigma= 1.1 * math.sqrt(self.Data.N / CritValue) * self.Data.FullSigma
        objTest= self.TestFunction(self.Data, Sigma, test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        CritValue = self.Model.qf(0.975)
        #make sure to pass due to too low population variance
        Sigma= 0.9 * math.sqrt(self.Data.N / CritValue) * self.Data.FullSigma
        objTest= self.TestFunction(self.Data, Sigma, test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest
        #make sure to fail due to too low difference with population variance
        Sigma= self.Data.FullSigma
        objTest= self.TestFunction(self.Data, Sigma, test_module.NEQ_TEST)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertIsInstance(objTest.Report, str)
        del objTest

class Test_unpaired_t_test(unittest.TestCase):
    """
    Unit tests for the function unpaired_t_test from the module
    statistics_lib.stat_tests.
    
    Implements tests: TEST-T-740, TEST-T-700, TEST-T-701 and TEST-T-702.
    
    Covers requirements: REQ-FUN-740, REQ-AWM-700, REQ-AWM-701, REQ-SIO-700,
    REQ-SIO-701 and REQ-SIO-702.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        
        Version 1.0.0.0
        """
        cls.TestFunction = staticmethod(test_module.unpaired_t_test)
        PMean1 = random.randint(-2, 1) + random.random()
        PSigma1 = 0.4 + random.random()
        cls.Length1 = random.randint(10, 20)
        PMean2 = random.randint(-2, 1) + random.random() + 0.2
        PSigma2 = 0.6 + random.random()
        cls.Length2 = random.randint(10, 20)
        objGenerator = Gaussian(PMean1, PSigma1)
        cls.Data1 = Statistics1D([objGenerator.random()
                                                for _ in range(cls.Length1)])
        del objGenerator
        objGenerator = Gaussian(PMean2, PSigma2)
        cls.Data2 = Statistics1D([objGenerator.random()
                                                for _ in range(cls.Length2)])
        cls.BadDataType = (1, 1.0, [1, 2.0], (1, 3), int, float, list, tuple,
                                            bool, True, None, {'a':1}, 'test')
        cls.NotFloat = ([1, 2.0], (1, 3), int, float, list, tuple, bool, True,
                                        None, {'a':1}, cls.Data1, 'test', 1)
        cls.Model = Student(Degree = cls.Length1 + cls.Length2 - 2)
        del objGenerator
    
    @classmethod
    def tearDownClass(cls) -> None:
        """
        Cleaning up after the tests. Done only once.
        
        Version 1.0.0.0
        """
        del cls.Data1
        del cls.Data2
        cls.Data1 = None
        cls.Data2 = None
        del cls.Model
        cls.Model = None
    
    def test_TypeError(self):
        """
        Checks that TypeError (or its sub-class) is raised in response to the
        unexpected / inappropriate data type of, at least, one argument.
        
        Test ID: TEST-T-700
        Requirement ID: REQ-AWM-700
        
        Version 1.0.0.0
        """
        for gItem in self.BadDataType:
            #Data1 argument
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, self.Data2, test_module.GT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, self.Data2, test_module.LT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(gItem, self.Data2, test_module.NEQ_TEST)
            #Data2 argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, gItem, test_module.GT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, gItem, test_module.LT_TEST)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, gItem, test_module.NEQ_TEST)
            #Type argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, self.Data2, gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, self.Data2, gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, self.Data2, gItem)
        for gItem in self.NotFloat:
            #Confidence keyword argument
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                            Confidence = gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, self.Data2, test_module.LT_TEST,
                                                            Confidence = gItem)
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, self.Data2, test_module.NEQ_TEST,
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
            self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                            Confidence = 0.0)
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                            Confidence = 1.0)
        for _ in range(10):
            gValue = random.randint(1, 10)
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                        Confidence = gValue + random.random())
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                        Confidence = -gValue + random.random())
        #special case
        Data = Statistics1D([1])
        with self.assertRaises(ValueError):
            self.TestFunction(Data, self.Data2, test_module.GT_TEST)
        with self.assertRaises(ValueError):
            self.TestFunction(self.Data1, Data, test_module.GT_TEST)
    
    def test_GreaterTest(self):
        """
        Checks the implementation of the 1-sided right-tailed test.
        
        Test ID: TEST-T-740 and TEST-T-702
        Requirement ID: REQ-FUN-740, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        N1 = self.Data1.N
        N2 = self.Data2.N
        Temp = (N1 - 1) * self.Data1.FullVar + (N2 - 1) * self.Data2.FullVar
        Temp /= N1 + N2 - 2
        Temp *= (N1 + N2) / (N1 * N2)
        TestValue = (self.Data1.Mean - self.Data2.Mean) / math.sqrt(Temp)
        p_Value = 1 - self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.GT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.GT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
    
    def test_LessTest(self):
        """
        Checks the implementation of the 1-sided left-tailed test.
        
        Test ID: TEST-T-740 and TEST-T-702
        Requirement ID: REQ-FUN-740, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        N1 = self.Data1.N
        N2 = self.Data2.N
        Temp = (N1 - 1) * self.Data1.FullVar + (N2 - 1) * self.Data2.FullVar
        Temp /= N1 + N2 - 2
        Temp *= (N1 + N2) / (N1 * N2)
        TestValue = (self.Data1.Mean - self.Data2.Mean) / math.sqrt(Temp)
        p_Value = self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.LT_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.LT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.LT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
    
    def test_NotEqualTest(self):
        """
        Checks the implementation of the 2-sided test.
        
        Test ID: TEST-T-740 and TEST-T-702
        Requirement ID: REQ-FUN-740, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        N1 = self.Data1.N
        N2 = self.Data2.N
        Temp = (N1 - 1) * self.Data1.FullVar + (N2 - 1) * self.Data2.FullVar
        Temp /= N1 + N2 - 2
        Temp *= (N1 + N2) / (N1 * N2)
        TestValue = (self.Data1.Mean - self.Data2.Mean) / math.sqrt(Temp)
        CDF = self.Model.cdf(TestValue)
        if CDF < 0.5:
            p_Value = 2 * self.Model.cdf(TestValue)
        else:
            p_Value = 2 * (1 - CDF)
        objTest= self.TestFunction(self.Data1, self.Data2, test_module.NEQ_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.NEQ_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.NEQ_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest

class Test_paired_t_test(Test_unpaired_t_test):
    """
    Unit tests for the function paired_t_test from the module
    statistics_lib.stat_tests.
    
    Implements tests: TEST-T-750, TEST-T-700, TEST-T-701 and TEST-T-702.
    
    Covers requirements: REQ-FUN-750, REQ-AWM-700, REQ-AWM-701, REQ-SIO-700,
    REQ-SIO-701 and REQ-SIO-702.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        
        Version 1.0.0.0
        """
        cls.TestFunction = staticmethod(test_module.paired_t_test)
        PMean1 = random.randint(-2, 1) + random.random()
        PSigma1 = 0.4 + random.random()
        cls.Length = random.randint(10, 20)
        PMean2 = random.randint(-2, 1) + random.random() + 0.2
        PSigma2 = 0.6 + random.random()
        objGenerator = Gaussian(PMean1, PSigma1)
        cls.Data1 = Statistics1D([objGenerator.random()
                                                for _ in range(cls.Length)])
        del objGenerator
        objGenerator = Gaussian(PMean2, PSigma2)
        cls.Data2 = Statistics1D([objGenerator.random()
                                                for _ in range(cls.Length)])
        cls.BadDataType = (1, 1.0, [1, 2.0], (1, 3), int, float, list, tuple,
                                            bool, True, None, {'a':1}, 'test')
        cls.NotReal = ([1, 2.0], (1, 3), int, float, list, tuple, bool,
                                            None, {'a':1}, cls.Data1, 'test')
        cls.NotFloat = ([1, 2.0], (1, 3), int, float, list, tuple, bool, True,
                                        None, {'a':1}, cls.Data1, 'test', 1)
        cls.Model = Student(Degree = cls.Length - 1)
        del objGenerator
        TempSeq = [cls.Data1.Values[Index] - cls.Data2.Values[Index]
                                                for Index in range(cls.Length)]
        objData = Statistics1D(TempSeq)
        cls.Mean = objData.Mean
        cls.Sigma = objData.FullSigma
        del objData
    
    def test_TypeError(self):
        """
        Checks that TypeError (or its sub-class) is raised in response to the
        unexpected / inappropriate data type of, at least, one argument.
        
        Test ID: TEST-T-700
        Requirement ID: REQ-AWM-700
        
        Version 1.0.0.0
        """
        super().test_TypeError()
        for gItem in self.NotReal:
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                                Bias = gItem)
    
    def test_ValueError(self):
        """
        Checks that ValueError (or its sub-class) is raised in response to the
        unexpected / inappropriate value of, at least, one argument.
        
        Test ID: TEST-T-701
        Requirement ID: REQ-AWM-701
        
        Version 1.0.0.0
        """
        super().test_ValueError()
        N = self.Length
        for _ in range(10):
            N1 = N + random.randint(1, 10)
            Data = Statistics1D([1 for _ in range(N1)])
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data1, Data, test_module.GT_TEST)
            del Data
            N2 = N - min(random.randint(1, 10), N - 1)
            Data = Statistics1D([1 for _ in range(N1)])
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data1, Data, test_module.GT_TEST)
            del Data
    
    def test_GreaterTest(self):
        """
        Checks the implementation of the 1-sided right-tailed test.
        
        Test ID: TEST-T-750 and TEST-T-702
        Requirement ID: REQ-FUN-750, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        TestValue = self.Mean * math.sqrt(self.Length - 1) / self.Sigma
        p_Value = 1 - self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.GT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.GT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        CritValue = self.Model.qf(0.95)
        #make sure to pass due to too low bias
        Bias= -0.1 + self.Mean - CritValue*self.Sigma / math.sqrt(self.Length-1)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                                    Bias = Bias)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertLess(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
        #make sure to fail due to too high bias
        Bias= +0.1 + self.Mean - CritValue*self.Sigma / math.sqrt(self.Length-1)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                                    Bias = Bias)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertGreater(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
    
    def test_LessTest(self):
        """
        Checks the implementation of the 1-sided left-tailed test.
        
        Test ID: TEST-T-750 and TEST-T-702
        Requirement ID: REQ-FUN-750, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        TestValue = self.Mean * math.sqrt(self.Length - 1) / self.Sigma
        p_Value = self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.LT_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.LT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.LT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        CritValue = self.Model.qf(0.05)
        #make sure to fail due to too low bias
        Bias= -0.1 + self.Mean - CritValue*self.Sigma / math.sqrt(self.Length-1)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.LT_TEST,
                                                                    Bias = Bias)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertGreater(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
        #make sure to pass due to too high bias
        Bias= +0.1 + self.Mean - CritValue*self.Sigma / math.sqrt(self.Length-1)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.LT_TEST,
                                                                    Bias = Bias)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertLess(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
    
    def test_NotEqualTest(self):
        """
        Checks the implementation of the 2-sided test.
        
        Test ID: TEST-T-750 and TEST-T-702
        Requirement ID: REQ-FUN-750, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        TestValue = self.Mean * math.sqrt(self.Length - 1) / self.Sigma
        CDF = self.Model.cdf(TestValue)
        if CDF < 0.5:
            p_Value = 2 * self.Model.cdf(TestValue)
        else:
            p_Value = 2 * (1 - CDF)
        objTest= self.TestFunction(self.Data1, self.Data2, test_module.NEQ_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.NEQ_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.NEQ_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        CritValue = self.Model.qf(0.975)
        #make sure to pass due to too low bias - right tail
        Bias= -0.1 + self.Mean - CritValue*self.Sigma / math.sqrt(self.Length-1)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                                    Bias = Bias)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertLess(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
        CritValue = self.Model.qf(0.025)
        #make sure to pass due to too high bias - left tail
        Bias= +0.1 + self.Mean - CritValue*self.Sigma / math.sqrt(self.Length-1)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.LT_TEST,
                                                                    Bias = Bias)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertLess(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
        #make sure to fail due to too exact bias value matching the difference
        Bias= self.Mean
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                                    Bias = Bias)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertIsInstance(objTest.p_Value, float)
        self.assertGreater(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)

class Test_welch_t_test(Test_unpaired_t_test):
    """
    Unit tests for the function welch_t_test from the module
    statistics_lib.stat_tests.
    
    Implements tests: TEST-T-750, TEST-T-700, TEST-T-701 and TEST-T-702.
    
    Covers requirements: REQ-FUN-750, REQ-AWM-700, REQ-AWM-701, REQ-SIO-700,
    REQ-SIO-701 and REQ-SIO-702.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        
        Version 1.0.0.0
        """
        cls.TestFunction = staticmethod(test_module.welch_t_test)
        PMean1 = random.randint(-2, 1) + random.random()
        PSigma1 = 0.4 + random.random()
        cls.Length1 = random.randint(10, 20)
        PMean2 = random.randint(-2, 1) + random.random() + 0.2
        PSigma2 = 0.6 + random.random()
        cls.Length2 = random.randint(10, 20)
        objGenerator = Gaussian(PMean1, PSigma1)
        cls.Data1 = Statistics1D([objGenerator.random()
                                                for _ in range(cls.Length1)])
        del objGenerator
        objGenerator = Gaussian(PMean2, PSigma2)
        cls.Data2 = Statistics1D([objGenerator.random()
                                                for _ in range(cls.Length2)])
        cls.BadDataType = (1, 1.0, [1, 2.0], (1, 3), int, float, list, tuple,
                                            bool, True, None, {'a':1}, 'test')
        cls.NotFloat = ([1, 2.0], (1, 3), int, float, list, tuple, bool, True,
                                        None, {'a':1}, cls.Data1, 'test', 1)
        NormVar1 = cls.Data1.FullVar / (cls.Data1.N - 1)
        NormVar2 = cls.Data2.FullVar / (cls.Data2.N - 1)
        Divident = math.pow(NormVar1 + NormVar2, 2)
        Divisor = math.pow(NormVar1, 2) / (cls.Data1.N - 1)
        Divisor += math.pow(NormVar2, 2) / (cls.Data2.N - 1)
        Degree = Divident / Divisor
        cls.Model = Student(Degree = Degree)
        del objGenerator
    
    @classmethod
    def tearDownClass(cls) -> None:
        """
        Cleaning up after the tests. Done only once.
        
        Version 1.0.0.0
        """
        del cls.Data1
        del cls.Data2
        cls.Data1 = None
        cls.Data2 = None
        del cls.Model
        cls.Model = None
    
    def test_GreaterTest(self):
        """
        Checks the implementation of the 1-sided right-tailed test.
        
        Test ID: TEST-T-760 and TEST-T-702
        Requirement ID: REQ-FUN-760, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        NormVar1 = self.Data1.FullVar / (self.Data1.N - 1)
        NormVar2 = self.Data2.FullVar / (self.Data2.N - 1)
        Temp = NormVar1 + NormVar2
        TestValue = (self.Data1.Mean - self.Data2.Mean) / math.sqrt(Temp)
        p_Value = 1 - self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.GT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.GT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
    
    def test_LessTest(self):
        """
        Checks the implementation of the 1-sided left-tailed test.
        
        Test ID: TEST-T-760 and TEST-T-702
        Requirement ID: REQ-FUN-760, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        NormVar1 = self.Data1.FullVar / (self.Data1.N - 1)
        NormVar2 = self.Data2.FullVar / (self.Data2.N - 1)
        Temp = NormVar1 + NormVar2
        TestValue = (self.Data1.Mean - self.Data2.Mean) / math.sqrt(Temp)
        p_Value = self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.LT_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.LT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.LT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
    
    def test_NotEqualTest(self):
        """
        Checks the implementation of the 2-sided test.
        
        Test ID: TEST-T-760 and TEST-T-702
        Requirement ID: REQ-FUN-760, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        NormVar1 = self.Data1.FullVar / (self.Data1.N - 1)
        NormVar2 = self.Data2.FullVar / (self.Data2.N - 1)
        Temp = NormVar1 + NormVar2
        TestValue = (self.Data1.Mean - self.Data2.Mean) / math.sqrt(Temp)
        CDF = self.Model.cdf(TestValue)
        if CDF < 0.5:
            p_Value = 2 * self.Model.cdf(TestValue)
        else:
            p_Value = 2 * (1 - CDF)
        objTest= self.TestFunction(self.Data1, self.Data2, test_module.NEQ_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.NEQ_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.NEQ_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest

class Test_f_test(Test_unpaired_t_test):
    """
    Unit tests for the function f_test from the module
    statistics_lib.stat_tests.
    
    Implements tests: TEST-T-770, TEST-T-700, TEST-T-701 and TEST-T-702.
    
    Covers requirements: REQ-FUN-770, REQ-AWM-700, REQ-AWM-701, REQ-SIO-700,
    REQ-SIO-701 and REQ-SIO-702.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        
        Version 1.0.0.0
        """
        cls.TestFunction = staticmethod(test_module.f_test)
        PMean1 = random.randint(-2, 1) + random.random()
        PSigma1 = 0.4 + random.random()
        cls.Length1 = random.randint(10, 20)
        PMean2 = random.randint(-2, 1) + random.random() + 0.2
        PSigma2 = 0.6 + random.random()
        cls.Length2 = random.randint(10, 20)
        objGenerator = Gaussian(PMean1, PSigma1)
        cls.Data1 = Statistics1D([objGenerator.random()
                                                for _ in range(cls.Length1)])
        del objGenerator
        objGenerator = Gaussian(PMean2, PSigma2)
        cls.Data2 = Statistics1D([objGenerator.random()
                                                for _ in range(cls.Length2)])
        cls.BadDataType = (1, 1.0, [1, 2.0], (1, 3), int, float, list, tuple,
                                            bool, True, None, {'a':1}, 'test')
        cls.NotFloat = ([1, 2.0], (1, 3), int, float, list, tuple, bool, True,
                                        None, {'a':1}, cls.Data1, 'test', 1)
        cls.NotReal = ([1, 2.0], (1, 3), int, float, list, tuple, bool, None,
                                                    {'a':1}, cls.Data1, 'test')
        cls.Model = F_Distribution(Degree1 = cls.Length1 - 1,
                                                    Degree2 = cls.Length2 -1)
        del objGenerator
    
    def test_TypeError(self):
        """
        Checks that TypeError (or its sub-class) is raised in response to the
        unexpected / inappropriate data type of, at least, one argument.
        
        Test ID: TEST-T-700
        Requirement ID: REQ-AWM-700
        
        Version 1.0.0.0
        """
        super().test_TypeError()
        for gItem in self.NotReal:
            with self.assertRaises(TypeError):
                self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                                Delta = gItem)
    
    def test_ValueError(self):
        """
        Checks that ValueError (or its sub-class) is raised in response to the
        unexpected / inappropriate value of, at least, one argument.
        
        Test ID: TEST-T-701
        Requirement ID: REQ-AWM-701
        
        Version 1.0.0.0
        """
        super().test_ValueError()
        for _ in range(10):
            Value = - random.randint(1, 10)
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                                Delta = Value)
            Value += random.random()
            with self.assertRaises(ValueError):
                self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST,
                                                                Delta = Value)
    
    def test_GreaterTest(self):
        """
        Checks the implementation of the 1-sided right-tailed test.
        
        Test ID: TEST-T-770 and TEST-T-702
        Requirement ID: REQ-FUN-770, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        N1 = self.Data1.N
        N2 = self.Data2.N
        Temp = (N2 - 1) * N1 / ((N1 - 1) * N2)
        TestValue = Temp * self.Data1.FullVar / self.Data2.FullVar
        p_Value = 1 - self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.GT_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.GT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.GT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        CritValue = self.Model.qf(0.95)
        Delta = CritValue / TestValue
        #make sure to fail using Delta correction
        objTest = self.TestFunction(self.Data1, self.Data2,
                                    test_module.GT_TEST, Delta = 0.9 * Delta)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertGreater(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
        #make sure to pass using Delta correction
        objTest = self.TestFunction(self.Data1, self.Data2,
                                    test_module.GT_TEST, Delta = 1.1 * Delta)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertLess(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
    
    def test_LessTest(self):
        """
        Checks the implementation of the 1-sided left-tailed test.
        
        Test ID: TEST-T-770 and TEST-T-702
        Requirement ID: REQ-FUN-770, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        N1 = self.Data1.N
        N2 = self.Data2.N
        Temp = (N2 - 1) * N1 / ((N1 - 1) * N2)
        TestValue = Temp * self.Data1.FullVar / self.Data2.FullVar
        p_Value = self.Model.cdf(TestValue)
        objTest = self.TestFunction(self.Data1, self.Data2, test_module.LT_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.LT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.LT_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        CritValue = self.Model.qf(0.05)
        Delta = CritValue / TestValue
        #make sure to fail using Delta correction
        objTest = self.TestFunction(self.Data1, self.Data2,
                                    test_module.LT_TEST, Delta = 1.1 * Delta)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertGreater(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
        #make sure to pass using Delta correction
        objTest = self.TestFunction(self.Data1, self.Data2,
                                    test_module.LT_TEST, Delta = 0.9 * Delta)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertLess(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
    
    def test_NotEqualTest(self):
        """
        Checks the implementation of the 2-sided test.
        
        Test ID: TEST-T-770 and TEST-T-702
        Requirement ID: REQ-FUN-770, REQ-SIO-700, REQ-SIO-701 and REQ-SIO-702.
        
        Version 1.0.0.0
        """
        #actual one with the default 95 % confidence
        N1 = self.Data1.N
        N2 = self.Data2.N
        Temp = (N2 - 1) * N1 / ((N1 - 1) * N2)
        TestValue = Temp * self.Data1.FullVar / self.Data2.FullVar
        CDF = self.Model.cdf(TestValue)
        if CDF < 0.5:
            p_Value = 2 * self.Model.cdf(TestValue)
        else:
            p_Value = 2 * (1 - CDF)
        objTest= self.TestFunction(self.Data1, self.Data2, test_module.NEQ_TEST)
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
        if p_Value > 0.01:
            Confidence = 1 - 0.9 * p_Value
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.NEQ_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertFalse(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to pass due to too low confidence level
        if p_Value < 0.99:
            Confidence = 0.9 * (1 - p_Value)
            objTest = self.TestFunction(self.Data1, self.Data2,
                                test_module.NEQ_TEST, Confidence = Confidence)
            self.assertIsInstance(objTest, test_module.TestResult)
            self.assertIsInstance(objTest.IsRejected, bool)
            self.assertTrue(objTest.IsRejected)
            self.assertIsInstance(objTest.p_Value, float)
            self.assertAlmostEqual(objTest.p_Value, p_Value)
            self.assertIsInstance(objTest.Report, str)
            del objTest
        #make sure to fail using Delta correction
        objTest = self.TestFunction(self.Data1, self.Data2,
                                    test_module.NEQ_TEST, Delta = 1 / TestValue)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertFalse(objTest.IsRejected)
        self.assertGreater(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
        #make sure to pass using Delta correction - right tail
        CritValue = self.Model.qf(0.975)
        Delta = CritValue / TestValue
        objTest = self.TestFunction(self.Data1, self.Data2,
                                    test_module.NEQ_TEST, Delta = 1.1 * Delta)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertLess(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)
        #make sure to pass using Delta correction - left tail
        CritValue = self.Model.qf(0.025)
        Delta = CritValue / TestValue
        objTest = self.TestFunction(self.Data1, self.Data2,
                                    test_module.NEQ_TEST, Delta = 0.9 * Delta)
        self.assertIsInstance(objTest, test_module.TestResult)
        self.assertIsInstance(objTest.IsRejected, bool)
        self.assertTrue(objTest.IsRejected)
        self.assertLess(objTest.p_Value, 0.05)
        self.assertIsInstance(objTest.Report, str)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_TestResult)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_z_test)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_t_test)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_chi_squared_test)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_unpaired_t_test)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_paired_t_test)
TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_welch_t_test)
TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(Test_f_test)

TestSuite = unittest.TestSuite()

TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6, TestSuite7, TestSuite8])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting statistics_lib.stat_tests module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)