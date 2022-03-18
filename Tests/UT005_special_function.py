"""
Module statistics_lib.Tests.UT005_special_functions

Set of unit tests on the module stastics_lib.special_functions. See the test
plan / report TE005_special_functions.md
"""


__version__= '1.0.0.0'
__date__ = '18-03-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import unittest
import random
import math

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.special_functions as test_module

#globals

FLOAT_CHECK_PRECISION = 5 #digits after comma, mostly due to precision of
#+ the reference tables + internal Python implementation of the special
#+ functions

#classes

#+ test cases

class Test_factorial(unittest.TestCase):
    """
    Sanity check - basically, not required, since the Standard Python Library
    is supposed to be properly tested. Just to make sure that the conventions
    are not changed.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(math.factorial)
    
    def test_Ok(self):
        """
        Checks that the function returns positive integer value with the non-
        negative integer input, which is of the expected value. The test
        values are calculated manually.

        Version 1.0.0.0
        """
        for Input, Output in ( (0, 1), (1, 1), (2, 2), (3, 6), (4, 24),
                                (5, 120), (6, 720), (7, 5040), (8, 40320),
                                (9, 362880), (10, 3628800), (11, 39916800),
                                (12, 479001600), (13, 6227020800),
                                (14, 87178291200), (15, 1307674368000),
                                (16, 20922789888000), (17, 355687428096000),
                                (18, 6402373705728000),
                                (19, 121645100408832000),
                                (20, 2432902008176640000)):
            TestResult = self.TestFunction(Input)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, Output)
        for _ in range(100):
            TestResult = self.TestFunction(random.randint(21, 1000))
            self.assertIsInstance(TestResult, int)

class Test_gamma(unittest.TestCase):
    """
    Sanity check - basically, not required, since the Standard Python Library
    is supposed to be properly tested. Just to make sure that the conventions
    are not changed.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(math.gamma)
    
    def test_Ok(self):
        """
        Checks that the function returns positive floating point value with the
        positive integer or floating point input, which is of the expected
        value.

        The test values are taken directly or calculated from the ones provided
        in:

        Reliability Engineering, First Ed. Kailash C. Kapur. Published by
        John Wiley & Sons, Inc. (2014).
        https://onlinelibrary.wiley.com/doi/pdf/10.1002/9781118841716.app2

        Version 1.0.0.0
        """
        for Input, Output in ((1, 1.00000), (1.0, 1.00000),
                                (2, 1.00000), (2.0, 1.00000),
                                (3, 2.00000), (3.0, 2.00000),
                                (4, 6.00000), (4.0, 6.00000),
                                (5, 2.40000E1), (5.0, 2.40000E1),
                                (6, 1.20000E2), (6.0, 1.20000E2),
                                (7, 7.20000E2), (7.0, 7.20000E2),
                                (1.01, 0.99433), (1.10, 0.95135),
                                (1.50, 0.88623), (1.75, 0.91906),
                                (0.01, 0.9943259E2), (0.10, 0.951351E1),
                                (0.50, 1.77245), (0.75, 1.22542),
                                (2.01, 1.00427), (2.10, 1.04649),
                                (2.50, 1.32934), (2.75, 1.60836)):
            TestResult = self.TestFunction(Input)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, Output,
                                                places = FLOAT_CHECK_PRECISION)
        for _ in range(1000):
            Input = random.randint(1, 100) + random.random()
            TestResult = self.TestFunction(Input)
            self.assertIsInstance(TestResult, float)
            TestResult2 = self.TestFunction(Input + 1)
            Check = TestResult * Input
            Delta = Check / pow(10, FLOAT_CHECK_PRECISION)
            self.assertIsInstance(TestResult2, float)
            self.assertAlmostEqual(TestResult2, Check, delta = Delta)

