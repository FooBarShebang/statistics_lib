#usr/bin/python3
"""
Module statistics_lib.Tests.UT003_data_classes

Set of unit tests on the module stastics_lib.data_classes. See the test plan /
report TE003_data_classes.md
"""


__version__= '1.0.0.0'
__date__ = '28-02-2022'
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
        cls.TotalErr = list()
        for Item in cls.MixedErr:
            Temp = random.random()
            if Temp >= 0.6:
                cls.TotalMixed.append(Item)
                cls.TotalErr.append(0)
            else:
                cls.TotalMixed.append(Item.Value)
                cls.TotalErr.append(Item.SE)
        cls.BadCases = [1, 2.0, 'asd', [1, '1'], ('b', 2.0), int, float, list,
                        tuple, {1:1, 2:2}, dict]
    
    def test_InitTypeError(self):
        """
        Checks that sub-class of TypeError exception is raised with improper
        argument of the initialization method.
        
        Tests ID: TEST-T-310
        Requirements ID: REQ-AWM-300
        """
        for Item in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestClass(Item)
    
    def test_InitValueError(self):
        """
        Checks that sub-class of ValueError exception is raised if the class is
        instantiated with an empty sequence
        
        Tests ID: TEST-T-311
        Requirements ID: REQ-AWM-301
        """
        with self.assertRaises(ValueError):
                self.TestClass([])
        with self.assertRaises(ValueError):
                self.TestClass(tuple())

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
        Length = random.randrange(5, 100)
        cls.AllIntX = [random.randint(-100, 100) for _ in range(Length)]
        cls.AllIntY = [random.randint(-100, 100) for _ in range(Length)]
        Length = random.randrange(5, 100)
        cls.AllFloatX = [random.uniform(-10.0, 10.0) for _ in range(Length)]
        cls.AllFloatY = [random.uniform(-10.0, 10.0) for _ in range(Length)]
        cls.MixedX = list()
        cls.MixedY = list()
        for _ in range(random.randrange(10, 100)):
            Temp = random.random()
            if Temp >= 0.5:
                cls.MixedX.append(random.uniform(-10.0, 10.0))
            else:
                cls.MixedX.append(random.randint(-100, 100))
            Temp = random.random()
            if Temp >= 0.5:
                cls.MixedY.append(random.uniform(-10.0, 10.0))
            else:
                cls.MixedY.append(random.randint(-100, 100))
        MaxLength = max(len(cls.AllIntX), len(cls.AllFloatX), len(cls.MixedX))
        cls.ErrorsX = [random.uniform(0.0, 3.0) for _ in range(MaxLength)]
        cls.ErrorsY = [random.uniform(0.0, 3.0) for _ in range(MaxLength)]
        cls.IntErrX = [MeasuredValue(Value, cls.ErrorsX[i])
                                        for i, Value in enumerate(cls.AllIntX)]
        cls.FloatErrX = [MeasuredValue(Value, cls.ErrorsX[i])
                                    for i, Value in enumerate(cls.AllFloatX)]
        cls.MixedErrX = [MeasuredValue(Value, cls.ErrorsX[i])
                                        for i, Value in enumerate(cls.MixedX)]
        cls.IntErrY = [MeasuredValue(Value, cls.ErrorsX[i])
                                        for i, Value in enumerate(cls.AllIntX)]
        cls.FloatErrY = [MeasuredValue(Value, cls.ErrorsX[i])
                                    for i, Value in enumerate(cls.AllFloatX)]
        cls.MixedErrY = [MeasuredValue(Value, cls.ErrorsX[i])
                                        for i, Value in enumerate(cls.MixedX)]
        cls.TotalMixedX = list()
        cls.TotalMixedY = list()
        cls.TotalErrX = list()
        cls.TotalErrY = list()
        for Index, Item in enumerate(cls.MixedErrX):
            Temp = random.random()
            if Temp >= 0.6:
                cls.TotalMixedX.append(Item)
                cls.TotalErrX.append(0)
            else:
                cls.TotalMixedX.append(Item.Value)
                cls.TotalErrX.append(Item.SE)
            Temp = random.random()
            if Temp >= 0.6:
                cls.TotalMixedY.append(cls.MixedErrY[Index])
                cls.TotalErrY.append(0)
            else:
                cls.TotalMixedY.append(cls.MixedErrY[Index].Value)
                cls.TotalErrY.append(cls.MixedErrY[Index].SE)
        cls.BadCases = [1, 2.0, 'asd', [1, '1'], ('b', 2.0), int, float, list,
                        tuple, {1:1, 2:2}, dict]
        
    def test_InitTypeError(self):
        """
        Checks that sub-class of TypeError exception is raised with improper
        argument of the initialization method.
        
        Tests ID: TEST-T-320
        Requirements ID: REQ-AWM-300
        """
        for Item in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestClass(Item, [1, 1, 1])
            with self.assertRaises(TypeError):
                self.TestClass([1, 1, 1], Item)
            with self.assertRaises(TypeError):
                self.TestClass(Item, Item)
    
    def test_InitValueError(self):
        """
        Checks that sub-class of ValueError exception is raised if the class is
        instantiated with two sequences of unequal length, including one being
        empty, or both sequences being empty
        
        Tests ID: TEST-T-311
        Requirements ID: REQ-AWM-301
        """
        with self.assertRaises(ValueError):
                self.TestClass([], tuple())
        with self.assertRaises(ValueError):
                self.TestClass(tuple(), [1, 2, 3])
        with self.assertRaises(ValueError):
                self.TestClass([1, 2, 3], list())
        with self.assertRaises(ValueError):
                self.TestClass([1, 2, 3], (1, 2))
        with self.assertRaises(ValueError):
                self.TestClass((1, 2, 3), [1, 2, 3, 4, 5])

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