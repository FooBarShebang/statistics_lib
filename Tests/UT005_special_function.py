#usr/bin/python3
"""
Module statistics_lib.Tests.UT005_special_functions

Set of unit tests on the module stastics_lib.special_functions. See the test
plan / report TE005_special_functions.md
"""


__version__= '1.0.0.0'
__date__ = '07-04-2022'
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

# regularized incomplete beta function values
#+ https://keisan.casio.com/exec/system/1180573396

RIBF_Z = (0.1, 0.3, 0.5, 0.7, 0.9)

RIBFZ_X_Y = (0.5, 1, 1.5, 2, 2.5, 3, 3.5)

RIBF = (
    ((0.204833, 0.051317, 0.013847, 0.003883, 0.001114, 0.000325, 0.000096),
    (0.316228, 0.1, 0.031623, 0.01, 0.003162, 0.001, 0.000316),
    (0.395819, 0.146185, 0.052044, 0.018113, 0.006207, 0.002104, 0.000707),
    (0.45853, 0.19, 0.074314, 0.028, 0.010277, 0.0037, 0.001312),
    (0.51041, 0.231567, 0.097881, 0.039458, 0.015375, 0.005839, 0.002174),
    (0.554584, 0.271, 0.122341, 0.0523, 0.021484, 0.00856, 0.003329),
    (0.592916, 0.30841, 0.147384, 0.066353, 0.028576, 0.011891, 0.004814)),
    ((0.36901, 0.16334, 0.077274, 0.037841, 0.018927, 0.009604, 0.004924),
    (0.547723, 0.3, 0.164317, 0.09, 0.049295, 0.027, 0.014789),
    (0.660746, 0.414338, 0.252316, 0.15079, 0.088944, 0.05196, 0.03013),
    (0.739425, 0.51, 0.336849, 0.216, 0.135561, 0.0837, 0.05102),
    (0.796889, 0.590037, 0.415688, 0.282564, 0.186967, 0.121141, 0.077181),
    (0.840069, 0.657, 0.487815, 0.3483, 0.241238, 0.16308, 0.108086),
    (0.87313, 0.713026, 0.55292, 0.411703, 0.296753, 0.208309, 0.143053)),
    ((0.5, 0.292893, 0.18169, 0.116117, 0.075587, 0.049825, 0.033146),
    (0.707107, 0.5, 0.353553, 0.25, 0.176777, 0.125, 0.088388),
    (0.81831, 0.646447, 0.5, 0.381282, 0.287793, 0.215553, 0.160469),
    (0.883883, 0.75, 0.618718, 0.5, 0.397748, 0.3125, 0.243068),
    (0.924413, 0.823223, 0.712207, 0.602252, 0.5, 0.408903, 0.330235),
    (0.950175, 0.875, 0.784447, 0.6875, 0.591097, 0.5, 0.417083),
    (0.966854, 0.911612, 0.839531, 0.756932, 0.669765, 0.582917, 0.5)),
    ((0.63099, 0.452277, 0.339254, 0.260575, 0.203111, 0.159931, 0.12687),
    (0.83666, 0.7, 0.585662, 0.49, 0.409963, 0.343, 0.286974),
    (0.922726, 0.835683, 0.747684, 0.663151, 0.584312, 0.512185, 0.44708),
    (0.962159, 0.91, 0.84921, 0.784, 0.717436, 0.6517, 0.588297),
    (0.981073, 0.950705, 0.911056, 0.864439, 0.813033, 0.758762, 0.703247),
    (0.990396, 0.973, 0.94804, 0.9163, 0.878859, 0.83692, 0.791691),
    (0.995076, 0.985211, 0.96987, 0.94898, 0.922819, 0.891914, 0.856947)),
    ((0.795167, 0.683772, 0.604181, 0.54147, 0.48959, 0.445416, 0.407084),
    (0.948683, 0.9, 0.853815, 0.81, 0.768433, 0.729, 0.69159),
    (0.986153, 0.968377, 0.947956, 0.925686, 0.902119, 0.877659, 0.852616),
    (0.996117, 0.99, 0.981887, 0.972, 0.960542, 0.9477, 0.933647),
    (0.998886, 0.996838, 0.993793, 0.989723, 0.984625, 0.978516, 0.971424),
    (0.999675, 0.999, 0.997896, 0.9963, 0.994161, 0.99144, 0.988109),
    (0.999904, 0.999684, 0.999293, 0.998687, 0.997826, 0.996671, 0.995186)))