class Test_erf(unittest.TestCase):
    """
    Sanity check - basically, not required, since the Standard Python Library
    is supposed to be properly tested. Just to make sure that the conventions
    are not changed.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(math.erf)
    
    def test_Ok(self):
        """
        Checks that the function returns positive floating point value with the
        positive integer or floating point input, which is of the expected
        value.

        The test values are taken directly or calculated from the ones provided
        in:

        Iraj Javandel, Christine Doughty, Chin-Fu Tsang
        Groundwater Transport: Handbook of Mathematical Models.
        Published by John Wiley & Sons, Inc. (2013).
        https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1002/9781118665473.app7

        Version 1.0.0.0
        """
        for Input, Output in ((0, 0.00000), (0.0, 0.00000),
                                (0.02, 0.022564), (0.04, 0.04511),
                                (0.1, 0.11246), (0.2, 0.22270),
                                (0.3, 0.328626), (0.4, 0.428392),
                                (0.5, 0.520500), (0.8, 0.74210),
                                (1, 0.84270), (1.5, 0.96611),
                                (2, 0.99532), (2.5, 0.99959),
                                (3, 0.99998), (3.5, 0.999999)):
            TestResult = self.TestFunction(Input)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, Output,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(- Input)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, - Output,
                                                places = FLOAT_CHECK_PRECISION)

class Test_permutation(unittest.TestCase):
    """
    Checks the implementation of the function special_functions.permutation().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-510.
    Covers requirements: REQ-FUN-510, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.permutation)
    
    def test_TypeError(self):
        """
        Checks that sub-class TypeError is raised with non-integer argument.

        Test ID: TEST-T-500
        Requirement(s): REQ-AWM-500

        Version 1.0.0.0
        """
        for Value in [1.0, int, float, [1, 2], '1', (1, 1), {1 : 1}, bool]:
            with self.assertRaises(TypeError):
                self.TestFunction(Value, 1)
            with self.assertRaises(TypeError):
                self.TestFunction(1, Value)
            with self.assertRaises(TypeError):
                self.TestFunction(Value, Value)
    
    def test_ValueError(self):
        """
        Checks that sub-class ValueError is raised with wrong value argument.

        Test ID: TEST-T-501
        Requirement(s): REQ-AWM-501

        Version 1.0.0.0
        """
        for _ in range(100):
            Value = - random.randint(1, 100)
            with self.assertRaises(ValueError):
                self.TestFunction(Value, 1)
            with self.assertRaises(ValueError):
                self.TestFunction(1, Value)
            with self.assertRaises(ValueError):
                self.TestFunction(Value, Value)
            n = random.randint(1, 100)
            k = n + random.randint(1, 100)
            with self.assertRaises(ValueError):
                self.TestFunction(n, k)
    
    def test_OK(self):
        """
        Checks that the k-permutations are calculated properly. The pre-defined
        values are calculated manually.

        Test ID: TEST-T-510
        Requirement(s): REQ-FUN-510.

        Version 1.0.0.0
        """
        for n, k, p in ((0, 0, 1), (1, 0, 1), (1, 1, 1), (2, 0, 1), (2, 1, 2),
                            (2, 2, 2), (3, 0, 1), (3, 1, 3), (3, 2, 6),
                            (3, 3, 6), (4, 0, 1), (4, 1, 4), (4, 2, 12),
                            (4, 3, 24), (4, 4, 24), (5, 0, 1), (5, 1, 5),
                            (5, 2, 20), (5, 3, 60), (5, 4, 120), (5, 5, 120)):
            TestResult = self.TestFunction(n, k)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, p)
        for _ in range(100):
            n = random.randint(6, 1000)
            TestResult = self.TestFunction(n, 0)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, 1)
            TestResult = self.TestFunction(n, 1)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, n)
            TestResult = self.TestFunction(n, n-1)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, math.factorial(n))
            TestResult = self.TestFunction(n, n)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, math.factorial(n))
            k = random.randint(2, n-1)
            TestResult = self.TestFunction(n, k)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, math.factorial(n)//math.factorial(n-k))

