#usr/bin/python3
"""
Module statistics_lib.Tests.UT003_data_classes

Set of unit tests on the module stastics_lib.data_classes. See the test plan /
report TE003_data_classes.md
"""


__version__= '1.0.0.0'
__date__ = '25-02-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import unittest
import random

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.data_classes as test_module

from phyqus_lib.base_classes import MeasuredValue

#globals

FLOAT_CHECK_PRECISION = 8 #digits after comma

#classes

#+ test cases

class Test_Statistics1D(unittest.TestCase):
    """
    Unit-test class implementing testing of the class Statistics1D() from the
    module statistics_lib.data_classes.

    Implements tests: 
    Covers the requirements:
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = test_module.Statistics1D
        cls.AllInt = [random.randint(-100, 100)
                                    for _ in range(random.randrange(5, 100))]
        cls.AllFloat = [random.uniform(-10.0, 10.0)
                                    for _ in range(random.randrange(5, 100))]
        cls.Mixed = list()
        for _ in range(random.randrange(10, 100)):
            Temp = random.random()
            if Temp >= 0.5:
                cls.Mixed.append(random.uniform(-10.0, 10.0))
            else:
                cls.Mixed.append(random.randint(-100, 100))
        MaxLength = max(len(cls.AllInt), len(cls.AllFloat), len(cls.Mixed))
        cls.Errors = [random.uniform(0.0, 3.0) for _ in range(MaxLength)]
        cls.IntErr = [MeasuredValue(Value, cls.Errors[i])
                                        for i, Value in enumerate(cls.AllInt)]
        cls.FloatErr = [MeasuredValue(Value, cls.Errors[i])
                                        for i, Value in enumerate(cls.AllFloat)]
        cls.MixedErr = [MeasuredValue(Value, cls.Errors[i])
                                        for i, Value in enumerate(cls.Mixed)]
        cls.TotalMixed = list()
        for Item in cls.MixedErr:
            Temp = random.random()
            if Temp >= 0.6:
                cls.TotalMixed.append(Item)
            else:
                cls.TotalMixed.append(Item.Value)
        cls.BadCases = [1, 2.0, 'asd', [1, '1'], ('b', 2.0), int, float, list,
                        tuple, {1:1, 2:2}, dict]

class Test_Statistics2D(unittest.TestCase):
    """
    Unit-test class implementing testing of the class Statistics2D() from the
    module statistics_lib.data_classes.

    Implements tests: 
    Covers the requirements:
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = test_module.Statistics2D

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_Statistics1D)

TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_Statistics2D)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.data_classes module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)