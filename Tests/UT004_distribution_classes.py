#usr/bin/python3
"""
Module statistics_lib.Tests.UT004_distribution_classes

Set of unit tests on the module stastics_lib.distribution_classes. See the test
plan / report TE004_distribution_classes.md
"""


__version__= '1.0.0.0'
__date__ = '15-04-2022'
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

#+ critical values tables

#++ Student's t-distributions
#++ https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm

TD_1_A = (0.9, 0.95, 0.975, 0.99, 0.995, 0.999)

TD_NU = (1, 2, 3, 4, 5, 10, 50, 100)

TD_CR = ((3.078, 6.314, 12.706, 31.821, 63.657, 318.313),
            (1.886, 2.920, 4.303, 6.965, 9.925, 22.327),
            (1.638, 2.353, 3.182, 4.541, 5.841, 10.215),
            (1.533, 2.132, 2.776, 3.747, 4.604, 7.173),
            (1.476, 2.015, 2.571, 3.365, 4.032, 5.893),
            (1.372, 1.812, 2.228, 2.764, 3.169, 4.143),
            (1.299, 1.676, 2.009, 2.403, 2.678, 3.261),
            (1.290, 1.660, 1.984, 2.364, 2.626, 3.174))

#++ Chi-squared distribution - with minor corrections for 1 degree of freedom
#++ and extremely propability level of < 0.05
#++ https://www.itl.nist.gov/div898/handbook/eda/section3/eda3674.htm

CHS_1_A = (0.9, 0.95, 0.975, 0.99, 0.999, 0.10, 0.05, 0.01, 0.001)

CHS_NU = (1, 2, 3, 4, 5, 10, 50, 100)

CHS_CR =(
    (2.706, 3.841, 5.024, 6.635, 10.828, 0.0158, 0.00393, 0.000157, 0.000001),
    (4.605, 5.991, 7.378, 9.210, 13.816, 0.211, 0.103, 0.020, 0.002),
    (6.251, 7.815, 9.348, 11.345, 16.266, 0.584, 0.352, 0.115, 0.024),
    (7.779, 9.488, 11.143, 13.277, 18.467, 1.064, 0.711, 0.297, 0.091),
    (9.236, 11.070, 12.833, 15.086, 20.515, 1.610, 1.145, 0.554, 0.210),
    (15.987, 18.307, 20.483, 23.209, 29.588, 4.865, 3.940, 2.558, 1.479),
    (63.167, 67.505, 71.420, 76.154, 86.661, 37.689, 34.764, 29.707, 24.674),
    (118.498, 124.342, 129.561, 135.807, 149.449, 82.358, 77.929, 70.065, 61.918
    ))

#++ F-distribution
#++ https://www.itl.nist.gov/div898/handbook/eda/section3/eda3673.htm

FD_1_A = (0.95, 0.90, 0.99)

FD_D = (1, 5, 10, 20)

FD_CR =(((161.448, 230.162, 241.882, 248.013),
        (6.608, 5.050, 4.735, 4.558),
        (4.965, 3.326, 2.978, 2.774),
        (4.351, 2.711, 2.348, 2.124)),
        ((39.863, 57.240, 60.195, 61.740),
        (4.060, 3.453, 3.297, 3.207),
        (3.285, 2.522, 2.323, 2.201),
        (2.975, 2.158, 1.937, 1.794)),
        ((4052.19, 5763.65, 6055.85, 6208.74),
        (16.258, 10.967, 10.051, 9.553),
        (10.044, 5.636, 4.849, 4.405),
        (8.096, 4.103, 3.368, 2.938)))

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
            if Value < 1.0E-5:
                Value = 1.0E-5
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
                if Value < 1.0E-5:
                    Value = 1.0E-5
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
                if Value < 1.0E-5:
                    Value = 1.0E-5
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

