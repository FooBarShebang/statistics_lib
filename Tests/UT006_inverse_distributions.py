#usr/bin/python3
"""
Module statistics_lib.Tests.UT006_inverse_distributions

Set of unit tests on the module stastics_lib.inverse_distributions. See the test
plan / report TE006_inverse_distributions.md
"""


__version__= '1.0.0.0'
__date__ = '28-04-2022'
__status__ = 'Testing'

#imports

#+ standard library

from sre_constants import SUCCESS
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

import statistics_lib.inverse_distributions as test_module

import statistics_lib.special_functions as sf

#globals

FLOAT_CHECK_PRECISION = 5 #digits after comma, mostly due to precision of
#+ the reference tables + internal Python implementation of the special
#+ functions

#classes

#+ test cases

class Test_InverseGaussian(unittest.TestCase):
    """
    Unittests for InverseGaussian class from the module
    statistics_lib.inverse_distributions.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = test_module.InverseGaussian
        cls.Properties = ('Mean', 'Median', 'Q1', 'Q3', 'Min', 'Max', 'Var',
                            'Sigma', 'Skew', 'Kurt')
        cls.Parameters = ('Mean', 'Shape')
        cls.Methods = ('pdf', 'cdf', 'qf', 'getQuantile', 'getHistogram',
                                                                    'random')
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Mean = random.randint(1, 10)
        if random.random() > 0.5:
            Mean -= random.random()
        if Mean < 0.1:
            Mean = 0.1
        Shape = random.randint(1, 5)
        if random.random() > 0.5:
            Shape -= random.random()
        if Shape < 0.1:
            Shape = 0.1
        self.DefArguments = (Mean, Shape)
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-600
        Requirements: REQ-FUN-601
        """
        for _ in range(100):
            Mean = random.randint(1, 10)
            if random.random() > 0.5:
                Mean -= random.random()
            if Mean < 0.1:
                Mean = 0.1
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            objTest = self.TestClass(Mean, Shape)
            self.assertEqual(objTest.Mean, Mean)
            self.assertEqual(objTest.Shape, Shape)
            Var = math.pow(Mean, 3) / Shape
            self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Skew, 3 * math.sqrt(Mean / Shape),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Kurt, 15 * Mean / Shape,
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
        
        Test ID: TEST-T-607
        Requirements: REQ-AWM-600
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
        
        Test ID: TEST-T-608
        Requirements: REQ-AWM-601
        """
        for _ in range(10):
            NegInt = random.randint(-10, -1)
            NegFloat = NegInt + random.random()
            with self.assertRaises(ValueError):
                self.TestClass(NegInt, 1)
            with self.assertRaises(ValueError):
                self.TestClass(NegFloat, 1.0)
            with self.assertRaises(ValueError):
                self.TestClass(1, NegInt)
            with self.assertRaises(ValueError):
                self.TestClass(1.0, NegFloat)
            with self.assertRaises(ValueError):
                self.TestClass(NegFloat, NegInt)
            with self.assertRaises(ValueError):
                self.TestClass(NegInt, NegFloat)
            with self.assertRaises(ValueError):
                self.TestClass(0,  - NegInt)
            with self.assertRaises(ValueError):
                self.TestClass(0.0,  - NegFloat)
            with self.assertRaises(ValueError):
                self.TestClass(- NegInt, 0.0)
            with self.assertRaises(ValueError):
                self.TestClass(- NegFloat, 0)
            with self.assertRaises(ValueError):
                self.TestClass(0, 0.0)
            with self.assertRaises(ValueError):
                self.TestClass(0.0, 0)
    
    def test_hasAttributes(self) -> None:
        """
        Checks that the class' instance has all required attributes.
        
        Test ID: TEST-T-601
        Requirements: REQ-FUN-601
        """
        objTest = self.TestClass(*self.DefArguments)
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
        numbers (including infinity) or None values.
        
        Test ID: TEST-T-603
        Requirements: REQ-FUN-603
        """
        objTest = self.TestClass(*self.DefArguments)
        for Name in self.Properties:
            Value = getattr(objTest, Name)
            if not (Value is None):
                self.assertIsInstance(Value, (int, float))
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
        
        Test ID: TEST-T-607
        Requirements: REQ-AWM-600
        """
        objTest = self.TestClass(*self.DefArguments)
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                objTest.pdf(Value)
        del objTest
    
    def test_cdf_TypeError(self) -> None:
        """
        Checks that TypeError or its sub-class exception is raised if the
        function being tested recieves improper data type argument(s).
        
        Test ID: TEST-T-607
        Requirements: REQ-AWM-600
        """
        objTest = self.TestClass(*self.DefArguments)
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                objTest.cdf(Value)
        del objTest
    
    def test_qf_TypeError(self) -> None:
        """
        Checks that TypeError or its sub-class exception is raised if the
        function being tested recieves improper data type argument(s).
        
        Test ID: TEST-T-607
        Requirements: REQ-AWM-600
        """
        objTest = self.TestClass(*self.DefArguments)
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool, 1, 3, -2):
            with self.assertRaises(TypeError):
                objTest.qf(Value)
        del objTest
    
    def test_qf_ValueError(self) -> None:
        """
        Checks that ValueError or its sub-class exception is raised if the
        function being tested recieves improper value argument(s).
        
        Test ID: TEST-T-608
        Requirements: REQ-AWM-601
        """
        objTest = self.TestClass(*self.DefArguments)
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
        
        Test ID: TEST-T-607
        Requirements: REQ-AWM-600
        """
        objTest = self.TestClass(*self.DefArguments)
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
        
        Test ID: TEST-T-608
        Requirements: REQ-AWM-601
        """
        objTest = self.TestClass(*self.DefArguments)
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
        
        Test ID: TEST-T-607
        Requirements: REQ-AWM-600
        """
        objTest = self.TestClass(*self.DefArguments)
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
        
        Test ID: TEST-T-608
        Requirements: REQ-AWM-601
        """
        objTest = self.TestClass(*self.DefArguments)
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
    
    def test_setters_TypeError(self) -> None:
        """
        Checks that improper data types of the argument(s) of the setter
        properties result in TypeError or its sub-class exception.
        
        Test ID: TEST-T-607
        Requirements: REQ-AWM-600
        """
        objTest = self.TestClass(*self.DefArguments)
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            for Attr in self.Parameters:
                with self.assertRaises(TypeError):
                    setattr(objTest, Attr, Value)
        del objTest
    
    def test_setters_ValueError(self) -> None:
        """
        Checks that improper data types of the argument(s) of the setter
        properties result in ValueError or its sub-class exception.
        
        Test ID: TEST-T-608
        Requirements: REQ-AWM-601
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            for Attr in self.Parameters:
                Value = random.randint(-10, -1)
                with self.assertRaises(ValueError):
                    setattr(objTest, Attr, Value)
                Value += random.random()
                with self.assertRaises(ValueError):
                    setattr(objTest, Attr, Value)
        for Attr in self.Parameters:
            with self.assertRaises(ValueError):
                setattr(objTest, Attr, 0)
        del objTest
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-602
        Requirements: REQ-FUN-602
        """
        objTest = self.TestClass(*self.DefArguments)
        Mean = self.DefArguments[0]
        Shape = self.DefArguments[1]
        for _ in range(100):
            self.assertEqual(objTest.Mean, Mean)
            self.assertEqual(objTest.Shape, Shape)
            Var = math.pow(Mean, 3) / Shape
            self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Skew, 3 * math.sqrt(Mean / Shape),
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Kurt, 15 * Mean / Shape,
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
            Mean = random.randint(1, 10)
            if random.random() > 0.5:
                Mean -= random.random()
            if Mean < 0.1:
                Mean = 0.1
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            objTest.Mean = Mean
            objTest.Shape = Shape
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-604
        Requirements ID: REQ-FUN-604
        """
        objTest = self.TestClass(*self.DefArguments)
        Mean = self.DefArguments[0]
        Shape = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.0001:
                    Value = 0.0001
                z = 0.5 * Shape * math.pow(Value - Mean, 2) / Value
                z /= Mean * Mean
                TestResult = objTest.pdf(Value)
                if z > 300:
                    self.assertAlmostEqual(TestResult, 0)
                else:
                    Temp = 0.5 * Shape / math.pi
                    CheckValue = math.sqrt(Temp / math.pow(Value, 3))
                    CheckValue *= math.exp(-z)
                    self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.pdf(-Value), 0)
            self.assertAlmostEqual(objTest.pdf(0), 0)
            Mean = random.randint(1, 10)
            if random.random() > 0.5:
                Mean -= random.random()
            if Mean < 0.1:
                Mean = 0.1
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            objTest.Mean = Mean
            objTest.Shape = Shape
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method.
        
        Test ID: TEST-T-605
        Requirements ID: REQ-FUN-605
        """
        objTest = self.TestClass(*self.DefArguments)
        Mean = self.DefArguments[0]
        Shape = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.0001:
                    Value = 0.0001
                z = math.sqrt(0.5 * Shape / Value) * (Value / Mean - 1)
                y = - math.sqrt(0.5 * Shape / Value) * (Value / Mean + 1)
                CheckValue= 0.5 * (1 + math.erf(y)) * math.exp(2 * Shape / Mean)
                CheckValue += 0.5 * (1 + math.erf(z))
                TestResult = objTest.cdf(Value)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.cdf(-Value), 0)
            self.assertAlmostEqual(objTest.cdf(0), 0)
            Mean = random.randint(1, 10)
            if random.random() > 0.5:
                Mean -= random.random()
            if Mean < 0.1:
                Mean = 0.1
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            objTest.Mean = Mean
            objTest.Shape = Shape
        del objTest
    
    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            for _ in range(100):
                Value = random.random()
                if Value < 0.01:
                    Value = 0.01
                if Value > 0.99:
                    Value = 0.99
                Point = objTest.qf(Value)
                self.assertIsInstance(Point, (int, float))
                self.assertGreater(Point, objTest.Min)
                self.assertLess(Point, objTest.Max)
                self.assertAlmostEqual(objTest.cdf(Point), Value,
                                                places = FLOAT_CHECK_PRECISION)
            Mean = random.randint(1, 10)
            if random.random() > 0.5:
                Mean -= random.random()
            if Mean < 0.1:
                Mean = 0.1
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            objTest.Mean = Mean
            objTest.Shape = Shape
        del objTest
    
    def test_getQuantile(self) -> None:
        """
        Checks the implementation of the getQuantile() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
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
            Mean = random.randint(1, 10)
            if random.random() > 0.5:
                Mean -= random.random()
            if Mean < 0.1:
                Mean = 0.1
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            objTest.Mean = Mean
            objTest.Shape = Shape
        del objTest
    
    def test_random(self) -> None:
        """
        Checks that the method random() generates only real numbers within
        the supported by the distribution range.
        """
        objTest = self.TestClass(*self.DefArguments)
        Min = objTest.Min
        Max = objTest.Max
        for _ in range(1000):
            TestResult = objTest.random()
            self.assertIsInstance(TestResult, (int, float))
            self.assertGreaterEqual(TestResult, Min)
            self.assertLessEqual(TestResult, Max)
        del objTest

