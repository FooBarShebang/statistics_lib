#usr/bin/python3
"""
Module statistics_lib.Tests.UT004_distribution_classes

Set of unit tests on the module stastics_lib.distribution_classes. See the test
plan / report TE004_distribution_classes.md
"""


__version__= '1.0.0.0'
__date__ = '16-03-2022'
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

import statistics_lib.distribution_classes as test_module

import statistics_lib.special_functions as sf

#globals

FLOAT_CHECK_PRECISION = 5 #digits after comma, mostly due to precision of
#+ the reference tables + internal Python implementation of the special
#+ functions

#classes

#+ test cases

class Test_ContinuousDistributionABC(unittest.TestCase):
    """
    Unittests for ContinuousDistributionABC class from the module
    statistics_lib.distribution_classes, which is an abstract class / prototype.
    
    Also defines some template methods, re-used by the concrete sub-classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = test_module.ContinuousDistributionABC
        cls.Properties = ('Mean', 'Median', 'Q1', 'Q3', 'Min', 'Max', 'Var',
                            'Sigma', 'Skew', 'Kurt')
        cls.Parameters = tuple()
        cls.Methods = ('pdf', 'cdf', 'qf', 'getQuantile', 'getHistogram',
                                                                    'random')
    
    def test_init(self) -> None:
        """
        Checks that the class cannot be instantiated.
        
        Test ID: TEST-T-400
        Requirements: REQ-FUN-401
        """
        with self.assertRaises(TypeError):
            self.TestClass()
    
    def test_hasAttributes(self) -> None:
        """
        Checks that the class has all required attributes, w/o instantiation.
        
        Test ID: TEST-T-401
        Requirements: REQ-FUN-401
        """
        for Name in self.Properties:
            self.assertTrue(hasattr(self.TestClass, Name))
        for Name in self.Parameters:
            self.assertTrue(hasattr(self.TestClass, Name))
        for Name in self.Methods:
            self.assertTrue(hasattr(self.TestClass, Name))

class Test_DiscreteDistributionABC(Test_ContinuousDistributionABC):
    """
    Unittests for DiscreteDistributionABC class from the module
    statistics_lib.distribution_classes, which is an abstract class / prototype.
    
    Also defines some template methods, re-used by the concrete sub-classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.DiscreteDistributionABC