class Test_combination(Test_permutation):
    """
    Checks the implementation of the function special_functions.combination().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-520.
    Covers requirements: REQ-FUN-520, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.combination)
    
    def test_OK(self):
        """
        Checks that the binomial coefficients are calculated properly. The
        pre-defined values are calculated manually.

        Test ID: TEST-T-510
        Requirement(s): REQ-FUN-510.

        Version 1.0.0.0
        """
        for n, k, p in ((0, 0, 1), (1, 0, 1), (1, 1, 1), (2, 0, 1), (2, 1, 2),
                            (2, 2, 1), (3, 0, 1), (3, 1, 3), (3, 2, 3),
                            (3, 3, 1), (4, 0, 1), (4, 1, 4), (4, 2, 6),
                            (4, 3, 4), (4, 4, 1), (5, 0, 1), (5, 1, 5),
                            (5, 2, 10), (5, 3, 10), (5, 4, 5), (5, 5, 1)):
            TestResult = self.TestFunction(n, k)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, p)
        for _ in range(100):
            n = random.randint(6, 1000)
            TestResult = self.TestFunction(n, 0)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, 1)
            TestResult = self.TestFunction(n, 1)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, n)
            TestResult = self.TestFunction(n, n-1)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, n)
            TestResult = self.TestFunction(n, n)
            self.assertIsInstance(TestResult, int)
            self.assertEqual(TestResult, 1)
            k = random.randint(2, n-1)
            TestResult = self.TestFunction(n, k)
            self.assertIsInstance(TestResult, int)
            Check = math.factorial(n)//(math.factorial(n-k) * math.factorial(k))
            self.assertEqual(TestResult, Check)

class Test_beta(unittest.TestCase):
    """
    Checks the implementation of the function special_functions.beta().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-540.
    Covers requirements: REQ-FUN-540, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.beta)
    
    def test_TypeError(self):
        """
        Checks that sub-class TypeError is raised with non-integer argument.

        Test ID: TEST-T-500
        Requirement(s): REQ-AWM-500

        Version 1.0.0.0
        """
        for Value in [int, float, [1, 2], '1', (1, 1), {1 : 1}, bool]:
            with self.assertRaises(TypeError):
                self.TestFunction(Value, 1)
            with self.assertRaises(TypeError):
                self.TestFunction(1, Value)
            with self.assertRaises(TypeError):
                self.TestFunction(Value, Value)
    
    def test_ValueError(self):
        """
        Checks that sub-class ValueError is raised with wrong value argument.

        Test ID: TEST-T-501
        Requirement(s): REQ-AWM-501

        Version 1.0.0.0
        """
        for _ in range(100):
            Value = - random.randint(1, 100)
            with self.assertRaises(ValueError):
                self.TestFunction(Value, 1)
            with self.assertRaises(ValueError):
                self.TestFunction(1, Value)
            with self.assertRaises(ValueError):
                self.TestFunction(Value, Value)
            with self.assertRaises(ValueError):
                self.TestFunction(-Value, 0)
            with self.assertRaises(ValueError):
                self.TestFunction(0, -Value)
            with self.assertRaises(ValueError):
                self.TestFunction(0, 0)
            Value += random.random()
            with self.assertRaises(ValueError):
                self.TestFunction(Value, 1)
            with self.assertRaises(ValueError):
                self.TestFunction(1, Value)
            with self.assertRaises(ValueError):
                self.TestFunction(Value, Value)
            with self.assertRaises(ValueError):
                self.TestFunction(-Value, 0)
            with self.assertRaises(ValueError):
                self.TestFunction(0, -Value)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly. The pre-defined values
        are obtained with help of:

        https://www.allmath.com/beta-function.php

        Test ID: TEST-T-540
        Requirement(s): REQ-FUN-540.

        Version 1.0.0.0
        """
        for x, y, b in ((0.25, 0.25, 7.41630), (0.25, 0.5, 5.24412),
                            (0.25, 0.75, 4.44288), (0.25, 1.25, 3.70815),
                            (0.25, 1.5, 3.49608), (0.25, 2.5, 2.99664),
                            (0.5, 0.125, 9.30874), (0.5, 0.5, 3.14159),
                            (0.5, 0.75, 2.39628), (0.5, 1.25, 1.74804),
                            (0.5, 1.5, 1.57080), (0.5, 2.5, 1.17810),
                            (5, 2, 0.03333), (5, 3, 0.00952), (5, 4, 0.00357),
                            (5, 5, 0.0015873)):
            TestResult = self.TestFunction(x, y)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, b, FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(y, x)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, b, FLOAT_CHECK_PRECISION)
            #known edge cases!
            TestResult = self.TestFunction(1, y)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, 1/y, FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(x, 1)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, 1/x, FLOAT_CHECK_PRECISION)

class Test_log_beta(Test_beta):
    """
    Checks the implementation of the function special_functions.log_beta().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-540.
    Covers requirements: REQ-FUN-540, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.log_beta)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly. The pre-defined values
        are obtained with help of:

        https://www.allmath.com/beta-function.php

        Test ID: TEST-T-540
        Requirement(s): REQ-FUN-540.

        Version 1.0.0.0
        """
        for x, y, b in ((0.25, 0.25, 7.41630), (0.25, 0.5, 5.24412),
                            (0.25, 0.75, 4.44288), (0.25, 1.25, 3.70815),
                            (0.25, 1.5, 3.49608), (0.25, 2.5, 2.99664),
                            (0.5, 0.125, 9.30874), (0.5, 0.5, 3.14159),
                            (0.5, 0.75, 2.39628), (0.5, 1.25, 1.74804),
                            (0.5, 1.5, 1.57080), (0.5, 2.5, 1.17810),
                            (5, 2, 0.03333), (5, 3, 0.00952), (5, 4, 0.00357),
                            (5, 5, 0.0015873)):
            TestResult = self.TestFunction(x, y)
            Check = math.log(b)
            #note the lost of precision. In fact, log vesion is more precise,
            #+ but the online calculator has a finite precision and gives
            #+ very limited number of digits
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, Check, FLOAT_CHECK_PRECISION - 2)
            TestResult = self.TestFunction(y, x)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, Check, FLOAT_CHECK_PRECISION - 2)
            #known edge cases!
            TestResult = self.TestFunction(1, y)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, -math.log(y),
                                                    FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(x, 1)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, -math.log(x),
                                                    FLOAT_CHECK_PRECISION)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_factorial)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_gamma)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_erf)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_permutation)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_combination)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_beta)
TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_log_beta)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                        TestSuite6, TestSuite7])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.special_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