class Test_InverseGamma(Test_InverseGaussian):
    """
    Unittests for InverseGamma class from the module
    statistics_lib.inverse_distributions.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.InverseGamma
        cls.Parameters = ('Shape', 'Scale')
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Shape = random.randint(1, 5)
        if random.random() > 0.5:
            Shape -= random.random()
        if Shape < 0.1:
            Shape = 0.1
        Scale = random.randint(1, 10)
        if random.random() > 0.5:
            Scale -= random.random()
        if Scale < 0.1:
            Scale = 0.1
        self.DefArguments = (Shape, Scale)
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-600
        Requirements: REQ-FUN-601
        """
        for _ in range(100):
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest= self.TestClass(Shape, Scale)
            if Shape > 1:
                Mean = Scale / (Shape - 1)
                self.assertAlmostEqual(objTest.Mean, Mean,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Mean)
            if Shape > 2:
                Var = math.pow(Scale / (Shape -1), 2) / (Shape - 2)
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if Shape > 3:
                Skew = 4 * math.sqrt(Shape -2) / (Shape - 3)
                self.assertAlmostEqual(objTest.Skew, Skew,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Skew)
            if Shape > 4:
                Kurt = 6 * (5 * Shape - 11) / ((Shape - 3) * (Shape - 4))
                self.assertAlmostEqual(objTest.Kurt, Kurt,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Kurt)
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
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-602
        Requirements: REQ-FUN-602
        """
        objTest = self.TestClass(*self.DefArguments)
        Shape = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(100):
            self.assertEqual(objTest.Shape, Shape)
            self.assertEqual(objTest.Scale, Scale)
            if Shape > 1:
                Mean = Scale / (Shape - 1)
                self.assertAlmostEqual(objTest.Mean, Mean,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Mean)
            if Shape > 2:
                Var = math.pow(Scale / (Shape -1), 2) / (Shape - 2)
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if Shape > 3:
                Skew = 4 * math.sqrt(Shape -2) / (Shape - 3)
                self.assertAlmostEqual(objTest.Skew, Skew,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Skew)
            if Shape > 4:
                Kurt = 6 * (5 * Shape - 11) / ((Shape - 3) * (Shape - 4))
                self.assertAlmostEqual(objTest.Kurt, Kurt,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Kurt)
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
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Shape = Shape
            objTest.Scale = Scale
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-604
        Requirements ID: REQ-FUN-604
        """
        objTest = self.TestClass(*self.DefArguments)
        Shape = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.0001:
                    Value = 0.0001
                z = Scale / Value
                TestResult = objTest.pdf(Value)
                if z > 300:
                    self.assertAlmostEqual(TestResult, 0)
                else:
                    Temp = - z + Shape * math.log(Scale) - math.lgamma(Shape)
                    Temp -= (Shape + 1) * math.log(Value)
                    CheckValue = math.exp(Temp)
                    self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.pdf(-Value), 0)
            self.assertAlmostEqual(objTest.pdf(0), 0)
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Shape = Shape
            objTest.Scale = Scale
        del objTest

    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method.
        
        Test ID: TEST-T-605
        Requirements ID: REQ-FUN-605
        """
        objTest = self.TestClass(*self.DefArguments)
        Shape = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.0001:
                    Value = 0.0001
                CheckValue= sf.upper_gamma_reg(Shape, Scale / Value)
                TestResult = objTest.cdf(Value)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.cdf(-Value), 0)
            self.assertAlmostEqual(objTest.cdf(0), 0)
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Shape = Shape
            objTest.Scale = Scale
        del objTest

    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            for _ in range(100):
                Value = random.random()
                if Value < 0.01:
                    Value = 0.01
                if Value > 0.99:
                    Value = 0.99
                Point = objTest.qf(Value)
                self.assertIsInstance(Point, (int, float))
                self.assertGreater(Point, objTest.Min)
                self.assertLess(Point, objTest.Max)
                self.assertAlmostEqual(objTest.cdf(Point), Value,
                                                places = FLOAT_CHECK_PRECISION)
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Shape = Shape
            objTest.Scale = Scale
        del objTest
    
    def test_getQuantile(self) -> None:
        """
        Checks the implementation of the getQuantile() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
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
            Shape = random.randint(1, 5)
            if random.random() > 0.5:
                Shape -= random.random()
            if Shape < 0.1:
                Shape = 0.1
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Shape = Shape
            objTest.Scale = Scale
        del objTest