class Test_Z_Distribution(Test_ContinuousDistributionABC):
    """
    Unittests for Z_Distribution class from the module
    statistics_lib.distribution_classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Z_Distribution
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        self.DefArguments = None
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-400
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            objTest = self.TestClass()
            self.assertEqual(objTest.Mean, 0)
            self.assertEqual(objTest.Sigma, 1)
            self.assertEqual(objTest.Median, 0)
            self.assertEqual(objTest.Var, 1)
            self.assertEqual(objTest.Skew, 0)
            self.assertEqual(objTest.Kurt, 0)
            self.assertEqual(objTest.Min, -math.inf)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Q1, -0.6744899,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, 0.6744899,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_hasAttributes(self) -> None:
        """
        Checks that the class' instance has all required attributes.
        
        Test ID: TEST-T-401
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            objTest = self.TestClass()
            for Name in self.Properties:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Parameters:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Methods:
                self.assertTrue(hasattr(objTest, Name))
            del objTest
    
    def test_Properties(self) -> None:
        """
        Checks that the class has all required properties, and they are
        read-only unless the statistical property is also a parameter of the
        distribution. Also checks that all statistical properties are real
        numbers.
        
        Test ID: TEST-T-403
        Requirements: REQ-FUN-403
        """
        if not (self.DefArguments is None):
            objTest = self.TestClass(*self.DefArguments)
        else:
            objTest = self.TestClass()
        for Name in self.Properties:
            self.assertIsInstance(getattr(objTest, Name), (int, float))
            with self.assertRaises(AttributeError):
                delattr(objTest, Name)
            if not (Name in self.Parameters):
                with self.assertRaises(AttributeError):
                    setattr(objTest, Name, 1)
        del objTest
    
    def test_pdf_TypeError(self) -> None:
        """
        Checks that TypeError or its sub-class exception is raised if the
        function being tested recieves improper data type argument(s).
        
        Test ID: TEST-T-407
        Requirements: REQ-AWM-400
        """
        if not (self.DefArguments is None):
            objTest = self.TestClass(*self.DefArguments)
        else:
            objTest = self.TestClass()
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                objTest.pdf(Value)
        del objTest
    
    def test_cdf_TypeError(self) -> None:
        """
        Checks that TypeError or its sub-class exception is raised if the
        function being tested recieves improper data type argument(s).
        
        Test ID: TEST-T-407
        Requirements: REQ-AWM-400
        """
        if not (self.DefArguments is None):
            objTest = self.TestClass(*self.DefArguments)
        else:
            objTest = self.TestClass()
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                objTest.cdf(Value)
        del objTest
    
    def test_qf_TypeError(self) -> None:
        """
        Checks that TypeError or its sub-class exception is raised if the
        function being tested recieves improper data type argument(s).
        
        Test ID: TEST-T-407
        Requirements: REQ-AWM-400
        """
        if not (self.DefArguments is None):
            objTest = self.TestClass(*self.DefArguments)
        else:
            objTest = self.TestClass()
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool, 1, 3, -2):
            with self.assertRaises(TypeError):
                objTest.qf(Value)
        del objTest
    
    def test_qf_ValueError(self) -> None:
        """
        Checks that ValueError or its sub-class exception is raised if the
        function being tested recieves improper value argument(s).
        
        Test ID: TEST-T-408
        Requirements: REQ-AWM-401
        """
        if not (self.DefArguments is None):
            objTest = self.TestClass(*self.DefArguments)
        else:
            objTest = self.TestClass()
        for _ in range(10):
            Value = random.random() + random.randint(1, 10)
            with self.assertRaises(ValueError):
                objTest.qf(Value)
            Value = random.random() - random.randint(1, 10)
            with self.assertRaises(ValueError):
                objTest.qf(Value)
        with self.assertRaises(ValueError):
            objTest.qf(0.0)
        with self.assertRaises(ValueError):
            objTest.qf(1.0)
        del objTest
    
    def test_getQuantile_TypeError(self) -> None:
        """
        Checks that TypeError or its sub-class exception is raised if the
        function being tested recieves improper data type argument(s).
        
        Test ID: TEST-T-407
        Requirements: REQ-AWM-400
        """
        if not (self.DefArguments is None):
            objTest = self.TestClass(*self.DefArguments)
        else:
            objTest = self.TestClass()
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool, 1.0):
            with self.assertRaises(TypeError):
                objTest.getQuantile(Value, 1)
            with self.assertRaises(TypeError):
                objTest.getQuantile(1, Value)
            with self.assertRaises(TypeError):
                objTest.getQuantile(Value, Value)
        del objTest
    
    def test_getQuantile_ValueError(self) -> None:
        """
        Checks that ValueError or its sub-class exception is raised if the
        function being tested recieves improper value argument(s).
        
        Test ID: TEST-T-408
        Requirements: REQ-AWM-401
        """
        if not (self.DefArguments is None):
            objTest = self.TestClass(*self.DefArguments)
        else:
            objTest = self.TestClass()
        for _ in range(10):
            Value = random.randint(1, 10)
            with self.assertRaises(ValueError):
                objTest.getQuantile(-Value, 1)
            with self.assertRaises(ValueError):
                objTest.getQuantile(1, -Value)
            with self.assertRaises(ValueError):
                objTest.getQuantile(-Value, -Value)
            with self.assertRaises(ValueError):
                objTest.getQuantile(2 + Value, 2)
            with self.assertRaises(ValueError):
                objTest.getQuantile(Value, Value)
            with self.assertRaises(ValueError):
                objTest.getQuantile(0, Value)
            with self.assertRaises(ValueError):
                objTest.getQuantile(Value, 0)
        with self.assertRaises(ValueError):
            objTest.getQuantile(0, 0)
        del objTest
    
    def test_getHistogram_TypeError(self) -> None:
        """
        Checks that TypeError or its sub-class exception is raised if the
        function being tested recieves improper data type argument(s).
        
        Test ID: TEST-T-407
        Requirements: REQ-AWM-400
        """
        if not (self.DefArguments is None):
            objTest = self.TestClass(*self.DefArguments)
        else:
            objTest = self.TestClass()
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                objTest.getHistogram(Value, 1, 4)
            with self.assertRaises(TypeError):
                objTest.getHistogram(1, Value, 4)
            with self.assertRaises(TypeError):
                objTest.getHistogram(Value, Value, 4)
            with self.assertRaises(TypeError):
                objTest.getHistogram(Value, Value, Value)
            with self.assertRaises(TypeError):
                objTest.getHistogram(1, 4, Value)
        with self.assertRaises(TypeError):
                objTest.getHistogram(1, 4, 2.0)
        del objTest
    
    def test_getHistogram_ValueError(self) -> None:
        """
        Checks that ValueError or its sub-class exception is raised if the
        function being tested recieves improper value argument(s).
        
        Test ID: TEST-T-408
        Requirements: REQ-AWM-401
        """
        if not (self.DefArguments is None):
            objTest = self.TestClass(*self.DefArguments)
        else:
            objTest = self.TestClass()
        for _ in range(10):
            Value = random.random()
            with self.assertRaises(ValueError):
                objTest.getHistogram(Value, 1 + Value, 1)
            with self.assertRaises(ValueError):
                objTest.getHistogram(Value, 1 + Value, 0)
            with self.assertRaises(ValueError):
                objTest.getHistogram(Value, 1 + Value, - random.randint(1, 10))
            with self.assertRaises(ValueError):
                objTest.getHistogram(Value, Value, 20)
            with self.assertRaises(ValueError):
                objTest.getHistogram(Value + random.random() +0.0001, Value, 20)
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-404
        Requirements ID: REQ-FUN-404
        """
        objTest = self.TestClass()
        for _ in range(100):
            Value = random.randint(-10, 10)
            if random.random() > 0.5:
                Value += random.random()
            TestResult = objTest.pdf(Value)
            self.assertIsInstance(TestResult, float)
            self.assertGreater(TestResult, 0)
            CheckValue = math.exp(-0.5 * Value * Value) / math.sqrt(2 * math.pi)
            self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method.
        
        Test ID: TEST-T-405
        Requirements ID: REQ-FUN-405
        """
        objTest = self.TestClass()
        for _ in range(100):
            Value = random.randint(-10, 10)
            if random.random() > 0.5:
                Value += random.random()
            TestResult = objTest.cdf(Value)
            self.assertIsInstance(TestResult, float)
            self.assertGreaterEqual(TestResult, 0)
            CheckValue = 0.5 * (1 + math.erf(Value / math.sqrt(2)))
            self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
        del objTest
    
    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method.
        
        Test ID: TEST-T-406
        Requirements ID: REQ-FUN-406
        """
        objTest = self.TestClass()
        for _ in range(100):
            Value = random.random()
            if Value < 1.0E-11:
                Value = 1.0E-11
            TestResult = objTest.qf(Value)
            self.assertIsInstance(TestResult, float)
            self.assertGreater(TestResult, objTest.Min)
            self.assertLess(TestResult, objTest.Max)
            CheckValue = math.sqrt(2) * sf.inv_erf(2 * Value - 1)
            self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
        del objTest
    
    def test_getQuantile(self) -> None:
        """
        Checks the implementation of the getQuantile() method.
        
        Test ID: TEST-T-406
        Requirements ID: REQ-FUN-406
        """
        objTest = self.TestClass()
        for _ in range(100):
            k = random.randint(1, 20)
            m = random.randint(1, 20) + k
            TestResult = objTest.getQuantile(k, m)
            self.assertIsInstance(TestResult, float)
            self.assertGreater(TestResult, objTest.Min)
            self.assertLess(TestResult, objTest.Max)
            CheckValue = objTest.qf(k/m)
            self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
        del objTest

class Test_Gaussian(Test_Z_Distribution):
    """
    Unittests for Gaussian class from the module
    statistics_lib.distribution_classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Gaussian
        cls.Parameters = ('Mean', 'Sigma')
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Mean = random.randint(-10, 10)
        if random.random() > 0.5:
            Mean += random.random()
        Sigma = random.randint(1, 3)
        if random.random() > 0.5:
            Sigma -= random.random()
        self.DefArguments = (Mean, Sigma)
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-400
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Mean = random.randint(-10, 10)
            if random.random() > 0.5:
                Mean += random.random()
            Sigma = random.randint(1, 3)
            if random.random() > 0.5:
                Sigma -= random.random()
            objTest = self.TestClass(Mean, Sigma)
            self.assertAlmostEqual(objTest.Mean, Mean,
                                                places= FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Sigma, Sigma,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Median, Mean,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, Sigma * Sigma,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertEqual(objTest.Skew, 0)
            self.assertEqual(objTest.Kurt, 0)
            self.assertEqual(objTest.Min, -math.inf)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Q1, Mean -0.6744899 * Sigma,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, Mean + 0.6744899 * Sigma,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_hasAttributes(self) -> None:
        """
        Checks that the class' instance has all required attributes.
        
        Test ID: TEST-T-401
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Mean = random.randint(-10, 10)
            if random.random() > 0.5:
                Mean += random.random()
            Sigma = random.randint(1, 3)
            if random.random() > 0.5:
                Sigma -= random.random()
            objTest = self.TestClass(Mean, Sigma)
            for Name in self.Properties:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Parameters:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Methods:
                self.assertTrue(hasattr(objTest, Name))
            del objTest
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-402
        Requirements: REQ-FUN-402
        """
        objTest = self.TestClass(*self.DefArguments)
        Mean = self.DefArguments[0]
        Sigma = self.DefArguments[1]
        self.assertEqual(objTest.Mean, Mean)
        self.assertEqual(objTest.Sigma, Sigma)
        for _ in range(100):
            Mean = random.randint(-10, 10)
            if random.random() > 0.5:
                Mean += random.random()
            Sigma = random.randint(1, 3)
            if random.random() > 0.5:
                Sigma -= random.random()
            objTest.Mean = Mean
            objTest.Sigma = Sigma
            self.assertAlmostEqual(objTest.Mean, Mean,
                                                places= FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Sigma, Sigma,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Median, Mean,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, Sigma * Sigma,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertEqual(objTest.Skew, 0)
            self.assertEqual(objTest.Kurt, 0)
            self.assertEqual(objTest.Min, -math.inf)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Q1, Mean -0.6744899 * Sigma,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, Mean + 0.6744899 * Sigma,
                                                places = FLOAT_CHECK_PRECISION)
        del objTest
    
    def test_init_TypeError(self) -> None:
        """
        Checks that improper data types of the argument(s) of the initialization
        method result in TypeError or its sub-class exception.
        
        Test ID: TEST-T-407
        Requirements: REQ-AWM-400
        """
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                self.TestClass(Value, 1)
            with self.assertRaises(TypeError):
                self.TestClass(1, Value)
            with self.assertRaises(TypeError):
                self.TestClass(Value, Value)
    
    def test_init_ValueError(self) -> None:
        """
        Checks that improper values of the argument(s) of the initialization
        method result in ValueError or its sub-class exception.
        
        Test ID: TEST-T-408
        Requirements: REQ-AWM-401
        """
        for _ in range(10):
            Mean = random.randint(-10, 10) + random.random()
            Value = random.randint(-10, -1)
            with self.assertRaises(ValueError):
                self.TestClass(Mean, Value)
            Value += random.random()
            with self.assertRaises(ValueError):
                self.TestClass(Mean, Value)
            with self.assertRaises(ValueError):
                self.TestClass(Mean, 0)
    
    def test_setters_TypeError(self) -> None:
        """
        Checks that improper data types of the argument(s) of the setter
        properties result in TypeError or its sub-class exception.
        
        Test ID: TEST-T-407
        Requirements: REQ-AWM-400
        """
        objTest = self.TestClass(*self.DefArguments)
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                objTest.Mean = Value
            with self.assertRaises(TypeError):
                objTest.Sigma = Value
        del objTest
    
    def test_setters_ValueError(self) -> None:
        """
        Checks that improper data types of the argument(s) of the setter
        properties result in TypeError or its sub-class exception.
        
        Test ID: TEST-T-408
        Requirements: REQ-AWM-401
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Value = random.randint(-10, -1)
            with self.assertRaises(ValueError):
                objTest.Sigma = Value
            Value += random.random()
            with self.assertRaises(ValueError):
                objTest.Sigma = Value
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-404
        Requirements ID: REQ-FUN-404
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Mean = objTest.Mean
            Sigma = objTest.Sigma
            for _ in range(100):
                Value = random.randint(-10, 10)
                if random.random() > 0.5:
                    Value += random.random()
                z = (Value - Mean) / Sigma
                TestResult = objTest.pdf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreaterEqual(TestResult, 0)
                CheckValue = math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
                CheckValue /= Sigma
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Mean = random.randint(-10, 10)
            if random.random() > 0.5:
                Mean += random.random()
            Sigma = random.randint(1, 3)
            if random.random() > 0.5:
                Sigma -= random.random()
            objTest.Mean = Mean
            objTest.Sigma = Sigma
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method.
        
        Test ID: TEST-T-405
        Requirements ID: REQ-FUN-405
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Mean = objTest.Mean
            Sigma = objTest.Sigma
            for _ in range(100):
                Value = random.randint(-10, 10)
                if random.random() > 0.5:
                    Value += random.random()
                z = (Value - Mean) / Sigma
                TestResult = objTest.cdf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreaterEqual(TestResult, 0)
                CheckValue = 0.5 * (1 + math.erf(z / math.sqrt(2)))
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Mean = random.randint(-10, 10)
            if random.random() > 0.5:
                Mean += random.random()
            Sigma = random.randint(1, 3)
            if random.random() > 0.5:
                Sigma -= random.random()
            objTest.Mean = Mean
            objTest.Sigma = Sigma
        del objTest
    
    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method.
        
        Test ID: TEST-T-406
        Requirements ID: REQ-FUN-406
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Mean = objTest.Mean
            Sigma = objTest.Sigma
            for _ in range(100):
                Value = random.random()
                if Value < 1.0E-11:
                    Value = 1.0E-11
                TestResult = objTest.qf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreater(TestResult, objTest.Min)
                self.assertLess(TestResult, objTest.Max)
                CheckValue = math.sqrt(2) * sf.inv_erf(2 * Value - 1) * Sigma
                CheckValue += Mean
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Mean = random.randint(-10, 10)
            if random.random() > 0.5:
                Mean += random.random()
            Sigma = random.randint(1, 3)
            if random.random() > 0.5:
                Sigma -= random.random()
            objTest.Mean = Mean
            objTest.Sigma = Sigma
        del objTest
    
    def test_getQuantile(self) -> None:
        """
        Checks the implementation of the getQuantile() method.
        
        Test ID: TEST-T-406
        Requirements ID: REQ-FUN-406
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            for _ in range(100):
                k = random.randint(1, 20)
                m = random.randint(1, 20) + k
                TestResult = objTest.getQuantile(k, m)
                self.assertIsInstance(TestResult, float)
                self.assertGreater(TestResult, objTest.Min)
                self.assertLess(TestResult, objTest.Max)
                CheckValue = objTest.qf(k/m)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Mean = random.randint(-10, 10)
            if random.random() > 0.5:
                Mean += random.random()
            Sigma = random.randint(1, 3)
            if random.random() > 0.5:
                Sigma -= random.random()
            objTest.Mean = Mean
            objTest.Sigma = Sigma
        del objTest

class Test_Exponential(Test_Z_Distribution):
    """
    Unittests for Exponential class from the module
    statistics_lib.distribution_classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Exponential
        cls.Parameters = ('Rate', )
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Rate = random.randint(1, 10)
        if random.random() > 0.5:
            Rate -= random.random()
        self.DefArguments = (Rate, )
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-400
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest = self.TestClass(Rate)
            self.assertAlmostEqual(objTest.Mean, 1 / Rate,
                                                places= FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Sigma, 1 / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Median, math.log(2) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, 1 / (Rate * Rate),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertEqual(objTest.Skew, 2)
            self.assertEqual(objTest.Kurt, 6)
            self.assertEqual(objTest.Min, 0)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Q1, -math.log(0.75) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, -math.log(0.25) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_hasAttributes(self) -> None:
        """
        Checks that the class' instance has all required attributes.
        
        Test ID: TEST-T-401
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest = self.TestClass(Rate)
            for Name in self.Properties:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Parameters:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Methods:
                self.assertTrue(hasattr(objTest, Name))
            del objTest
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-402
        Requirements: REQ-FUN-402
        """
        objTest = self.TestClass(*self.DefArguments)
        Rate = self.DefArguments[0]
        self.assertEqual(objTest.Rate, Rate)
        for _ in range(100):
            Rate = random.randint(1, 5)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Rate = Rate
            self.assertEqual(objTest.Rate, Rate)
            self.assertAlmostEqual(objTest.Mean, 1 / Rate,
                                                places= FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Sigma, 1 / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Median, -math.log(0.5) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, 1 / (Rate * Rate),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertEqual(objTest.Skew, 2)
            self.assertEqual(objTest.Kurt, 6)
            self.assertEqual(objTest.Min, 0)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Q1, -math.log(0.75) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, -math.log(0.25) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
        del objTest
    
    def test_init_TypeError(self) -> None:
        """
        Checks that improper data types of the argument(s) of the initialization
        method result in TypeError or its sub-class exception.
        
        Test ID: TEST-T-407
        Requirements: REQ-AWM-400
        """
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                self.TestClass(Value)
    
    def test_init_ValueError(self) -> None:
        """
        Checks that improper values of the argument(s) of the initialization
        method result in ValueError or its sub-class exception.
        
        Test ID: TEST-T-408
        Requirements: REQ-AWM-401
        """
        for _ in range(10):
            Value = random.randint(-10, -1)
            with self.assertRaises(ValueError):
                self.TestClass(Value)
            Value += random.random()
            with self.assertRaises(ValueError):
                self.TestClass(Value)
        with self.assertRaises(ValueError):
            self.TestClass(0)
    
    def test_setters_TypeError(self) -> None:
        """
        Checks that improper data types of the argument(s) of the setter
        properties result in TypeError or its sub-class exception.
        
        Test ID: TEST-T-407
        Requirements: REQ-AWM-400
        """
        objTest = self.TestClass(*self.DefArguments)
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                objTest.Rate = Value
        del objTest
    
    def test_setters_ValueError(self) -> None:
        """
        Checks that improper data types of the argument(s) of the setter
        properties result in TypeError or its sub-class exception.
        
        Test ID: TEST-T-408
        Requirements: REQ-AWM-401
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Value = random.randint(-10, -1)
            with self.assertRaises(ValueError):
                objTest.Rate = Value
            Value += random.random()
            with self.assertRaises(ValueError):
                objTest.Rate = Value
        with self.assertRaises(ValueError):
            objTest.Rate = 0
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-404
        Requirements ID: REQ-FUN-404
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Rate = objTest.Rate
            for _ in range(100):
                Value = random.randint(0, 10)
                if random.random() > 0.5:
                    Value += random.random()
                TestResult = objTest.pdf(Value)
                self.assertIsInstance(TestResult, (int, float))
                self.assertGreaterEqual(TestResult, 0)
                CheckValue = math.exp(- Rate * Value) * Rate
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                if Value > 0:
                    self.assertEqual(objTest.pdf(-Value), 0)
            Rate = random.randint(1, 5)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Rate = Rate
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method.
        
        Test ID: TEST-T-405
        Requirements ID: REQ-FUN-405
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Rate = objTest.Rate
            for _ in range(100):
                Value = random.randint(0, 10)
                if random.random() > 0.5:
                    Value += random.random()
                TestResult = objTest.cdf(Value)
                self.assertIsInstance(TestResult, (float, int))
                self.assertGreaterEqual(TestResult, 0)
                CheckValue = 1 - math.exp(-Rate * Value)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertEqual(objTest.cdf(-Value), 0)
            Rate = random.randint(1, 5)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Rate = Rate
        del objTest
    
    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method.
        
        Test ID: TEST-T-406
        Requirements ID: REQ-FUN-406
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Rate = objTest.Rate
            for _ in range(100):
                Value = random.random()
                if Value < 1.0E-11:
                    Value = 1.0E-11
                TestResult = objTest.qf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreater(TestResult, objTest.Min)
                self.assertLess(TestResult, objTest.Max)
                CheckValue = - math.log(1 - Value) / Rate
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Rate = random.randint(1, 5)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Rate = Rate
        del objTest
    
    def test_getQuantile(self) -> None:
        """
        Checks the implementation of the getQuantile() method.
        
        Test ID: TEST-T-406
        Requirements ID: REQ-FUN-406
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            for _ in range(100):
                k = random.randint(1, 20)
                m = random.randint(1, 20) + k
                TestResult = objTest.getQuantile(k, m)
                self.assertIsInstance(TestResult, float)
                self.assertGreater(TestResult, objTest.Min)
                self.assertLess(TestResult, objTest.Max)
                CheckValue = objTest.qf(k/m)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Rate = random.randint(1, 5)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Rate = Rate
        del objTest

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(
                                                Test_ContinuousDistributionABC)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(
                                                Test_DiscreteDistributionABC)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(
                                                Test_Z_Distribution)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_Gaussian)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_Exponential)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                        ])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting statistics_lib.distribution_classes module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)