#usr/bin/python3
"""
Module statistics_lib.Tests.UT006_inverse_distributions

Set of unit tests on the module stastics_lib.inverse_distributions. See the test
plan / report TE006_inverse_distributions.md
"""


__version__= '1.0.0.0'
__date__ = '22-04-2022'
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
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = test_module.InverseGaussian
        cls.Properties = ('Mean', 'Median', 'Q1', 'Q3', 'Min', 'Max', 'Var',
                            'Sigma', 'Skew', 'Kurt')
        cls.Parameters = tuple('Mean', 'Shape')
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

class Test_InverseGamma(Test_InverseGaussian):
    """
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.InverseGamma
        cls.Parameters = tuple('Shape', 'Scale')
    
    def setUp(self) -> None:
        """
        Preparation of a single unottest - performed before each of them.
        """
        Scale = random.randint(1, 10)
        if random.random() > 0.5:
            Scale -= random.random()
        if Scale < 0.1:
            Scale = 0.1
        Shape = random.randint(1, 5)
        if random.random() > 0.5:
            Shape -= random.random()
        if Shape < 0.1:
            Shape = 0.1
        self.DefArguments = (Shape, Scale)

class Test_InverseChiSquared(Test_InverseGaussian):
    """
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.InverseChiSquared
        cls.Parameters = tuple('Degree', )
    
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

class Test_ScaledInverseChiSquared(Test_InverseChiSquared):
    """
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.ScaledInverseChiSquared
        cls.Parameters = tuple('Degree', 'Scale')
    
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

class Test_Cauchy(Test_InverseGaussian):
    """
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Cauchy
        cls.Parameters = tuple('Location', 'Scale')
    
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

class Test_Levy(Test_Cauchy):
    """
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestClass = test_module.Levy

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_InverseGaussian)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_InverseGamma)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_InverseChiSquared)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(
                                                Test_ScaledInverseChiSquared)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_Cauchy)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_Levy)

TestSuite = unittest.TestSuite()
#TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
#                        TestSuite6])
TestSuite.addTests([TestSuite1])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting statistics_lib.inverse_distributions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