class Test_InverseChiSquared(Test_InverseGaussian):
    """
    Unittests for InverseChiSquared class from the module
    statistics_lib.inverse_distributions.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.InverseChiSquared
        cls.Parameters = ('Degree', )
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Degree = random.randint(1, 40)
        if random.random() > 0.5:
            Degree -= random.random()
        if Degree < 0.5:
            Degree = 0.5
        self.DefArguments = (Degree, )

    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-600
        Requirements: REQ-FUN-601
        """
        for _ in range(100):
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            objTest = self.TestClass(Degree)
            if Degree > 2:
                Mean = 1 / (Degree - 2)
                self.assertAlmostEqual(objTest.Mean, Mean,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Mean)
            if Degree > 4:
                Var = 2 / (math.pow(Degree - 2, 2) * (Degree - 4))
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if Degree > 6:
                Skew = 4 * math.sqrt( 2 * (Degree - 4)) / (Degree - 6)
                self.assertAlmostEqual(objTest.Skew, Skew,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Skew)
            if Degree > 8:
                Kurt = 12 * (5 * Degree - 22) / ((Degree - 6) * (Degree - 8))
                self.assertAlmostEqual(objTest.Kurt, Kurt,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Kurt)
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
        
        Test ID: TEST-T-607
        Requirements: REQ-AWM-600
        """
        for Value in ('1', [1], (1, 2), {1: 1}, int, float, bool):
            with self.assertRaises(TypeError):
                self.TestClass(Value)
    
    def test_init_ValueError(self) -> None:
        """
        Checks that improper values of the argument(s) of the initialization
        method result in ValueError or its sub-class exception.
        
        Test ID: TEST-T-608
        Requirements: REQ-AWM-601
        """
        for _ in range(10):
            NegInt = random.randint(-10, -1)
            NegFloat = NegInt + random.random()
            with self.assertRaises(ValueError):
                self.TestClass(NegInt)
            with self.assertRaises(ValueError):
                self.TestClass(NegFloat)
        with self.assertRaises(ValueError):
            self.TestClass(0)
        with self.assertRaises(ValueError):
            self.TestClass(0.0)
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-602
        Requirements: REQ-FUN-602
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree = self.DefArguments[0]
        for _ in range(100):
            self.assertEqual(objTest.Degree, Degree)
            if Degree > 2:
                Mean = 1 / (Degree - 2)
                self.assertAlmostEqual(objTest.Mean, Mean,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Mean)
            if Degree > 4:
                Var = 2 / (math.pow(Degree - 2, 2) * (Degree - 4))
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if Degree > 6:
                Skew = 4 * math.sqrt( 2 * (Degree - 4)) / (Degree - 6)
                self.assertAlmostEqual(objTest.Skew, Skew,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Skew)
            if Degree > 8:
                Kurt = 12.0 * (5 * Degree - 22) / ((Degree - 6) * (Degree - 8))
                self.assertAlmostEqual(objTest.Kurt, Kurt,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Kurt)
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
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            objTest.Degree = Degree
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-604
        Requirements ID: REQ-FUN-604
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree = self.DefArguments[0]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.01:
                    Value = 0.01
                TestResult = objTest.pdf(Value)
                Temp = - 0.5 * Degree * math.log(2) - math.lgamma(0.5 * Degree)
                Temp -= (0.5 * Degree + 1) * math.log(Value) + 0.5 / Value
                CheckValue = math.exp(Temp)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.pdf(-Value), 0)
            self.assertAlmostEqual(objTest.pdf(0), 0)
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            objTest.Degree = Degree
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method.
        
        Test ID: TEST-T-605
        Requirements ID: REQ-FUN-605
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree = self.DefArguments[0]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.0001:
                    Value = 0.0001
                CheckValue= sf.upper_gamma_reg(0.5 * Degree, 0.5 / Value)
                TestResult = objTest.cdf(Value)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.cdf(-Value), 0)
            self.assertAlmostEqual(objTest.cdf(0), 0)
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            objTest.Degree = Degree
        del objTest

    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            for _ in range(100):
                Value = random.random()
                if Value < 0.01:
                    Value = 0.01
                if Value > 0.99:
                    Value = 0.99
                Point = objTest.qf(Value)
                self.assertIsInstance(Point, (int, float))
                self.assertGreater(Point, objTest.Min)
                self.assertLess(Point, objTest.Max)
                self.assertAlmostEqual(objTest.cdf(Point), Value,
                                                places = FLOAT_CHECK_PRECISION)
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            objTest.Degree = Degree
        del objTest
    
    def test_getQuantile(self) -> None:
        """
        Checks the implementation of the getQuantile() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
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
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            objTest.Degree = Degree
        del objTest

