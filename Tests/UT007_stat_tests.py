#usr/bin/python3
"""
Module statistics_lib.Tests.UT007_stat_tests

Set of unit tests on the module stastics_lib.stat_tests. See the test
plan / report TE007_stat_tests.md
"""


__version__= '1.0.0.0'
__date__ = '09-05-2022'
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

import statistics_lib.distribution_classes as dc

from statistics_lib.data_classes import Statistics1D

class Test_TestResult(unittest.TestCase):
    """
    Unittests for TestResult class from the module statistics_lib.stat_tests.

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = test_module.TestResult
    
    def test_TestName_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        """
        for gItem in [1, -2.0, [1,2], (2.0, 1), int, str, float, bool, {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass(gItem, 'test', 'test', 2.1, 0.95, (None, 2.0))
    
    def test_DataName_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        """
        for gItem in [1, -2.0, [1,2], (2.0, 1), int, str, float, bool, {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass('test', gItem, 'test', 2.1, 0.95, (None, 2.0))
    
    def test_ModelName_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        """
        for gItem in [1, -2.0, [1,2], (2.0, 1), int, str, float, bool, {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass('test', 'test', gItem, 2.1, 0.95, (None, 2.0))
    
    def test_TestValue_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        """
        for gItem in ['-2.0', [1,2], (2.0, 1), int, str, float, bool, {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass('test', 'test', 'test', gItem, 0.95, (None, 2.0))
    
    def test_CDF_Value_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        """
        for gItem in [1, '-2.0', [1, 2], (2.0, 1), int, str, float, bool,
                                                                    {'a':1}]:
            with self.assertRaises(TypeError):
                self.TestClass('test', 'test', 'test', 2.1, gItem, (None, 2.0))
    
    def test_CritValues_TypeError(self):
        """
        Additional test - checks the sanity checks on the input values.
        """
        for gItem in [1, '-2.0', [1, 2], (2.0, 1, 3), int, str, float, bool,
                                    {'a':1}, (2.0, ), (None, None), ('1', 1)]:
            with self.assertRaises(TypeError):
                self.TestClass('test', 'test', 'test', 2.1, 0.95, gItem)
    
    def test_CDF_Value_ValueError(self):
        """
        Additional test - checks the sanity checks on the input values.
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
        """
        for _ in range(100):
            Value1 = random.randint(-5, 5)
            if random.random() > 0.5:
                Value1 += random.random()
            Value2 = Value1 - 0.1 - random.random() - random.randint(0, 10)
            gItem = (Value1, Value2)
            with self.assertRaises(ValueError):
                self.TestClass('test', 'test', 'test', 2.1, 0.95, gItem)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_TestResult)

TestSuite = unittest.TestSuite()

TestSuite.addTests([TestSuite1, ])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting statistics_lib.stat_tests module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)