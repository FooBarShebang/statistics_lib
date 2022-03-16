"""
Module statistics_lib.Tests.UT005_special_functions

Set of unit tests on the module stastics_lib.special_functions. See the test
plan / report TE005_special_functions.md
"""


__version__= '1.0.0.0'
__date__ = '16-03-2022'
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

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_factorial)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_gamma)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_erf)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.special_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