class Test_ScaledInverseChiSquared(Test_InverseGaussian):
    """
    Unittests for ScaledInverseChiSquared class from the module
    statistics_lib.inverse_distributions.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.ScaledInverseChiSquared
        cls.Parameters = ('Degree', 'Scale')
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Degree = random.randint(1, 40)
        if random.random() > 0.5:
            Degree -= random.random()
        if Degree < 0.5:
            Degree = 0.5
        Scale = random.randint(1, 10)
        if random.random() > 0.5:
            Scale -= random.random()
        if Scale < 0.1:
            Scale = 0.1
        self.DefArguments = (Degree, Scale)
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-600
        Requirements: REQ-FUN-601
        """
        for _ in range(100):
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest = self.TestClass(Degree, Scale)
            if Degree > 2:
                Mean = Degree * Scale / (Degree - 2)
                self.assertAlmostEqual(objTest.Mean, Mean,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Mean)
            if Degree > 4:
                Var = 2 * math.pow(Degree * Scale, 2)
                Var /= (math.pow(Degree - 2, 2) * (Degree - 4))
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if Degree > 6:
                Skew = 4 * math.sqrt( 2 * (Degree - 4)) / (Degree - 6)
                self.assertAlmostEqual(objTest.Skew, Skew,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Skew)
            if Degree > 8:
                Kurt = 12 * (5 * Degree - 22) / ((Degree - 6) * (Degree - 8))
                self.assertAlmostEqual(objTest.Kurt, Kurt,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Kurt)
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
        
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-602
        Requirements: REQ-FUN-602
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(100):
            self.assertEqual(objTest.Degree, Degree)
            self.assertEqual(objTest.Scale, Scale)
            if Degree > 2:
                Mean = Degree * Scale / (Degree - 2)
                self.assertAlmostEqual(objTest.Mean, Mean,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Mean)
            if Degree > 4:
                Var = 2 * math.pow(Degree * Scale, 2)
                Var /= (math.pow(Degree - 2, 2) * (Degree - 4))
                self.assertAlmostEqual(objTest.Sigma, math.sqrt(Var),
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.Var, Var,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Sigma)
                self.assertIsNone(objTest.Var)
            if Degree > 6:
                Skew = 4 * math.sqrt( 2 * (Degree - 4)) / (Degree - 6)
                self.assertAlmostEqual(objTest.Skew, Skew,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Skew)
            if Degree > 8:
                Kurt = 12 * (5 * Degree - 22) / ((Degree - 6) * (Degree - 8))
                self.assertAlmostEqual(objTest.Kurt, Kurt,
                                                places = FLOAT_CHECK_PRECISION)
            else:
                self.assertIsNone(objTest.Kurt)
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
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Degree = Degree
            objTest.Scale = Scale
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-604
        Requirements ID: REQ-FUN-604
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.0001:
                    Value = 0.0001
                z = 0.5 * Scale * Degree / Value
                TestResult = objTest.pdf(Value)
                if z > 300:
                    self.assertAlmostEqual(TestResult, 0)
                else:
                    Temp = 0.5 * Degree * math.log(0.5 * Scale * Degree)
                    Temp -= math.lgamma(0.5 * Degree)
                    Temp -= (0.5 * Degree + 1) * math.log(Value) + z
                    CheckValue = math.exp(Temp)
                    self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.pdf(-Value), 0)
            self.assertAlmostEqual(objTest.pdf(0), 0)
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Degree = Degree
            objTest.Scale = Scale
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method.
        
        Test ID: TEST-T-605
        Requirements ID: REQ-FUN-605
        """
        objTest = self.TestClass(*self.DefArguments)
        Degree = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.0001:
                    Value = 0.0001
                CheckValue= sf.upper_gamma_reg(0.5 * Degree,
                                                0.5 * Degree * Scale / Value)
                TestResult = objTest.cdf(Value)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.cdf(-Value), 0)
            self.assertAlmostEqual(objTest.cdf(0), 0)
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Degree = Degree
            objTest.Scale = Scale
        del objTest

    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            for _ in range(100):
                Value = random.random()
                if Value < 0.01:
                    Value = 0.01
                if Value > 0.99:
                    Value = 0.99
                Point = objTest.qf(Value)
                self.assertIsInstance(Point, (int, float))
                self.assertGreater(Point, objTest.Min)
                self.assertLess(Point, objTest.Max)
                self.assertAlmostEqual(objTest.cdf(Point), Value,
                                                places = FLOAT_CHECK_PRECISION)
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Degree = Degree
            objTest.Scale = Scale
        del objTest
    
    def test_getQuantile(self) -> None:
        """
        Checks the implementation of the getQuantile() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
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
            Degree = random.randint(1, 40)
            if random.random() > 0.5:
                Degree -= random.random()
            if Degree < 0.5:
                Degree = 0.5
            Scale = random.randint(1, 10)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Degree = Degree
            objTest.Scale = Scale
        del objTest