# regularized incomplete beta function values
#+ https://keisan.casio.com/exec/system/1180573447
#+ https://keisan.casio.com/exec/system/1180573444

RLIGF_X = (0.5, 1, 2.5, 5, 7.5, 10) #power parameter

RLIGF_Y = (0.5, 1, 2.5, 5, 7.5, 10, 15) #integration limit

RLIGF = ((0.6826895, 0.8427008, 0.9746527, 0.9984346, 0.9998925, 0.999992, 1.0),
        (0.3934693, 0.6321206, 0.917915, 0.993262, 0.9994469, 0.9999546, 1.0),
        (0.0374342, 0.150855, 0.58412, 0.924765, 0.989638, 0.9987506, 0.999986),
        (0.0001721, 0.0036599, 0.108822, 0.5595067, 0.8679381, 0.9707473,
                                                                    0.9991433),
        (0.0, 0.0000297, 0.0078736, 0.1802601, 0.5485828, 0.8280673, 0.9880785),
        (0.0, 0.0000001, 0.0002774, 0.0318281, 0.2235924, 0.5420703, 0.9301463))

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

class Test_inv_erf(unittest.TestCase):
    """
    Checks the implementation of the function special_functions.inv_erf().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-530.
    Covers requirements: REQ-FUN-530, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.inv_erf)
    
    def test_TypeError(self):
        """
        Checks that sub-class TypeError is raised with non-integer argument.

        Test ID: TEST-T-500
        Requirement(s): REQ-AWM-500

        Version 1.0.0.0
        """
        for Value in [int, float, [1, 2], '1', (1, 1), {1 : 1}, bool]:
            with self.assertRaises(TypeError):
                self.TestFunction(Value)
    
    def test_ValueError(self):
        """
        Checks that sub-class ValueError is raised with wrong value argument.

        Test ID: TEST-T-501
        Requirement(s): REQ-AWM-501

        Version 1.0.0.0
        """
        for _ in range(100):
            Value = random.randint(1, 10)
            with self.assertRaises(ValueError):
                self.TestFunction(Value)
            with self.assertRaises(ValueError):
                self.TestFunction(-Value)
            Value += random.random()
            with self.assertRaises(ValueError):
                self.TestFunction(Value)
            with self.assertRaises(ValueError):
                self.TestFunction(-Value)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly. The pre-defined values
        are obtained with help of a table given in:

        Iraj Javandel, Christine Doughty, Chin-Fu Tsang
        Groundwater Transport: Handbook of Mathematical Models.
        Published by John Wiley & Sons, Inc. (2013).
        https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1002/9781118665473.app7
        
        with adjustments for the precision of the table itself and of the
        used inv_erf algorithm.

        Test ID: TEST-T-530
        Requirement(s): REQ-FUN-530.

        Version 1.0.0.0
        """
        for Output, Input in ((0, 0.00000), (0.0, 0.00000),
                                (0.02, 0.022564), (0.04, 0.04511),
                                (0.1, 0.11246), (0.2, 0.22270),
                                (0.3, 0.328626), (0.4, 0.428392),
                                (0.5, 0.520500), (0.8, 0.74210),
                                (1, 0.84270), (1.50004, 0.96611),
                                (1.99989, 0.99532), (2.49861, 0.99959),
                                (3.01573, 0.99998), (3.45891, 0.999999)):
            TestResult = self.TestFunction(Input)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, Output,
                                                places = FLOAT_CHECK_PRECISION)
            TestResult = self.TestFunction(- Input)
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, - Output,
                                                places = FLOAT_CHECK_PRECISION)
        #just random numbers checks - inversivility with 7 digits precision
        #+ with respect to the Standard Library math.erf() implementation
        for _ in range(100):
            Input = 2 * random.random() - 1
            if Input > -1:
                TestResult = self.TestFunction(Input)
                self.assertIsInstance(TestResult, float)
                self.assertAlmostEqual(math.erf(TestResult), Input)
        for _ in range(100):
            Input = random.random() * random.randint(0, 4)
            TestResult = self.TestFunction(math.erf(Input))
            self.assertIsInstance(TestResult, float)
            self.assertAlmostEqual(TestResult, Input)

