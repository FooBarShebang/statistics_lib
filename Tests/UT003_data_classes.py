#usr/bin/python3
"""
Module statistics_lib.Tests.UT003_data_classes

Set of unit tests on the module stastics_lib.data_classes. See the test plan /
report TE003_data_classes.md
"""


__version__= '1.0.0.0'
__date__ = '07-03-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import unittest
import random
import math

import collections.abc as c_abc

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.data_classes as test_module

import statistics_lib.base_functions as bf

import statistics_lib.ordered_functions as of

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

    Version 1.0.0.0
    """
    
    @classmethod
    def setUpClass(cls) -> None:
        """
        Preparation for the test cases, done only once.

        Version 1.0.0.0
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
                cls.TotalErr.append(Item.SE)
            else:
                cls.TotalMixed.append(Item.Value)
                cls.TotalErr.append(0)
        cls.BadCases = [1, 2.0, 'asd', [1, '1'], ('b', 2.0), int, float, list,
                        tuple, {1:1, 2:2}, dict]
        cls.Properties = (('N', int), ('Mean', (int, float)),
                                ('Min', (int, float)), ('Max', (int, float)),
                                ('Median', (int, float)), ('Q1', (int, float)),
                                ('Q3', (int, float)), ('Var', (int, float)),
                                ('Sigma', (int, float)), ('SE', (int, float)),
                                ('FullVar', (int, float)),
                                ('FullSigma', (int, float)),
                                ('FullSE', (int, float)),
                                ('Skew', (int, float)), ('Kurt', (int, float)),
                                ('Summary', str), ('Sorted', c_abc.Sequence),
                                ('Values', c_abc.Sequence),
                                ('Errors', c_abc.Sequence))
    
    def test_InitTypeError(self):
        """
        Checks that sub-class of TypeError exception is raised with improper
        argument of the initialization method.
        
        Tests ID: TEST-T-310
        Requirements ID: REQ-AWM-300

        Version 1.0.0.0
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

        Version 1.0.0.0
        """
        with self.assertRaises(ValueError):
                self.TestClass([])
        with self.assertRaises(ValueError):
                self.TestClass(tuple())
    
    def test_HasAttributes(self):
        """
        Checks that the class has all required attributes (properties and
        methods), and the (read) properties are of the expected type.

        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312, REQ-FUN-313

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            for Attr, DataType in self.Properties:
                self.assertTrue(hasattr(objTest, Attr))
                self.assertIsInstance(getattr(objTest, Attr), DataType)
            self.assertTrue(hasattr(objTest, 'getQuantile'))
            self.assertTrue(hasattr(objTest, 'getHistogram'))
            self.assertTrue(hasattr(objTest, 'Name'))
            del objTest
    
    def test_AttributeError(self):
        """
        Checks that it is not possible to delete properties or methods, or to
        assign to read-only properties

        Tests ID: TEST-T-312
        Requirements ID: REQ-AWM-302

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            for Attr, _ in self.Properties:
                with self.assertRaises(AttributeError):
                    setattr(objTest, Attr, 1)
                with self.assertRaises(AttributeError):
                    delattr(objTest, Attr)
            with self.assertRaises(AttributeError):
                del objTest.getQuantile
            with self.assertRaises(AttributeError):
                del objTest.getHistogram
            with self.assertRaises(AttributeError):
                del objTest.Name
            with self.assertRaises(AttributeError):
                delattr(objTest, 'getQuantile')
            with self.assertRaises(AttributeError):
                delattr(objTest, 'getHistogram')
            with self.assertRaises(AttributeError):
                delattr(objTest, 'Name')
    
    def test_DataAccess(self):
        """
        Checks that it the input data is properly converted into two sequences
        of real numbers (means and errors).

        Tests ID: TEST-T-316
        Requirements ID: REQ-FUN-310, REQ-FUN-311

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed]:
            Length = len(Input)
            Errors = [0 for _ in range(Length)]
            objTest = self.TestClass(Input)
            self.assertSequenceEqual(objTest.Values, Input)
            self.assertSequenceEqual(objTest.Errors, Errors)
            del objTest
        for Input, Check in [(self.IntErr, self.AllInt),
                                (self.FloatErr, self.AllFloat),
                                (self.MixedErr, self.Mixed)]:
            Length = len(Input)
            Errors = self.Errors[:Length]
            objTest = self.TestClass(Input)
            self.assertSequenceEqual(objTest.Values, Check)
            self.assertSequenceEqual(objTest.Errors, Errors)
            del objTest
        objTest = self.TestClass(self.TotalMixed)
        self.assertSequenceEqual(objTest.Values, self.Mixed)
        self.assertSequenceEqual(objTest.Errors, self.TotalErr)
        del objTest
    
    def test_ImmutableData(self):
        """
        Checks that the stored data cannot be modified or deleted per element.
        
        Tests ID: TEST-T-313
        Requirements ID: REQ-AWM-310

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Length = len(objTest.Values)
            for Index in range(Length):
                with self.assertRaises(TypeError):
                    del objTest.Values[Index]
                with self.assertRaises(AttributeError): #immutable type sequence
                    objTest.Values.pop(Index)
                with self.assertRaises(TypeError):
                    objTest.Values[Index] = 1
                with self.assertRaises(TypeError):
                    del objTest.Errors[Index]
                with self.assertRaises(AttributeError): #immutable type sequence
                    objTest.Errors.pop(Index)
                with self.assertRaises(TypeError):
                    objTest.Errors[Index] = 1
            with self.assertRaises(AttributeError):
                objTest.Values.append(1)
            with self.assertRaises(AttributeError):
                objTest.Values.extend([1, 1])
            with self.assertRaises(AttributeError):
                objTest.Errors.append(1)
            with self.assertRaises(AttributeError):
                objTest.Errors.extend([1, 1])
            del objTest
    
    def test_Name(self):
        """
        Checks that the assignment and reading-out of the name of the data set.
        
        Tests ID: TEST-T-318
        Requirements ID: REQ-FUN-314

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            self.assertIsNone(objTest.Name)
            for Name in ['test', 1, 2.0, True, None]:
                objTest.Name = Name
                self.assertIsInstance(objTest.Name, str)
                self.assertEqual(objTest.Name, str(Name))
                self.assertIsInstance(objTest.Name, str)
                self.assertEqual(objTest.Name, str(Name))
            del objTest
    
    def test_N(self):
        """
        Checks that the length of the stored data set is returned properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            self.assertIsInstance(objTest.N, int)
            self.assertEqual(objTest.N, len(Input))
            #check the repetitive call!
            self.assertIsInstance(objTest.N, int)
            self.assertEqual(objTest.N, len(Input))
            del objTest
    
    def test_Mean(self):
        """
        Checks that the mean of the stored data set is returned properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = bf.GetMean(Input)
            TestResult = objTest.Mean
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Var(self):
        """
        Checks that the variance of the stored data set is returned properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = bf.GetVarianceP(Input)
            TestResult = objTest.Var
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_FullVar(self):
        """
        Checks that the full variance of the stored data set is returned
        properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = bf.GetVarianceP(Input) + bf.GetMeanSqrSE(
                                                    bf._ExtractErrors(Input))
            TestResult = objTest.FullVar
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Sigma(self):
        """
        Checks that the standard deviation of the stored data set is returned
        properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = bf.GetStdevP(Input)
            TestResult = objTest.Sigma
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_FullSigma(self):
        """
        Checks that the full standard deviation of the stored data set is
        returned properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = math.sqrt(bf.GetVarianceP(Input) + bf.GetMeanSqrSE(
                                                    bf._ExtractErrors(Input)))
            TestResult = objTest.FullSigma
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_SE(self):
        """
        Checks that the standard error of the mean of the stored data set is
        returned properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = bf.GetSE(Input)
            TestResult = objTest.SE
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_FullSE(self):
        """
        Checks that the full standard error of the mean of the stored data set
        is returned properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = math.sqrt(objTest.FullVar / objTest.N)
            #note - some rounding-up errors when compared with bs.GetFullSE()
            TestResult = objTest.FullSE
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Skew(self):
        """
        Checks that the skewness of the stored data set is returned properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = bf.GetSkewnessP(Input)
            TestResult = objTest.Skew
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Kurt(self):
        """
        Checks that the excess kurtosis of the stored data set is returned
        properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = bf.GetKurtosisP(Input)
            TestResult = objTest.Kurt
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Min(self):
        """
        Checks that the minimum value of the stored data set is returned
        properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-313

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = of.GetMin(Input)
            TestResult = objTest.Min
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Max(self):
        """
        Checks that the maximum value of the stored data set is returned
        properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-313

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = of.GetMax(Input)
            TestResult = objTest.Max
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Median(self):
        """
        Checks that the median value of the stored data set is returned
        properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-313

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = of.GetMedian(Input)
            TestResult = objTest.Median
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Q1(self):
        """
        Checks that the first quartile of the stored data set is returned
        properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-313

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = of.GetFirstQuartile(Input)
            TestResult = objTest.Q1
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest
    
    def test_Q3(self):
        """
        Checks that the third quartile of the stored data set is returned
        properly.
        
        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-313

        Version 1.0.0.0
        """
        for Input in [self.AllInt, self.AllFloat, self.Mixed, self.IntErr,
                                self.FloatErr, self.MixedErr, self.TotalMixed]:
            objTest = self.TestClass(Input)
            Check = of.GetThirdQuartile(Input)
            TestResult = objTest.Q3
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            #check the repetitive call!
            self.assertIsInstance(TestResult, (int, float))
            self.assertAlmostEqual(TestResult, Check,
                                                places = FLOAT_CHECK_PRECISION)
            del objTest

class Test_Statistics2D(unittest.TestCase):
    """
    Unit-test class implementing testing of the class Statistics2D() from the
    module statistics_lib.data_classes.

    Implements tests: 
    Covers the requirements:

    Version 1.0.0.0
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
        cls.IntErrY = [MeasuredValue(Value, cls.ErrorsY[i])
                                        for i, Value in enumerate(cls.AllIntY)]
        cls.FloatErrY = [MeasuredValue(Value, cls.ErrorsY[i])
                                    for i, Value in enumerate(cls.AllFloatY)]
        cls.MixedErrY = [MeasuredValue(Value, cls.ErrorsY[i])
                                        for i, Value in enumerate(cls.MixedY)]
        cls.TotalMixedX = list()
        cls.TotalMixedY = list()
        cls.TotalErrX = list()
        cls.TotalErrY = list()
        for Index, Item in enumerate(cls.MixedErrX):
            Temp = random.random()
            if Temp >= 0.6:
                cls.TotalMixedX.append(Item)
                cls.TotalErrX.append(Item.SE)
            else:
                cls.TotalMixedX.append(Item.Value)
                cls.TotalErrX.append(0)
            Temp = random.random()
            if Temp >= 0.6:
                cls.TotalMixedY.append(cls.MixedErrY[Index])
                cls.TotalErrY.append(cls.MixedErrY[Index].SE)
            else:
                cls.TotalMixedY.append(cls.MixedErrY[Index].Value)
                cls.TotalErrY.append(0)
        cls.BadCases = [1, 2.0, 'asd', [1, '1'], ('b', 2.0), int, float, list,
                        tuple, {1:1, 2:2}, dict]
        cls.Properties = (('N', int), ('Cov', (int, float)),
                                ('Pearson', (int, float)),
                                ('Spearman', (int, float)),
                                ('Kendall', (int, float)),
                                ('Summary', str),
                                ('X', test_module.Statistics1D),
                                ('Y', test_module.Statistics1D))
        
    def test_InitTypeError(self):
        """
        Checks that sub-class of TypeError exception is raised with improper
        argument of the initialization method.
        
        Tests ID: TEST-T-320
        Requirements ID: REQ-AWM-300

        Version 1.0.0.0
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

        Version 1.0.0.0
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
    
    def test_HasAttributes(self):
        """
        Checks that the class has all required attributes (properties and
        methods), and the (read) properties are of the expected type.

        Tests ID: TEST-T-317
        Requirements ID: REQ-FUN-312, REQ-FUN-313

        Version 1.0.0.0
        """
        for DataX, DataY in [(self.AllIntX, self.AllIntY),
                                (self.AllFloatX, self.AllFloatY),
                                (self.MixedX, self.MixedY),
                                (self.IntErrX, self.IntErrY),
                                (self.FloatErrX, self.FloatErrY),
                                (self.MixedErrX, self.MixedErrY),
                                (self.TotalMixedX, self.TotalMixedY)]:
            objTest = self.TestClass(DataX, DataY)
            for Attr, DataType in self.Properties:
                self.assertTrue(hasattr(objTest, Attr))
                self.assertIsInstance(getattr(objTest, Attr), DataType)
            self.assertTrue(hasattr(objTest, 'Name'))
            del objTest
    
    def test_AttributeError(self):
        """
        Checks that it is not possible to delete properties or methods, or to
        assign to read-only properties

        Tests ID: TEST-T-322
        Requirements ID: REQ-AWM-302

        Version 1.0.0.0
        """
        for DataX, DataY in [(self.AllIntX, self.AllIntY),
                                (self.AllFloatX, self.AllFloatY),
                                (self.MixedX, self.MixedY),
                                (self.IntErrX, self.IntErrY),
                                (self.FloatErrX, self.FloatErrY),
                                (self.MixedErrX, self.MixedErrY),
                                (self.TotalMixedX, self.TotalMixedY)]:
            objTest = self.TestClass(DataX, DataY)
            for Attr, _ in self.Properties:
                with self.assertRaises(AttributeError):
                    setattr(objTest, Attr, 1)
                with self.assertRaises(AttributeError):
                    delattr(objTest, Attr)
            with self.assertRaises(AttributeError):
                del objTest.Name
            with self.assertRaises(AttributeError):
                delattr(objTest, 'Name')
    
    def test_DataAccess(self):
        """
        Checks that it the input data is properly converted into two instances
        of Statistics1D classes, which contain the proper 'means' and 'errors'
        sequences.

        Tests ID: TEST-T-323
        Requirements ID: REQ-FUN-320, REQ-FUN-321

        Version 1.0.0.0
        """
        for DataX, DataY in [(self.AllIntX, self.AllIntY),
                                (self.AllFloatX, self.AllFloatY),
                                (self.MixedX, self.MixedY)]:
            Length = len(DataX)
            Errors = [0 for _ in range(Length)]
            objTest = self.TestClass(DataX, DataY)
            self.assertIsInstance(objTest.X, test_module.Statistics1D)
            self.assertIsInstance(objTest.Y, test_module.Statistics1D)
            self.assertSequenceEqual(objTest.X.Values, DataX)
            self.assertSequenceEqual(objTest.X.Errors, Errors)
            self.assertSequenceEqual(objTest.Y.Values, DataY)
            self.assertSequenceEqual(objTest.Y.Errors, Errors)
            del objTest
        for DataX, DataY, CheckX, CheckY in [
                (self.IntErrX, self.IntErrY, self.AllIntX, self.AllIntY),
                (self.FloatErrX, self.FloatErrY, self.AllFloatX,self.AllFloatY),
                (self.MixedErrX, self.MixedErrY, self.MixedX, self.MixedY)]:
            Length = len(DataX)
            ErrorsX = self.ErrorsX[:Length]
            ErrorsY = self.ErrorsY[:Length]
            objTest = self.TestClass(DataX, DataY)
            self.assertIsInstance(objTest.X, test_module.Statistics1D)
            self.assertIsInstance(objTest.Y, test_module.Statistics1D)
            self.assertSequenceEqual(objTest.X.Values, CheckX)
            self.assertSequenceEqual(objTest.X.Errors, ErrorsX)
            self.assertSequenceEqual(objTest.Y.Values, CheckY)
            self.assertSequenceEqual(objTest.Y.Errors, ErrorsY)
            del objTest
        objTest = self.TestClass(self.TotalMixedX, self.TotalMixedY)
        self.assertIsInstance(objTest.X, test_module.Statistics1D)
        self.assertIsInstance(objTest.Y, test_module.Statistics1D)
        self.assertSequenceEqual(objTest.X.Values, self.MixedX)
        self.assertSequenceEqual(objTest.X.Errors, self.TotalErrX)
        self.assertSequenceEqual(objTest.Y.Values, self.MixedY)
        self.assertSequenceEqual(objTest.Y.Errors, self.TotalErrY)
        del objTest
    
    def test_Name(self):
        """
        Checks that the assignment and reading-out of the name of the data set.
        
        Tests ID: TEST-T-325
        Requirements ID: REQ-FUN-323

        Version 1.0.0.0
        """
        for DataX, DataY in [(self.AllIntX, self.AllIntY),
                                (self.AllFloatX, self.AllFloatY),
                                (self.MixedX, self.MixedY),
                                (self.IntErrX, self.IntErrY),
                                (self.FloatErrX, self.FloatErrY),
                                (self.MixedErrX, self.MixedErrY),
                                (self.TotalMixedX, self.TotalMixedY)]:
            objTest = self.TestClass(DataX, DataY)
            self.assertIsNone(objTest.Name)
            for Name in ['test', 1, 2.0, True, None]:
                objTest.Name = Name
                self.assertIsInstance(objTest.Name, str)
                self.assertEqual(objTest.Name, str(Name))
                self.assertIsInstance(objTest.Name, str)
                self.assertEqual(objTest.Name, str(Name))
            del objTest
    
    def test_N(self):
        """
        Checks that the length of the stored data set is returned properly.
        
        Tests ID: TEST-T-324
        Requirements ID: REQ-FUN-322

        Version 1.0.0.0
        """
        for DataX, DataY in [(self.AllIntX, self.AllIntY),
                                (self.AllFloatX, self.AllFloatY),
                                (self.MixedX, self.MixedY),
                                (self.IntErrX, self.IntErrY),
                                (self.FloatErrX, self.FloatErrY),
                                (self.MixedErrX, self.MixedErrY),
                                (self.TotalMixedX, self.TotalMixedY)]:
            objTest = self.TestClass(DataX, DataY)
            self.assertIsInstance(objTest.N, int)
            self.assertEqual(objTest.N, len(DataX))
            #check the repetitive call!
            self.assertIsInstance(objTest.N, int)
            self.assertEqual(objTest.N, len(DataX))
            del objTest

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