class Test_Cauchy(Test_InverseGaussian):
    """
    Unittests for Cauchy class from the module
    statistics_lib.inverse_distributions.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Cauchy
        cls.Parameters = ('Location', 'Scale')
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Location = random.randint(-9, 10)
        if random.random() > 0.5:
            Location -= random.random()
        if Location < 0.1:
            Location = 0.1
        Scale = random.randint(1, 5)
        if random.random() > 0.5:
            Scale -= random.random()
        if Scale < 0.1:
            Scale = 0.1
        self.DefArguments = (Location, Scale)
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-600
        Requirements: REQ-FUN-601
        """
        for _ in range(100):
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest = self.TestClass(Location, Scale)
            self.assertIsNone(objTest.Mean)
            self.assertIsNone(objTest.Sigma)
            self.assertIsNone(objTest.Var)
            self.assertIsNone(objTest.Skew)
            self.assertIsNone(objTest.Kurt)
            self.assertEqual(objTest.Min, -math.inf)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, Location,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, Location - Scale,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, Location + Scale,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_init_ValueError(self) -> None:
        """
        Checks that improper values of the argument(s) of the initialization
        method result in ValueError or its sub-class exception.
        
        Test ID: TEST-T-608
        Requirements: REQ-AWM-601
        """
        for _ in range(10):
            Location = random.randint(-10, 10) + random.random()
            NegInt = random.randint(-10, -1)
            NegFloat = NegInt + random.random()
            with self.assertRaises(ValueError):
                self.TestClass(Location, NegInt)
            with self.assertRaises(ValueError):
                self.TestClass(Location, NegFloat)
        with self.assertRaises(ValueError):
            self.TestClass(Location, 0)
        with self.assertRaises(ValueError):
            self.TestClass(Location, 0.0)
    
    def test_setters_ValueError(self) -> None:
        """
        Checks that improper data types of the argument(s) of the setter
        properties result in ValueError or its sub-class exception.
        
        Test ID: TEST-T-608
        Requirements: REQ-AWM-601
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Value = random.randint(-10, -1)
            with self.assertRaises(ValueError):
                objTest.Scale = Value
            Value += random.random()
            with self.assertRaises(ValueError):
                objTest.Scale = Value
        with self.assertRaises(ValueError):
            objTest.Scale = 0
        del objTest
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-602
        Requirements: REQ-FUN-602
        """
        objTest = self.TestClass(*self.DefArguments)
        Location = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(100):
            self.assertEqual(objTest.Location, Location)
            self.assertEqual(objTest.Scale, Scale)
            self.assertIsNone(objTest.Mean)
            self.assertIsNone(objTest.Sigma)
            self.assertIsNone(objTest.Var)
            self.assertIsNone(objTest.Skew)
            self.assertIsNone(objTest.Kurt)
            self.assertEqual(objTest.Min, -math.inf)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, Location,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, Location - Scale,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, Location + Scale,
                                                places = FLOAT_CHECK_PRECISION)
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Location = Location
            objTest.Scale = Scale
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-604
        Requirements ID: REQ-FUN-604
        """
        objTest = self.TestClass(*self.DefArguments)
        Location = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = Location + random.randint(-9, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                TestResult = objTest.pdf(Value)
                Temp = 1 / (1 + math.pow((Value - Location) / Scale , 2))
                CheckValue = Temp / (math.pi * Scale)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Location = Location
            objTest.Scale = Scale
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method.
        
        Test ID: TEST-T-605
        Requirements ID: REQ-FUN-605
        """
        objTest = self.TestClass(*self.DefArguments)
        Location = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = Location + random.randint(-9, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                CheckValue=math.atan((Value - Location) / Scale) / math.pi + 0.5
                TestResult = objTest.cdf(Value)
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Location = Location
            objTest.Scale = Scale
        del objTest

    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Location = objTest.Location
            Scale = objTest.Scale
            for _ in range(100):
                Value = random.random()
                if Value < 0.01:
                    Value = 0.01
                if Value > 0.99:
                    Value = 0.99
                Point = objTest.qf(Value)
                self.assertIsInstance(Point, (int, float))
                self.assertGreater(Point, objTest.Min)
                self.assertLess(Point, objTest.Max)
                CheckValue=Location + Scale * math.tan(math.pi * (Value - 0.5))
                self.assertAlmostEqual(Point, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.cdf(Point), Value,
                                                places = FLOAT_CHECK_PRECISION)
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Location = Location
            objTest.Scale = Scale
        del objTest
    
    def test_getQuantile(self) -> None:
        """
        Checks the implementation of the getQuantile() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
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
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Location = Location
            objTest.Scale = Scale
        del objTest

class Test_Levy(Test_Cauchy):
    """
    Unittests for Levy class from the module
    statistics_lib.inverse_distributions.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Levy
    
    def test_init(self) -> None:
        """
        Checks that the class can be instantiated, and the parameters of the
        distribution are properly assigned
        
        Test ID: TEST-T-600
        Requirements: REQ-FUN-601
        """
        for _ in range(100):
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest = self.TestClass(Location, Scale)
            self.assertEqual(objTest.Mean, math.inf)
            self.assertEqual(objTest.Sigma, math.inf)
            self.assertEqual(objTest.Var, math.inf)
            self.assertIsNone(objTest.Skew)
            self.assertIsNone(objTest.Kurt)
            self.assertAlmostEqual(objTest.Min, Location)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, Location + 2.198109 * Scale,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, Location + 0.755684 * Scale,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, Location + 9.849204 * Scale,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Parameters(self) -> None:
        """
        Checks that the parameters of the distribution can be changed at any
        time.
        
        Test ID: TEST-T-602
        Requirements: REQ-FUN-602
        """
        objTest = self.TestClass(*self.DefArguments)
        Location = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(100):
            self.assertEqual(objTest.Location, Location)
            self.assertEqual(objTest.Scale, Scale)
            self.assertEqual(objTest.Mean, math.inf)
            self.assertEqual(objTest.Sigma, math.inf)
            self.assertEqual(objTest.Var, math.inf)
            self.assertIsNone(objTest.Skew)
            self.assertIsNone(objTest.Kurt)
            self.assertAlmostEqual(objTest.Min, Location)
            self.assertEqual(objTest.Max, math.inf)
            self.assertAlmostEqual(objTest.Median, Location + 2.198109 * Scale,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q1, Location + 0.755684 * Scale,
                                                places = FLOAT_CHECK_PRECISION)
            self.assertAlmostEqual(objTest.Q3, Location + 9.849204 * Scale,
                                                places = FLOAT_CHECK_PRECISION)
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Location = Location
            objTest.Scale = Scale
        del objTest
    
    def test_pdf(self) -> None:
        """
        Checks the implementation of the pdf() method.
        
        Test ID: TEST-T-604
        Requirements ID: REQ-FUN-604
        """
        objTest = self.TestClass(*self.DefArguments)
        Location = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.001:
                    Value = 0.001
                TestResult = objTest.pdf(Location + Value)
                z = 0.5 * Scale / Value
                if z > 300:
                    self.assertAlmostEqual(TestResult, 0)
                else:
                    Temp = - z + 1.5 * math.log(z) - math.log(Scale)
                    CheckValue = 2 * math.exp(Temp) / math.sqrt(math.pi)
                    self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.pdf(Location - Value), 0)
            self.assertAlmostEqual(objTest.pdf(Location), 0)
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Location = Location
            objTest.Scale = Scale
        del objTest
    
    def test_cdf(self) -> None:
        """
        Checks the implementation of the cdf() method.
        
        Test ID: TEST-T-605
        Requirements ID: REQ-FUN-605
        """
        objTest = self.TestClass(*self.DefArguments)
        Location = self.DefArguments[0]
        Scale = self.DefArguments[1]
        for _ in range(10):
            for _ in range(100):
                Value = random.randint(1, 10)
                if random.random() > 0.5:
                    Value -= random.random()
                if Value < 0.001:
                    Value = 0.001
                TestResult = objTest.cdf(Location + Value)
                CheckValue = 1 - math.erf(math.sqrt(0.5 * Scale / Value))
                self.assertAlmostEqual(TestResult, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.cdf(Location - Value), 0)
            self.assertAlmostEqual(objTest.cdf(Location), 0)
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Location = Location
            objTest.Scale = Scale
        del objTest

    def test_qf(self) -> None:
        """
        Checks the implementation of the qf() method.
        
        Test ID: TEST-T-606
        Requirements ID: REQ-FUN-606
        """
        objTest = self.TestClass(*self.DefArguments)
        for _ in range(10):
            Location = objTest.Location
            Scale = objTest.Scale
            for _ in range(100):
                Value = random.random()
                if Value < 0.01:
                    Value = 0.01
                if Value > 0.99:
                    Value = 0.99
                Point = objTest.qf(Value)
                self.assertIsInstance(Point, (int, float))
                self.assertGreater(Point, objTest.Min)
                self.assertLess(Point, objTest.Max)
                Temp = math.pow(sf.inv_erf(1 - Value), 2)
                CheckValue=Location + 0.5 * Scale / Temp
                self.assertAlmostEqual(Point, CheckValue,
                                                places = FLOAT_CHECK_PRECISION)
                self.assertAlmostEqual(objTest.cdf(Point), Value,
                                                places = FLOAT_CHECK_PRECISION)
            Location = random.randint(-9, 10)
            if random.random() > 0.5:
                Location -= random.random()
            if Location < 0.1:
                Location = 0.1
            Scale = random.randint(1, 5)
            if random.random() > 0.5:
                Scale -= random.random()
            if Scale < 0.1:
                Scale = 0.1
            objTest.Location = Location
            objTest.Scale = Scale
        del objTest

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_InverseGaussian)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_InverseGamma)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_InverseChiSquared)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(
                                                Test_ScaledInverseChiSquared)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_Cauchy)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_Levy)

TestSuite = unittest.TestSuite()

TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                        TestSuite6])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting statistics_lib.inverse_distributions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