class Test_Student(Test_Z_Distribution):
    """
    Unittests for Student class from the module
    statistics_lib.distribution_classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Student
        cls.Parameters = ('Degree', )
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Degree = random.randint(1, 100)
        if random.random() > 0.5:
            Degree -= random.random()
        self.DefArguments = (Degree, )
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-400
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest = self.TestClass(Degree)
            if Degree > 1:
                self.assertEqual(objTest.Mean, 0)
            else:
                self.assertIsNone(objTest.Mean)
            if Degree > 2:
                Temp = Degree / (Degree - 2)
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Temp),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Temp,
                                                places = FLOAT_CHECK_PRECISION)
            elif Degree > 1:
                self.assertIs(objTest.Sigma, math.inf)
                self.assertIs(objTest.Var, math.inf)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if Degree > 3:
                self.assertEqual(objTest.Skew, 0)
            else:
                self.assertIsNone(objTest.Skew)
            if Degree > 4:
                self.assertAlmostEqual(objTest.Kurt, 6 / (Degree - 4),
                                                places = FLOAT_CHECK_PRECISION)
            elif Degree > 2:
                self.assertIs(objTest.Kurt, math.inf)
            else:
                self.assertIsNone(objTest.Kurt)
            self.assertEqual(objTest.Median, 0)
            self.assertEqual(objTest.Min, - math.inf)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-402
        Requirements: REQ-FUN-402
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree = self.DefArguments[0]
        self.assertEqual(objTest.Degree, Degree)
        for _ in range(100):
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
            self.assertEqual(objTest.Degree, Degree)
            if Degree > 1:
                self.assertEqual(objTest.Mean, 0)
            else:
                self.assertIsNone(objTest.Mean)
            if Degree > 2:
                Temp = Degree / (Degree - 2)
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Temp),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Temp,
                                                places = FLOAT_CHECK_PRECISION)
            elif Degree > 1:
                self.assertIs(objTest.Sigma, math.inf)
                self.assertIs(objTest.Var, math.inf)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if Degree > 3:
                self.assertEqual(objTest.Skew, 0)
            else:
                self.assertIsNone(objTest.Skew)
            if Degree > 4:
                self.assertAlmostEqual(objTest.Kurt, 6 / (Degree - 4),
                                                places = FLOAT_CHECK_PRECISION)
            elif Degree > 2:
                self.assertIs(objTest.Kurt, math.inf)
            else:
                self.assertIsNone(objTest.Kurt)
            self.assertEqual(objTest.Median, 0)
            self.assertEqual(objTest.Min, - math.inf)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
                                                places = FLOAT_CHECK_PRECISION)
        del objTest
    
    def test_hasAttributes(self) -> None:
        """
        Checks that the class' instance has all required attributes.
        
        Test ID: TEST-T-401
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest = self.TestClass(Degree)
            for Name in self.Properties:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Parameters:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Methods:
                self.assertTrue(hasattr(objTest, Name))
            del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method. The test values are
        calculated using beta function instead of gamma functions definition,
        see
        
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda3664.htm
        
        Test ID: TEST-T-404
        Requirements ID: REQ-FUN-404
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Degree = objTest.Degree
            LogFactor = -0.5 * math.log(Degree) - sf.log_beta(0.5, 0.5 * Degree)
            for _ in range(100):
                Value = random.randint(0, 10)
                if random.random() > 0.5:
                    Value += random.random()
                Temp= -0.5 * (Degree + 1) * math.log(1 + Value * Value / Degree)
                CheckValue = math.exp(Temp + LogFactor)
                TestResult = objTest.pdf(Value)
                self.assertIsInstance(TestResult, (int, float))
                self.assertGreaterEqual(TestResult, 0)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = objTest.pdf(-Value)
                self.assertIsInstance(TestResult, (int, float))
                self.assertGreaterEqual(TestResult, 0)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method. The tabulated values
        are taken from NIST with 3 digits after comma.
        
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm
        
        Test ID: TEST-T-405
        Requirements ID: REQ-FUN-405
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Degree = objTest.Degree
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                Temp = Degree / (Value * Value + Degree)
                CheckValue=1 - 0.5*sf.beta_incomplete_reg(Temp, 0.5*Degree, 0.5)
                TestResult = objTest.cdf(Value)
                self.assertIsInstance(TestResult, (float, int))
                self.assertGreaterEqual(TestResult, 0)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = objTest.cdf(-Value)
                self.assertIsInstance(TestResult, (float, int))
                self.assertGreaterEqual(TestResult, 0)
                self.assertAlmostEqual(TestResult, 1 - CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = objTest.cdf(0)
            self.assertAlmostEqual(TestResult, 0.5)
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
        #check tabulated values
        for DegreeIndex, Degree in enumerate(TD_NU):
            objTest.Degree = Degree
            for ProbIndex, Prob in enumerate(TD_1_A):
                Temp = TD_CR[DegreeIndex][ProbIndex]
                TestResult = objTest.cdf(Temp)
                self.assertAlmostEqual(TestResult, Prob, places = 3)
                TestResult = objTest.cdf(-Temp)
                self.assertAlmostEqual(TestResult, 1 - Prob, places = 3)
        del objTest
    
    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method. The tabulated values
        are taken from NIST with 3 digits after comma.
        
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm
        
        Test ID: TEST-T-406
        Requirements ID: REQ-FUN-406
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Degree = objTest.Degree
            for _ in range(100):
                Value = random.random()
                if Value < 1.0E-5:
                    Value = 1.0E-5
                TestResult = objTest.cdf(objTest.qf(Value))
                self.assertIsInstance(TestResult, float)
                self.assertGreater(TestResult, objTest.Min)
                self.assertLess(TestResult, objTest.Max)
                self.assertAlmostEqual(TestResult, Value,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = objTest.qf(0.5)
            self.assertAlmostEqual(TestResult, 0, places= FLOAT_CHECK_PRECISION)
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
        #check tabulated values
        for DegreeIndex, Degree in enumerate(TD_NU):
            objTest.Degree = Degree
            for ProbIndex, Prob in enumerate(TD_1_A):
                CheckValue = TD_CR[DegreeIndex][ProbIndex]
                Delta = CheckValue / 1000 #max relative error = 0.001 = 0.1 %
                TestResult = objTest.qf(Prob)
                self.assertAlmostEqual(TestResult, CheckValue, delta = Delta)
                TestResult = objTest.qf(1 - Prob)
                self.assertAlmostEqual(TestResult, -CheckValue, delta = Delta)
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
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
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
        Degree = self.DefArguments[0]
        objTest = self.TestClass(Degree)
        for Name in self.Properties:
            if (Name in ['Var', 'Sigma', 'Mean']) and (Degree <= 1):
                self.assertIsNone(getattr(objTest, Name))
            elif (Name == 'Skew') and (Degree <= 3):
                self.assertIsNone(getattr(objTest, Name))
            elif (Name == 'Kurt') and (Degree <= 2):
                self.assertIsNone(getattr(objTest, Name))
            else:
                self.assertIsInstance(getattr(objTest, Name), (int, float))
            with self.assertRaises(AttributeError):
                delattr(objTest, Name)
            if not (Name in self.Parameters):
                with self.assertRaises(AttributeError):
                    setattr(objTest, Name, 1)
        del objTest
    
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
                objTest.Degree = Value
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
                objTest.Degree = Value
            Value += random.random()
            with self.assertRaises(ValueError):
                objTest.Degree = Value
        with self.assertRaises(ValueError):
            objTest.Degree = 0
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
            Degree1 = random.randint(-10, -1)
            with self.assertRaises(ValueError):
                self.TestClass(Degree1)
            Degree1 += random.random()
            with self.assertRaises(ValueError):
                self.TestClass(Degree1)
        with self.assertRaises(ValueError):
            self.TestClass(0)

class Test_ChiSquared(Test_Student):
    """
    Unittests for ChiSquared class from the module
    statistics_lib.distribution_classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.ChiSquared
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-400
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest = self.TestClass(Degree)
            self.assertEqual(objTest.Mean, Degree)
            self.assertAlmostEqual(objTest.Sigma, math.sqrt(2 * Degree),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, 2 * Degree,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Skew,  math.sqrt(8 / Degree),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Kurt, 12 / Degree,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Median, objTest.qf(0.5),
                                                places = FLOAT_CHECK_PRECISION)
            if Degree >= 2:
                self.assertEqual(objTest.Min, 0)
            else:
                self.assertLess(objTest.Min, 3 * sys.float_info.min)
                self.assertGreater(objTest.Min, sys.float_info.min)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-402
        Requirements: REQ-FUN-402
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree = self.DefArguments[0]
        self.assertEqual(objTest.Degree, Degree)
        for _ in range(100):
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
            self.assertEqual(objTest.Degree, Degree)
            self.assertEqual(objTest.Mean, Degree)
            self.assertAlmostEqual(objTest.Sigma, math.sqrt(2 * Degree),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, 2 * Degree,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Skew,  math.sqrt(8 / Degree),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Kurt, 12 / Degree,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Median, objTest.qf(0.5),
                                                places = FLOAT_CHECK_PRECISION)
            if Degree >= 2:
                self.assertEqual(objTest.Min, 0)
            else:
                self.assertLess(objTest.Min, 3 * sys.float_info.min)
                self.assertGreater(objTest.Min, sys.float_info.min)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
                                                places = FLOAT_CHECK_PRECISION)
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method. The test values are
        calculated using definition, see
        
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda3666.htm
        
        Test ID: TEST-T-404
        Requirements ID: REQ-FUN-404
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Degree = objTest.Degree
            LogFactor = - (0.5 * Degree * math.log(2) + math.lgamma(0.5*Degree))
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                Temp = (0.5 * Degree - 1) * math.log(Value) - 0.5 * Value
                CheckValue = math.exp(Temp + LogFactor)
                TestResult = objTest.pdf(Value)
                self.assertIsInstance(TestResult, (int, float))
                self.assertGreaterEqual(TestResult, 0)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = objTest.pdf(-Value)
                self.assertIsInstance(TestResult, (int, float))
                self.assertEqual(TestResult, 0)
            #special case
            TestResult = objTest.pdf(0)
            if Degree != 2:
                self.assertAlmostEqual(TestResult, 0)
            else:
                self.assertAlmostEqual(TestResult, 0.5)
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method. The tabulated values
        are taken from NIST with 3 digits after comma.
        
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda3674.htm
        
        Test ID: TEST-T-405
        Requirements ID: REQ-FUN-405
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Degree = objTest.Degree
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                CheckValue = sf.lower_gamma_reg(0.5 * Degree, 0.5 * Value)
                TestResult = objTest.cdf(Value)
                self.assertIsInstance(TestResult, (float, int))
                self.assertGreaterEqual(TestResult, 0)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = objTest.cdf(-Value)
                self.assertIsInstance(TestResult, (float, int))
                self.assertEqual(TestResult, 0)
            TestResult = objTest.cdf(0)
            self.assertIsInstance(TestResult, (float, int))
            self.assertEqual(TestResult, 0)
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
        #check tabulated values
        for DegreeIndex, Degree in enumerate(CHS_NU):
            objTest.Degree = Degree
            for ProbIndex, Prob in enumerate(CHS_1_A):
                Temp = CHS_CR[DegreeIndex][ProbIndex]
                TestResult = objTest.cdf(Temp)
                self.assertAlmostEqual(TestResult, Prob, places = 3)
        del objTest
    
    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method. The tabulated values
        are taken from NIST with 3 digits after comma.
        
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda3674.htm
        
        Test ID: TEST-T-406
        Requirements ID: REQ-FUN-406
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Degree = objTest.Degree
            for _ in range(100):
                Value = random.random()
                if Value < 1.0E-5:
                    Value = 1.0E-5
                TestResult = objTest.cdf(objTest.qf(Value))
                self.assertIsInstance(TestResult, float)
                self.assertGreater(TestResult, objTest.Min)
                self.assertLess(TestResult, objTest.Max)
                self.assertAlmostEqual(TestResult, Value,
                                                places = FLOAT_CHECK_PRECISION)
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
        #check tabulated values
        for DegreeIndex, Degree in enumerate(CHS_NU):
            objTest.Degree = Degree
            for ProbIndex, Prob in enumerate(CHS_1_A):
                CheckValue = CHS_CR[DegreeIndex][ProbIndex]
                TestResult = objTest.qf(Prob)
                if CheckValue > 1:
                    Delta = CheckValue / 1000 #max relative error = 0.001= 0.1 %
                self.assertAlmostEqual(TestResult, CheckValue, delta = Delta)
            else:
                self.assertAlmostEqual(TestResult, CheckValue, places = 3)
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

class Test_F_Distribution(Test_Z_Distribution):
    """
    Unittests for F_Distribution class from the module
    statistics_lib.distribution_classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.F_Distribution
        cls.Parameters = ('Degree1', 'Degree2')
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Degree1 = random.randint(1, 100)
        if random.random() > 0.5:
            Degree1 -= random.random()
        Degree2 = random.randint(1, 100)
        if random.random() > 0.5:
            Degree2 -= random.random()
        self.DefArguments = (Degree1, Degree2)
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-400
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Degree1 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree1 -= random.random()
            Degree2 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree2 -= random.random()
            objTest = self.TestClass(Degree1, Degree2)
            d1 = Degree1
            d2 = Degree2
            if Degree2 > 2:
                Check = d2 / (d2 - 2)
                self.assertAlmostEqual(objTest.Mean, Check)
            else:
                self.assertIsNone(objTest.Mean)
            if Degree2 > 4:
                Var = 2 * d2 * d2 * (d1 + d2 - 2) / (d1 * (d2 - 2) * (d2 - 2))
                Var /= (d2 - 4)
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if Degree2 > 6:
                Temp = math.sqrt(8 * (d2 -  4) / (d1 * (d1 + d2 -2)))
                Temp *= (2 * d1 + d2 - 2) / (d2 - 6)
                self.assertAlmostEqual(objTest.Skew, Temp)
            else:
                self.assertIsNone(objTest.Skew)
            if Degree2 > 8:
                Temp = d1 * (5 * d2 - 22) * (d1 + d2 - 2)
                Temp += (d2 - 4) * (d2 - 2) * (d2 - 2)
                Temp *= 12 / d1
                Temp /= (d2 - 6) * (d2 - 8) * (d1 + d2 - 2)
                self.assertAlmostEqual(objTest.Kurt, Temp,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Kurt)
            if Degree1 >= 2:
                self.assertEqual(objTest.Min, 0)
            else:
                self.assertLess(objTest.Min, 3 * sys.float_info.min)
                self.assertGreater(objTest.Min, sys.float_info.min)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, objTest.qf(0.5),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-402
        Requirements: REQ-FUN-402
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree1 = self.DefArguments[0]
        Degree2 = self.DefArguments[1]
        self.assertEqual(objTest.Degree1, Degree1)
        self.assertEqual(objTest.Degree2, Degree2)
        for _ in range(100):
            d1 = objTest.Degree1
            d2 = objTest.Degree2
            if d2 > 2:
                Check = d2 / (d2 - 2)
                self.assertAlmostEqual(objTest.Mean, Check)
            else:
                self.assertIsNone(objTest.Mean)
            if d2 > 4:
                Var = 2 * d2 * d2 * (d1 + d2 - 2) / (d1 * (d2 - 2) * (d2 - 2))
                Var /= (d2 - 4)
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if d2 > 6:
                Temp = math.sqrt(8 * (d2 -  4) / (d1 * (d1 + d2 -2)))
                Temp *= (2 * d1 + d2 - 2) / (d2 - 6)
                self.assertAlmostEqual(objTest.Skew, Temp)
            else:
                self.assertIsNone(objTest.Skew)
            if d2 > 8:
                Temp = d1 * (5 * d2 - 22) * (d1 + d2 - 2)
                Temp += (d2 - 4) * (d2 - 2) * (d2 - 2)
                Temp *= 12 / d1
                Temp /= (d2 - 6) * (d2 - 8) * (d1 + d2 - 2)
                self.assertAlmostEqual(objTest.Kurt, Temp,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Kurt)
            if d1 >= 2:
                self.assertEqual(objTest.Min, 0)
            else:
                self.assertLess(objTest.Min, 3 * sys.float_info.min)
                self.assertGreater(objTest.Min, sys.float_info.min)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, objTest.qf(0.5),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
                                                places = FLOAT_CHECK_PRECISION)
            Degree1 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree1 -= random.random()
            Degree2 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree2 -= random.random()
            objTest.Degree1 = Degree1
            objTest.Degree2 = Degree2
        del objTest
    
    def test_hasAttributes(self) -> None:
        """
        Checks that the class' instance has all required attributes.
        
        Test ID: TEST-T-401
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Degree1 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree1 -= random.random()
            Degree2 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree2 -= random.random()
            objTest = self.TestClass(Degree1, Degree2)
            for Name in self.Properties:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Parameters:
                self.assertTrue(hasattr(objTest, Name))
            for Name in self.Methods:
                self.assertTrue(hasattr(objTest, Name))
            del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method. The test values are
        calculated using beta function instead of gamma functions definition,
        see
        
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda3665.htm
        
        Test ID: TEST-T-404
        Requirements ID: REQ-FUN-404
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree1 = self.DefArguments[0]
        Degree2 = self.DefArguments[1]
        for _ in range(10):
            Temp = 0.5*(Degree1*math.log(Degree1) + Degree2*math.log(Degree2))
            LogFactor = Temp - sf.log_beta(0.5 * Degree1, 0.5 * Degree2)
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                Temp = LogFactor + (0.5 * Degree1 -1) * math.log(Value)
                Temp -= 0.5*(Degree1 + Degree2)*math.log(Degree1*Value+Degree2)
                CheckValue = math.exp(Temp)
                TestResult = objTest.pdf(Value)
                self.assertIsInstance(TestResult, (int, float))
                self.assertGreaterEqual(TestResult, 0)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = objTest.pdf(-Value)
                self.assertIsInstance(TestResult, (int, float))
                self.assertEqual(TestResult, 0)
            TestResult = objTest.pdf(0)
            if Degree1 != 2:
                self.assertEqual(TestResult, 0)
            else:
                self.assertEqual(TestResult, 1)
            Degree1 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree1 -= random.random()
            objTest.Degree1 = Degree1
            Degree2 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree2 -= random.random()
            objTest.Degree2 = Degree2
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method. The tabulated values
        are taken from NIST with 3 digits after comma.
        
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda3673.htm
        
        Test ID: TEST-T-405
        Requirements ID: REQ-FUN-405
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            d1 = objTest.Degree1
            d2 = objTest.Degree2
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                z = d1 * Value / (d1 * Value + d2)
                CheckValue = sf.beta_incomplete_reg(z, 0.5 * d1, 0.5 * d2)
                TestResult = objTest.cdf(Value)
                self.assertIsInstance(TestResult, (float, int))
                self.assertGreaterEqual(TestResult, 0)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                TestResult = objTest.cdf(-Value)
                self.assertIsInstance(TestResult, (float, int))
                self.assertEqual(TestResult, 0)
            TestResult = objTest.cdf(0)
            self.assertIsInstance(TestResult, (float, int))
            self.assertEqual(TestResult, 0)
            Degree1 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree1 -= random.random()
            objTest.Degree1 = Degree1
            Degree2 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree2 -= random.random()
            objTest.Degree2 = Degree2
        #check tabulated values
        for DegreeIndex1, Degree1 in enumerate(FD_D):
            for DegreeIndex2, Degree2 in enumerate(FD_D):
                objTest.Degree1 = Degree1
                objTest.Degree2 = Degree2
                for ProbIndex, Prob in enumerate(FD_1_A):
                    Temp = FD_CR[ProbIndex][DegreeIndex2][DegreeIndex1]
                    TestResult = objTest.cdf(Temp)
                    self.assertAlmostEqual(TestResult, Prob, places = 3)
        del objTest
    
    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method. The tabulated values
        are taken from NIST with 3 digits after comma.
        
        https://www.itl.nist.gov/div898/handbook/eda/section3/eda3673.htm
        
        Test ID: TEST-T-406
        Requirements ID: REQ-FUN-406
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            for _ in range(100):
                Value = random.random()
                if Value < 1.0E-5:
                    Value = 1.0E-5
                TestResult = objTest.cdf(objTest.qf(Value))
                self.assertIsInstance(TestResult, float)
                self.assertGreater(TestResult, objTest.Min)
                self.assertLess(TestResult, objTest.Max)
                self.assertAlmostEqual(TestResult, Value,
                                                places = FLOAT_CHECK_PRECISION)
            Degree1 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree1 -= random.random()
            objTest.Degree1 = Degree1
            Degree2 = random.randint(1, 100)
            if random.random() > 0.5:
                Degree2 -= random.random()
            objTest.Degree2 = Degree2
        #check tabulated values
        for DegreeIndex1, Degree1 in enumerate(FD_D):
            for DegreeIndex2, Degree2 in enumerate(FD_D):
                objTest.Degree1 = Degree1
                objTest.Degree2 = Degree2
                for ProbIndex, Prob in enumerate(FD_1_A):
                    CheckValue = FD_CR[ProbIndex][DegreeIndex2][DegreeIndex1]
                    Delta = CheckValue / 1000
                    #max relative error = 0.001 = 0.1 %
                    TestResult = objTest.qf(Prob)
                    self.assertAlmostEqual(TestResult, CheckValue, delta= Delta)
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
            Degree = random.randint(1, 100)
            if random.random() > 0.5:
                Degree -= random.random()
            objTest.Degree = Degree
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
        Degree1 = self.DefArguments[0]
        Degree2 = self.DefArguments[1]
        objTest = self.TestClass(Degree1, Degree2)
        for Name in self.Properties:
            if (Name == 'Mean') and (Degree2 <= 2):
                self.assertIsNone(getattr(objTest, Name))
            elif (Name in ['Var', 'Sigma']) and (Degree2 <= 4):
                self.assertIsNone(getattr(objTest, Name))
            elif (Name == 'Skew') and (Degree2 <= 6):
                self.assertIsNone(getattr(objTest, Name))
            elif (Name == 'Kurt') and (Degree2 <= 8):
                self.assertIsNone(getattr(objTest, Name))
            else:
                self.assertIsInstance(getattr(objTest, Name), (int, float))
            with self.assertRaises(AttributeError):
                delattr(objTest, Name)
            if not (Name in self.Parameters):
                with self.assertRaises(AttributeError):
                    setattr(objTest, Name, 1)
        del objTest
    
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
                objTest.Degree1 = Value
            with self.assertRaises(TypeError):
                objTest.Degree2 = Value
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
                objTest.Degree1 = Value
            with self.assertRaises(ValueError):
                objTest.Degree2 = Value
            Value += random.random()
            with self.assertRaises(ValueError):
                objTest.Degree1 = Value
            with self.assertRaises(ValueError):
                objTest.Degree2 = Value
        with self.assertRaises(ValueError):
            objTest.Degree1 = 0
        with self.assertRaises(ValueError):
            objTest.Degree2 = 0
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
            Degree1 = random.randint(-10, -1)
            Degree2 = random.randint(-10, -1)
            with self.assertRaises(ValueError):
                self.TestClass(Degree1, - Degree2) #first negative
            with self.assertRaises(ValueError):
                self.TestClass(- Degree1, Degree2) #second negative
            with self.assertRaises(ValueError):
                self.TestClass(Degree1, Degree2) #both negative
            Degree1 += random.random()
            Degree2 += random.random()
            with self.assertRaises(ValueError):
                self.TestClass(Degree1, - Degree2) #first negative
            with self.assertRaises(ValueError):
                self.TestClass(- Degree1, Degree2) #second negative
            with self.assertRaises(ValueError):
                self.TestClass(Degree1, Degree2) #both negative
        with self.assertRaises(ValueError):
            self.TestClass(0, 1) #first zero
        with self.assertRaises(ValueError):
            self.TestClass(1, 0) #second zero
        with self.assertRaises(ValueError):
            self.TestClass(0, 0) #both zero

class Test_Gamma(Test_Z_Distribution):
    """
    Unittests for Gamma class from the module
    statistics_lib.distribution_classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Gamma
        cls.Parameters = ('Shape', 'Rate')
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Shape = random.randint(1, 10)
        if random.random() > 0.5:
            Shape -= random.random()
        Rate = random.randint(1, 10)
        if random.random() > 0.5:
            Rate -= random.random()
        self.DefArguments = (Shape, Rate)
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-400
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Shape = random.randint(1, 10)
            if random.random() > 0.5:
                Shape -= random.random()
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest = self.TestClass(Shape, Rate)
            self.assertAlmostEqual(objTest.Shape, Shape)
            self.assertAlmostEqual(objTest.Rate, Rate)
            self.assertAlmostEqual(objTest.Mean, Shape / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, Shape / (Rate * Rate),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Sigma, math.sqrt(Shape) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Skew, 2 / math.sqrt(Shape),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Kurt, 6 / Shape,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertIsInstance(objTest.Min, float)
            self.assertGreater(objTest.Min, sys.float_info.min)
            self.assertLess(objTest.Min, 3 * sys.float_info.min)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, objTest.qf(0.5),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_hasAttributes(self) -> None:
        """
        Checks that the class' instance has all required attributes.
        
        Test ID: TEST-T-401
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Shape = random.randint(1, 10)
            if random.random() > 0.5:
                Shape -= random.random()
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest = self.TestClass(Shape, Rate)
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
        Shape = self.DefArguments[0]
        Rate = self.DefArguments[1]
        self.assertAlmostEqual(objTest.Shape, Shape)
        self.assertAlmostEqual(objTest.Rate, Rate)
        for _ in range(100):
            Shape = random.randint(1, 10)
            if random.random() > 0.5:
                Shape -= random.random()
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest = self.TestClass(Shape, Rate)
            objTest.Shape = Shape
            objTest.Rate = Rate
            self.assertAlmostEqual(objTest.Shape, Shape)
            self.assertAlmostEqual(objTest.Rate, Rate)
            self.assertAlmostEqual(objTest.Mean, Shape / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, Shape / (Rate * Rate),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Sigma, math.sqrt(Shape) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Skew, 2 / math.sqrt(Shape),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Kurt, 6 / Shape,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertIsInstance(objTest.Min, float)
            self.assertGreater(objTest.Min, sys.float_info.min)
            self.assertLess(objTest.Min, 3 * sys.float_info.min)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, objTest.qf(0.5),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
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
            Value = random.randint(-10, -1)
            with self.assertRaises(ValueError):
                self.TestClass(1, Value)
            with self.assertRaises(ValueError):
                self.TestClass(Value, 1)
            with self.assertRaises(ValueError):
                self.TestClass(Value, Value)
            Value += random.random()
            with self.assertRaises(ValueError):
                self.TestClass(1, Value)
            with self.assertRaises(ValueError):
                self.TestClass(Value, 1)
            with self.assertRaises(ValueError):
                self.TestClass(Value, Value)
        with self.assertRaises(ValueError):
            self.TestClass(1, 0)
        with self.assertRaises(ValueError):
            self.TestClass(0, 1)
        with self.assertRaises(ValueError):
            self.TestClass(0, 0)
    
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
                objTest.Shape = Value
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
                objTest.Shape = Value
            with self.assertRaises(ValueError):
                objTest.Rate = Value
            Value += random.random()
            with self.assertRaises(ValueError):
                objTest.Shape = Value
            with self.assertRaises(ValueError):
                objTest.Rate = Value
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-404
        Requirements ID: REQ-FUN-404
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Shape = objTest.Shape
            Rate = objTest.Rate
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 1.0E-5:
                    Value = 1.0E-5
                TestResult = objTest.pdf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreaterEqual(TestResult, 0)
                Temp = Shape * math.log(Rate) + (Shape - 1) * math.log(Value)
                Temp -= (Rate * Value + math.lgamma(Shape))
                CheckValue = math.exp(Temp)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION,
                                                msg = '{} {} {}'.format(Shape, Rate, Value))
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= 0.5 * random.random()
            Rate = random.randint(1, 5)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Shape = Shape
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
            Shape = objTest.Shape
            Rate = objTest.Rate
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                TestResult = objTest.cdf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreaterEqual(TestResult, 0)
                CheckValue = sf.lower_gamma_reg(Shape, Rate * Value)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Shape = random.randint(1, 10)
            if random.random() > 0.5:
                Shape -= random.random()
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Shape = Shape
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
            Shape = objTest.Shape
            Rate = objTest.Rate
            for _ in range(100):
                Value = random.random()
                if Value < 1.0E-5:
                    Value = 1.0E-5
                TestResult = objTest.qf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreater(TestResult, objTest.Min)
                self.assertLess(TestResult, objTest.Max)
                CheckValue = objTest.cdf(TestResult)
                self.assertAlmostEqual(CheckValue, Value,
                                                places = FLOAT_CHECK_PRECISION)
            Shape = random.randint(1, 10)
            if random.random() > 0.5:
                Shape -= random.random()
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Shape = Shape
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
            Shape = random.randint(1, 10)
            if random.random() > 0.5:
                Shape -= random.random()
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Shape = Shape
            objTest.Rate = Rate
        del objTest

class Test_Erlang(Test_Gamma):
    """
    Unittests for Erlang class from the module
    statistics_lib.distribution_classes.
    
    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Erlang
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Shape = random.randint(1, 10)
        Rate = random.randint(1, 10)
        if random.random() > 0.5:
            Rate -= random.random()
        self.DefArguments = (Shape, Rate)
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-400
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Shape = random.randint(1, 10)
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest = self.TestClass(Shape, Rate)
            self.assertAlmostEqual(objTest.Shape, Shape)
            self.assertAlmostEqual(objTest.Rate, Rate)
            self.assertAlmostEqual(objTest.Mean, Shape / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, Shape / (Rate * Rate),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Sigma, math.sqrt(Shape) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Skew, 2 / math.sqrt(Shape),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Kurt, 6 / Shape,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertEqual(objTest.Min, 0)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, objTest.qf(0.5),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_hasAttributes(self) -> None:
        """
        Checks that the class' instance has all required attributes.
        
        Test ID: TEST-T-401
        Requirements: REQ-FUN-401
        """
        for _ in range(100):
            Shape = random.randint(1, 10)
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest = self.TestClass(Shape, Rate)
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
        Shape = self.DefArguments[0]
        Rate = self.DefArguments[1]
        self.assertAlmostEqual(objTest.Shape, Shape)
        self.assertAlmostEqual(objTest.Rate, Rate)
        for _ in range(100):
            Shape = random.randint(1, 10)
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest = self.TestClass(Shape, Rate)
            objTest.Shape = Shape
            objTest.Rate = Rate
            self.assertAlmostEqual(objTest.Shape, Shape)
            self.assertAlmostEqual(objTest.Rate, Rate)
            self.assertAlmostEqual(objTest.Mean, Shape / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, Shape / (Rate * Rate),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Sigma, math.sqrt(Shape) / Rate,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Skew, 2 / math.sqrt(Shape),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Kurt, 6 / Shape,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertEqual(objTest.Min, 0)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, objTest.qf(0.5),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, objTest.qf(0.25),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, objTest.qf(0.75),
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
        for _ in range(10):
            Value = random.randint(1, 10) - random.random()
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
            Value = random.randint(-10, -1)
            with self.assertRaises(ValueError):
                self.TestClass(1, Value)
            with self.assertRaises(ValueError):
                self.TestClass(Value, 1)
            with self.assertRaises(ValueError):
                self.TestClass(Value, Value)
            Value += random.random()
            with self.assertRaises(ValueError):
                self.TestClass(1, Value)
        with self.assertRaises(ValueError):
            self.TestClass(1, 0)
        with self.assertRaises(ValueError):
            self.TestClass(0, 1)
        with self.assertRaises(ValueError):
            self.TestClass(0, 0)
    
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
                objTest.Shape = Value
            with self.assertRaises(TypeError):
                objTest.Rate = Value
        for _ in range(10):
            Value = random.randint(1, 10) - random.random()
            with self.assertRaises(TypeError):
                objTest.Shape = Value
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
                objTest.Shape = Value
            with self.assertRaises(ValueError):
                objTest.Rate = Value
            Value += random.random()
            with self.assertRaises(ValueError):
                objTest.Rate = Value
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-404
        Requirements ID: REQ-FUN-404
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Shape = objTest.Shape
            Rate = objTest.Rate
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                TestResult = objTest.pdf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreaterEqual(TestResult, 0)
                Temp = Shape * math.log(Rate) + (Shape - 1) * math.log(Value)
                Temp -= (Rate * Value + math.lgamma(Shape))
                CheckValue = math.exp(Temp)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            #special case - x = 0
            TestResult = objTest.pdf(0)
            if Shape > 1:
                self.assertEqual(TestResult, 0)
            else:
                self.assertAlmostEqual(TestResult, Rate)
            Shape = random.randint(1, 10)
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Shape = Shape
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
            Shape = objTest.Shape
            Rate = objTest.Rate
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                TestResult = objTest.cdf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreaterEqual(TestResult, 0)
                CheckValue = sf.lower_gamma_reg(Shape, Rate * Value)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Shape = random.randint(1, 10)
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Shape = Shape
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
            Shape = objTest.Shape
            Rate = objTest.Rate
            for _ in range(100):
                Value = random.random()
                if Value < 1.0E-5:
                    Value = 1.0E-5
                TestResult = objTest.qf(Value)
                self.assertIsInstance(TestResult, float)
                self.assertGreater(TestResult, objTest.Min)
                self.assertLess(TestResult, objTest.Max)
                CheckValue = objTest.cdf(TestResult)
                self.assertAlmostEqual(CheckValue, Value,
                                                places = FLOAT_CHECK_PRECISION)
            Shape = random.randint(1, 10)
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Shape = Shape
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
            Shape = random.randint(1, 10)
            Rate = random.randint(1, 10)
            if random.random() > 0.5:
                Rate -= random.random()
            objTest.Shape = Shape
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
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_Student)
TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_ChiSquared)
TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(Test_F_Distribution)
TestSuite9 = unittest.TestLoader().loadTestsFromTestCase(Test_Gamma)
TestSuite10 = unittest.TestLoader().loadTestsFromTestCase(Test_Erlang)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                        TestSuite6, TestSuite7, TestSuite8, TestSuite9,
                        TestSuite10])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting statistics_lib.distribution_classes module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)