class Test_beta_incomplete_reg(unittest.TestCase):
    """
    Checks the implementation of the function
    special_functions.beta_incomplete_reg().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-550.
    Covers requirements: REQ-FUN-550, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.beta_incomplete_reg)
    
    def test_TypeError(self):
        """
        Checks that sub-class TypeError is raised with non-integer argument.

        Test ID: TEST-T-500
        Requirement(s): REQ-AWM-500

        Version 1.0.0.0
        """
        for Value in [int, float, [1, 2], '1', (1, 1), {1 : 1}, bool]:
            with self.assertRaises(TypeError):
                self.TestFunction(Value, 1, 1)
            with self.assertRaises(TypeError):
                self.TestFunction(0.5, Value, 1)
            with self.assertRaises(TypeError):
                self.TestFunction(0.5, 1, Value)
            with self.assertRaises(TypeError):
                self.TestFunction(Value, Value, 1)
            with self.assertRaises(TypeError):
                self.TestFunction(Value, 1, Value)
            with self.assertRaises(TypeError):
                self.TestFunction(0.5, Value, Value)
            with self.assertRaises(TypeError):
                self.TestFunction(Value, Value, Value)
    
    def test_ValueError(self):
        """
        Checks that sub-class ValueError is raised with wrong value argument.

        Test ID: TEST-T-501
        Requirement(s): REQ-AWM-501

        Version 1.0.0.0
        """
        for _ in range(100):
            ValueInt = - random.randint(1, 10)
            ValueFloat = - (random.random() + 0.0000001)
            ValueMix = ValueInt + ValueFloat
            for Value in (ValueInt, ValueFloat, ValueMix): #negative values
                with self.assertRaises(ValueError):
                    self.TestFunction(Value, 1, 1)
                with self.assertRaises(ValueError):
                    self.TestFunction(0.5, Value, 1)
                with self.assertRaises(ValueError):
                    self.TestFunction(0.5, 1, Value)
                with self.assertRaises(ValueError):
                    self.TestFunction(Value, Value, 1)
                with self.assertRaises(ValueError):
                    self.TestFunction(0.5, Value, Value)
                with self.assertRaises(ValueError):
                    self.TestFunction(Value, 1, Value)
                with self.assertRaises(ValueError):
                    self.TestFunction(Value, Value, Value)
            #special cases
            #+ zero x or y
            with self.assertRaises(ValueError):
                self.TestFunction(- ValueFloat, 0, 1)
            with self.assertRaises(ValueError):
                self.TestFunction(- ValueFloat, 1, 0)
            with self.assertRaises(ValueError):
                self.TestFunction(- ValueFloat, 0, 0)
            #+ z > 1
            with self.assertRaises(ValueError):
                self.TestFunction(- ValueMix, 0, 1)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly. The pre-defined values
        are obtained with help of an online calculator:

        https://keisan.casio.com/exec/system/1180573396
        
        with adjustments for the precision of the table itself and of the
        used inv_erf algorithm.

        Test ID: TEST-T-550
        Requirement(s): REQ-FUN-550.

        Version 1.0.0.0
        """
        for IndZ, z in enumerate(RIBF_Z):
            for IndY, y in enumerate(RIBFZ_X_Y):
                for IndX, x in enumerate(RIBFZ_X_Y):
                    Check = RIBF[IndZ][IndY][IndX]
                    TestValue = self.TestFunction(z, x, y)
                    strError = 'for I_{}({}, {})'.format(z, x, y)
                    self.assertIsInstance(TestValue, float)
                    self.assertAlmostEqual(TestValue, Check,
                                                places = FLOAT_CHECK_PRECISION,
                                                                msg = strError)
        #special cases
        for IndY, y in enumerate(RIBFZ_X_Y):
            for IndX, x in enumerate(RIBFZ_X_Y):
                TestValue = self.TestFunction(0, x, y)
                self.assertIsInstance(TestValue, float)
                self.assertAlmostEqual(TestValue, 0.0)
                TestValue = self.TestFunction(1, x, y)
                self.assertIsInstance(TestValue, float)
                self.assertAlmostEqual(TestValue, 1.0)

class Test_beta_incomplete(Test_beta_incomplete_reg):
    """
    Checks the implementation of the function
    special_functions.beta_incomplete().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-550.
    Covers requirements: REQ-FUN-550, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.beta_incomplete)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly, using the previously
        tested functions.

        Test ID: TEST-T-550
        Requirement(s): REQ-FUN-550.

        Version 1.0.0.0
        """
        for _ in range(1000):
            z = random.random()
            x = random.random() + random.randint(1, 10)
            y = random.random() + random.randint(1, 10)
            TestValue = self.TestFunction(z, x, y)
            Check = test_module.beta_incomplete_reg(z, x, y)
            Check *= test_module.beta(x, y)
            self.assertIsInstance(TestValue, float)
            self.assertAlmostEqual(TestValue, Check)
        #special cases
        for y in RIBFZ_X_Y:
            for x in RIBFZ_X_Y:
                TestValue = self.TestFunction(0, x, y)
                self.assertIsInstance(TestValue, float)
                self.assertAlmostEqual(TestValue, 0.0)
                TestValue = self.TestFunction(1, x, y)
                Check = test_module.beta(x, y)
                self.assertIsInstance(TestValue, float)
                self.assertAlmostEqual(TestValue, Check)

class Test_log_beta_incomplete(Test_beta_incomplete_reg):
    """
    Checks the implementation of the function
    special_functions.log_beta_incomplete().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-550.
    Covers requirements: REQ-FUN-550, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.log_beta_incomplete)
    
    def test_ValueError(self):
        """
        Checks that sub-class ValueError is raised with wrong value argument.

        Test ID: TEST-T-501
        Requirement(s): REQ-AWM-501

        Version 1.0.0.0
        """
        for _ in range(1000):
            z = random.random()
            if z <= 0.0:
                z = 0.000000001
            x = random.random() + random.randint(1, 10)
            y = random.random() + random.randint(1, 10)
            TestValue = self.TestFunction(z, x, y)
            Check = math.log(test_module.beta_incomplete(z, x, y))
            self.assertIsInstance(TestValue, float)
            self.assertAlmostEqual(TestValue, Check)
        super().test_ValueError()
        #special case - z is 0
        for _ in range(100):
            with self.assertRaises(ValueError):
                self.TestFunction(0, random.random() + random.randint(1, 10),
                                        random.random() + random.randint(1, 10))
    
    def test_OK(self):
        """
        Checks that the values are calculated properly, using the previously
        tested functions.

        Test ID: TEST-T-550
        Requirement(s): REQ-FUN-550.

        Version 1.0.0.0
        """
        #special cases
        for y in RIBFZ_X_Y:
            for x in RIBFZ_X_Y:
                TestValue = self.TestFunction(1, x, y)
                Check = test_module.log_beta(x, y)
                self.assertIsInstance(TestValue, float)
                self.assertAlmostEqual(TestValue, Check)

class Test_lower_gamma_reg(unittest.TestCase):
    """
    Checks the implementation of the function
    special_functions.lower_gamma_reg().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-560.
    Covers requirements: REQ-FUN-560, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.lower_gamma_reg)
    
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
                self.TestFunction(0.5, Value)
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
            ValueInt = - random.randint(1, 10)
            ValueFloat = - (random.random() + 0.0000001)
            ValueMix = ValueInt + ValueFloat
            for Value in (ValueInt, ValueFloat, ValueMix): #negative values
                with self.assertRaises(ValueError):
                    self.TestFunction(Value, 1)
                with self.assertRaises(ValueError):
                    self.TestFunction(0.5, Value)
                with self.assertRaises(ValueError):
                    self.TestFunction(Value, Value)
            #special cases
            #+ zero x
            with self.assertRaises(ValueError):
                self.TestFunction(0, - ValueFloat)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly. The check values are
        calculated using online calculators:
        
        https://keisan.casio.com/exec/system/1180573447
        https://keisan.casio.com/exec/system/1180573444
        
        Test ID: TEST-T-560
        Requirement(s): REQ-FUN-560.

        Version 1.0.0.0
        """
        for IndX, x in enumerate(RLIGF_X):
            for IndY, y in enumerate(RLIGF_Y):
                Check = RLIGF[IndX][IndY]
                TestValue = self.TestFunction(x, y)
                strError = 'for gamma({}, {})'.format(x, y)
                self.assertIsInstance(TestValue, float)
                self.assertAlmostEqual(TestValue, Check,
                                                places = FLOAT_CHECK_PRECISION,
                                                                msg = strError)
        #edge cases
        for _ in range(100):
            TestValue = self.TestFunction(random.randint(1, 10), 0)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, 0.0)
            TestValue = self.TestFunction(
                                random.randint(1, 10) + random.random(), 0.0)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, 0.0)

class Test_lower_gamma(Test_lower_gamma_reg):
    """
    Checks the implementation of the function
    special_functions.lower_gamma().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-560.
    Covers requirements: REQ-FUN-560, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.lower_gamma)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly using comparison with
        the already tested functions.
        
        Test ID: TEST-T-560
        Requirement(s): REQ-FUN-560.

        Version 1.0.0.0
        """
        for _ in range(1000):
            x = random.random() + random.randint(0, 10) + 0.000001
            y = random.random() + random.randint(0, 15)
            TestValue = self.TestFunction(x, y)
            Check = test_module.lower_gamma_reg(x, y) * math.gamma(x)
            self.assertIsInstance(TestValue, float)
            self.assertAlmostEqual(TestValue, Check)
        #edge cases
        for _ in range(100):
            TestValue = self.TestFunction(random.randint(1, 10), 0)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, 0.0)
            TestValue = self.TestFunction(
                                random.randint(1, 10) + random.random(), 0.0)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, 0.0)

class Test_log_lower_gamma(Test_lower_gamma_reg):
    """
    Checks the implementation of the function
    special_functions.log_lower_gamma().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-560.
    Covers requirements: REQ-FUN-560, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.log_lower_gamma)
    
    def test_ValueError(self):
        """
        Checks that sub-class ValueError is raised with wrong value argument.

        Test ID: TEST-T-501
        Requirement(s): REQ-AWM-501

        Version 1.0.0.0
        """
        super().test_ValueError()
        #special cases of y = 0
        for _ in range(100):
            with self.assertRaises(ValueError):
                self.TestFunction(random.randint(1, 10), 0)
            with self.assertRaises(ValueError):
                self.TestFunction(random.randint(1, 10) + random.random(), 0)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly using comparison with
        the already tested functions.
        
        Test ID: TEST-T-560
        Requirement(s): REQ-FUN-560.

        Version 1.0.0.0
        """
        for _ in range(1000):
            x = random.random() + random.randint(0, 10) + 0.000001
            y = random.random() + random.randint(0, 15) + 0.000001
            TestValue = self.TestFunction(x, y)
            Check = test_module.lower_gamma_reg(x, y) * math.gamma(x)
            self.assertIsInstance(TestValue, float)
            self.assertAlmostEqual(TestValue, math.log(Check))

class Test_upper_gamma_reg(Test_lower_gamma_reg):
    """
    Checks the implementation of the function
    special_functions.upper_gamma_reg().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-560.
    Covers requirements: REQ-FUN-560, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.upper_gamma_reg)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly using comparison with
        the already tested functions.
        
        Test ID: TEST-T-560
        Requirement(s): REQ-FUN-560.

        Version 1.0.0.0
        """
        for _ in range(1000):
            x = random.random() + random.randint(0, 10) + 0.000001
            y = random.random() + random.randint(0, 15)
            TestValue = self.TestFunction(x, y)
            Check = 1 - test_module.lower_gamma_reg(x, y)
            self.assertIsInstance(TestValue, float)
            self.assertAlmostEqual(TestValue, Check)
        #edge cases
        for _ in range(100):
            TestValue = self.TestFunction(random.randint(1, 10), 0)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, 1.0)
            TestValue = self.TestFunction(
                                random.randint(1, 10) + random.random(), 0.0)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, 1.0)

class Test_upper_gamma(Test_lower_gamma_reg):
    """
    Checks the implementation of the function
    special_functions.upper_gamma().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-560.
    Covers requirements: REQ-FUN-560, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.upper_gamma)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly using comparison with
        the already tested functions.
        
        Test ID: TEST-T-560
        Requirement(s): REQ-FUN-560.

        Version 1.0.0.0
        """
        for _ in range(1000):
            x = random.random() + random.randint(0, 10) + 0.000001
            y = random.random() + random.randint(0, 15)
            TestValue = self.TestFunction(x, y)
            Check = test_module.upper_gamma_reg(x, y) * math.gamma(x)
            self.assertIsInstance(TestValue, float)
            self.assertAlmostEqual(TestValue, Check)
        #edge cases
        for _ in range(100):
            Value = random.randint(1, 10)
            TestValue = self.TestFunction(Value, 0)
            Check = math.gamma(Value)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, Check)
            Value = random.randint(1, 10) + random.random()
            TestValue = self.TestFunction(Value, 0.0)
            Check = math.gamma(Value)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, Check)

class Test_log_upper_gamma(Test_lower_gamma_reg):
    """
    Checks the implementation of the function
    special_functions.log_upper_gamma().

    Implements tests: TEST-T-500, TEST-T-501 and TEST-T-560.
    Covers requirements: REQ-FUN-560, REQ-AWM-500 and REQ-AWM-501.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(test_module.log_upper_gamma)
    
    def test_OK(self):
        """
        Checks that the values are calculated properly using comparison with
        the already tested functions.
        
        Test ID: TEST-T-560
        Requirement(s): REQ-FUN-560.

        Version 1.0.0.0
        """
        for _ in range(1000):
            x = random.random() + random.randint(0, 10) + 0.000001
            y = random.random() + random.randint(0, 15)
            TestValue = self.TestFunction(x, y)
            Check = test_module.upper_gamma_reg(x, y) * math.gamma(x)
            self.assertIsInstance(TestValue, float)
            self.assertAlmostEqual(TestValue, math.log(Check))
        #edge cases
        for _ in range(100):
            Value = random.randint(1, 10)
            TestValue = self.TestFunction(Value, 0)
            Check = math.lgamma(Value)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, Check)
            Value = random.randint(1, 10) + random.random()
            TestValue = self.TestFunction(Value, 0.0)
            Check = math.lgamma(Value)
            self.assertIsInstance(TestValue, float)
            self.assertEqual(TestValue, Check)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_factorial)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_gamma)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_erf)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_permutation)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_combination)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_beta)
TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_log_beta)
TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(Test_inv_erf)
TestSuite9 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_beta_incomplete_reg)
TestSuite10 = unittest.TestLoader().loadTestsFromTestCase(Test_beta_incomplete)
TestSuite11 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_log_beta_incomplete)
TestSuite12 = unittest.TestLoader().loadTestsFromTestCase(Test_lower_gamma_reg)
TestSuite13 = unittest.TestLoader().loadTestsFromTestCase(Test_upper_gamma_reg)
TestSuite14 = unittest.TestLoader().loadTestsFromTestCase(Test_lower_gamma)
TestSuite15 = unittest.TestLoader().loadTestsFromTestCase(Test_upper_gamma)
TestSuite16 = unittest.TestLoader().loadTestsFromTestCase(Test_log_lower_gamma)
TestSuite17 = unittest.TestLoader().loadTestsFromTestCase(Test_log_upper_gamma)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                        TestSuite6, TestSuite7, TestSuite8, TestSuite9,
                        TestSuite10, TestSuite11, TestSuite12, TestSuite13,
                        TestSuite14, TestSuite15, TestSuite16, TestSuite17])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.special_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
