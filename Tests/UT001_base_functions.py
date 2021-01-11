#usr/bin/python3
"""
Module statistics_lib.Tests.UT001_base_functions

Set of unit tests on the module stastics_lib.base_functions. The test sequences
and the expected retruned values of the statistical functions are defined in
the spreadsheet file ./Test_statistics_base.ods.
"""


__version__= '1.0.0.0'
__date__ = '11-01-2021'
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

import statistics_lib.base_functions as test_module

from phyqus_lib.base_classes import MeasuredValue

#globals

X_SET = [1, 1.5, -0.5, 2.3, 1, 4, 2.3, -3, 2.4546, 2]
X_SE_SET = [0.1, 0.2, 0.1, 0.15, 0.02, 0.8, 0.3, 0.23, 0.453, 0.03]
Y_SET = [2, 3, 1, 2, 4, 2.5, 2, -2, -2, 3]
Y_SE_SET = [0.1, 0.2, 0.3, 0.1, 0.2, 0.3, 0.1, 0.2, 0.3, 0.1]
CHECKS = {
    'X' : {
        'Mean' : 1.30546,
        'VAR.P' : 3.3062803,
        'VAR.S' : 3.67364478,
        'STDEV.P' : 1.81831799,
        'STDEV.S' : 1.91667545,
        'SE' : 0.57500264,
        'SE_FULL' : 0.62242664,
        'SKEW.P' : -1.03730424,
        'SKEW.S' : -1.23009151,
        'KURT.S' : 2.30606064,
        'KURT.P' : 0.7589838,
        'E2' : 5.01050612,
        'E3' : 8.93731151,
        'E4' : 45.2394562,
        'EC3' : -6.2361371742,
        'EC4' : 41.09129171
    },
    'Y' : {
        'Mean' : 1.55,
        'VAR.P' : 3.7225,
        'VAR.S' : 4.13611111,
        'STDEV.P' : 1.92937814,
        'STDEV.S' : 2.03374313,
        'SE' : 0.61012294,
        'SE_FULL' : 0.63902269,
        'SKEW.P' : -0.94275915,
        'SKEW.S' : -1.11797482,
        'KURT.S' : 0.29878323,
        'KURT.P' : -0.37644585,
        'E2' : 6.125,
        'E3' : 14.2625,
        'E4' : 53.80625,
        'EC3' : -6.771,
        'EC4' : 36.35460625
    },
    'XY' : {
        'COV' : 1.605617,
        'PEARSON' : 0.45767245,
        '1,1' : 3.62908,
        '1,2' : 9.22184,
        '1,3' : 26.96632,
        '2,1' : 5.61098777,
        '2,2' : 27.89202446,
        '2,3' : 45.54395107,
        '3,1' : 27.308976977,
        '3,2' : 57.074246049,
        '3,3' : 167.1359079,
        'C1,1' : 1.605617,
        'C1,2' : -3.7515152,
        'C1,3' : 14.2192579,
        'C2,1' : -6.34743425,
        'C2,2' : 25.9866288092,
        'C2,3' : -87.95729868,
        'C3,1' : 30.10610687,
        'C3,2' : -96.986730785,
        'C3,3' : 352.12852232
    }
}

FLOAT_CHECK_PRECISION = 8 #digits after comma

#classes

#+ test cases

class Test_GetMean(unittest.TestCase):
    """
    Test cases for the function statistics_lib.base_functions.GetMean()
    
    Implements tests: ???. Covers the requirements
    ???.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.Data = {
            'X' : {'Real' : X_SET},
            'Y' : {'Real' : Y_SET}
        }
        cls.Data['X']['WErrors'] = [MeasuredValue(Mean, SE)
                                        for Mean, SE in zip(X_SET, X_SE_SET)]
        cls.Data['Y']['WErrors'] = [MeasuredValue(Mean, SE)
                                        for Mean, SE in zip(Y_SET, Y_SE_SET)]
        glstTemp = []
        for Mean, SE in zip(X_SET, X_SE_SET):
            bFlag = random.randint(0,1)
            if bFlag:
                glstTemp.append(MeasuredValue(Mean, SE))
            else:
                glstTemp.append(Mean)
        cls.Data['X']['Mixed'] = glstTemp
        glstTemp = []
        for Mean, SE in zip(Y_SET, Y_SE_SET):
            bFlag = random.randint(0,1)
            if bFlag:
                glstTemp.append(MeasuredValue(Mean, SE))
            else:
                glstTemp.append(Mean)
        cls.Data['Y']['Mixed'] = glstTemp
        cls.BadInput = [
            '1', ['1'], (1, '1'), int, float, str, list, tuple, [1.3, int]
        ]
        cls.Precision = FLOAT_CHECK_PRECISION
        cls.TestFunction = staticmethod(test_module.GetMean)
        cls.CheckKey = 'Mean'
    
    def test_CheckOutput(self):
        """
        Checks that the tested function computes the proper value.
        """
        for strKey in ['X', 'Y']:
            dCheckValue = CHECKS[strKey][self.CheckKey]
            for strType, glstValues in self.Data[strKey].items():
                gResult = self.TestFunction(glstValues)
                strError = '[{}][{}] as a list'.format(strKey, strType)
                self.assertAlmostEqual(gResult, dCheckValue,
                                        places = self.Precision,
                                                    msg = strError)
                gResult = self.TestFunction(tuple(glstValues))
                strError = '[{}][{}] as a tuple'.format(strKey, strType)
                self.assertAlmostEqual(gResult, dCheckValue,
                                        places = self.Precision,
                                                    msg = strError)
    
    def test_ValueError(self):
        """
        Checks that the tested function raises ValueError (or its sub-class)
        if the passed sequence is empty.
        """
        with self.assertRaises(ValueError, msg = 'an empty list'):
            self.TestFunction(list())
        with self.assertRaises(ValueError, msg = 'an empty tuple'):
            self.TestFunction(tuple())
    
    def test_TypeError(self):
        """
        Checks that the tested function raises TypeError (or its sub-class)
        if the passed argument is not a sequence of real numbers or measurements
        data with the uncertainties.
        """
        for gItem in self.BadInput:
            with self.assertRaises(TypeError, msg = str(gItem)):
                self.TestFunction(gItem)

class Test_GetMeanSquares(Test_GetMean):
    """
    Test cases for the function statistics_lib.base_functions.GetMeanSquares()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetMeanSquares)
        cls.CheckKey = 'E2'

class Test_GetVariance(Test_GetMean):
    """
    Test cases for the function statistics_lib.base_functions.GetVariance()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetVariance)
        cls.CheckKey = 'VAR.P'

class Test_GetVarianceBessel(Test_GetMean):
    """
    Test cases for the function
    statistics_lib.base_functions.GetVarianceBessel()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetVarianceBessel)
        cls.CheckKey = 'VAR.S'
    
    def test_ValueError(self):
        """
        Checks that the tested function raises ValueError (or its sub-class)
        if the passed sequence is shorter than 2 elements.
        """
        super().test_ValueError()
        with self.assertRaises(ValueError, msg = 'one element list'):
            self.TestFunction([1])
        with self.assertRaises(ValueError, msg = 'one element tuple'):
            self.TestFunction((1, ))


class Test_GetStandardDeviation(Test_GetMean):
    """
    Test cases for the function
    statistics_lib.base_functions.GetStandardDeviation()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetStandardDeviation)
        cls.CheckKey = 'STDEV.P'

class Test_GetStandardDeviationBessel(Test_GetVarianceBessel):
    """
    Test cases for the function
    statistics_lib.base_functions.GetStandardDeviationBessel()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetStandardDeviationBessel)
        cls.CheckKey = 'STDEV.S'

class Test_GetStandardError(Test_GetMean):
    """
    Test cases for the function
    statistics_lib.base_functions.GetStandardError()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetStandardError)
        cls.CheckKey = 'SE'

class Test_GetFullStandardError(Test_GetMean):
    """
    Test cases for the function
    statistics_lib.base_functions.GetFullStandardError()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetFullStandardError)
    
    def test_CheckOutput(self):
        """
        Checks that the tested function computes the proper value.
        """
        for strKey in ['X', 'Y']:
            dMin = CHECKS[strKey]['SE']
            dMax = CHECKS[strKey]['SE_FULL']
            dCheckValue = CHECKS[strKey][self.CheckKey]
            glstValues = self.Data[strKey]['Real']
            gResult = self.TestFunction(glstValues)
            strError = '[{}]["Real"] as a list'.format(strKey)
            self.assertAlmostEqual(gResult, dMin, places = self.Precision,
                                                    msg = strError)
            gResult = self.TestFunction(tuple(glstValues))
            strError = '[{}]["Real"] as a tuple'.format(strKey)
            self.assertAlmostEqual(gResult, dMin, places = self.Precision,
                                                    msg = strError)
            glstValues = self.Data[strKey]['WErrors']
            gResult = self.TestFunction(glstValues)
            strError = '[{}]["WErrors"] as a list'.format(strKey)
            self.assertAlmostEqual(gResult, dMax, places = self.Precision,
                                                    msg = strError)
            gResult = self.TestFunction(tuple(glstValues))
            strError = '[{}]["WErrors"] as a tuple'.format(strKey)
            self.assertAlmostEqual(gResult, dMax, places = self.Precision,
                                                    msg = strError)
            glstValues = self.Data[strKey]['Mixed']
            gResult = self.TestFunction(glstValues)
            strError = '[{}]["Mixed"] as a list'.format(strKey)
            self.assertTrue(dMin <= gResult <= dMax, msg = strError)
            gResult = self.TestFunction(tuple(glstValues))
            strError = '[{}]["Mixed"] as a tuple'.format(strKey)
            self.assertTrue(dMin <= gResult <= dMax, msg = strError)

class Test_GetSkewness(Test_GetMean):
    """
    Test cases for the function
    statistics_lib.base_functions.GetSkewness()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetSkewness)
        cls.CheckKey = 'SKEW.P'

class Test_GetSkewnessBessel(Test_GetVarianceBessel):
    """
    Test cases for the function
    statistics_lib.base_functions.GetSkewnessBessel()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetSkewnessBessel)
        cls.CheckKey = 'SKEW.S'
    
    def test_ValueError(self):
        """
        Checks that the tested function raises ValueError (or its sub-class)
        if the passed sequence is shorter than 3 elements.
        """
        super().test_ValueError()
        with self.assertRaises(ValueError, msg = 'two element list'):
            self.TestFunction([1, 2.9])
        with self.assertRaises(ValueError, msg = 'two element tuple'):
            self.TestFunction((1, 0.1))

class Test_GetKurtosis(Test_GetMean):
    """
    Test cases for the function
    statistics_lib.base_functions.GetKurtosis()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetKurtosis)
        cls.CheckKey = 'KURT.P'

class Test_GetKurtosisBessel(Test_GetSkewnessBessel):
    """
    Test cases for the function
    statistics_lib.base_functions.GetKurtosisBessel()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetKurtosisBessel)
        cls.CheckKey = 'KURT.S'
    
    def test_ValueError(self):
        """
        Checks that the tested function raises ValueError (or its sub-class)
        if the passed sequence is shorter than 4 elements.
        """
        super().test_ValueError()
        with self.assertRaises(ValueError, msg = 'three element list'):
            self.TestFunction([1, 2.9, 3.4])
        with self.assertRaises(ValueError, msg = 'three element tuple'):
            self.TestFunction((1, 0.1, 3))

class Test_GetMoment(Test_GetMean):
    """
    Test cases for the function
    statistics_lib.base_functions.GetMoment()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetMoment)
    
    def test_ValueError(self):
        """
        Checks that the tested function raises ValueError (or its sub-class)
        if the passed sequence is empty or the passed power in an integer but
        not positive.
        """
        with self.assertRaises(ValueError, msg = 'an empty list'):
            self.TestFunction(list(), 1)
        with self.assertRaises(ValueError, msg = 'an empty tuple'):
            self.TestFunction(tuple(), 1)
        with self.assertRaises(ValueError, msg = 'zero power'):
            self.TestFunction(self.Data['X']['Real'], 0)
        with self.assertRaises(ValueError, msg = 'negative power'):
            self.TestFunction(self.Data['X']['Real'], -1)
    
    def test_TypeError(self):
        """
        Checks that the tested function raises TypeError (or its sub-class)
        if the passed argument is not a sequence of real numbers or measurements
        data with the uncertainties, or the power in not an integer.
        """
        for gItem in self.BadInput:
            with self.assertRaises(TypeError, msg = str(gItem)):
                self.TestFunction(gItem, 1)
        for gItem in [1.0, '1', int, float, [1], (2.0, 1)]:
            with self.assertRaises(TypeError,
                                        msg = '{} as the power'.format(gItem)):
                self.TestFunction(self.Data['X']['Real'], gItem)
    
    def test_CheckOutput(self):
        """
        Checks that the tested function computes the proper value.
        """
        for strKey in ['X', 'Y']:
            for strType, glstValues in self.Data[strKey].items():
                for iPower, strCheckKey in enumerate(['Mean',
                                                            'E2', 'E3', 'E4']):
                    dCheckValue = CHECKS[strKey][strCheckKey]
                    gResult = self.TestFunction(glstValues, iPower + 1,
                                                            IsCentral = False)
                    strError='[{}][{}] as a list - power {}, not centr'.format(
                                                        strKey, strType, iPower)
                    self.assertAlmostEqual(gResult, dCheckValue,
                                            places = self.Precision,
                                                        msg = strError)
                    gResult = self.TestFunction(tuple(glstValues), iPower + 1,
                                                            IsCentral = False)
                    strError='[{}][{}] as a tuple - power {}, not centr'.format(
                                                        strKey, strType, iPower)
                    self.assertAlmostEqual(gResult, dCheckValue,
                                            places = self.Precision,
                                                        msg = strError)
                for iPower, strCheckKey in enumerate(['Mean',
                                                        'VAR.P', 'EC3', 'EC4']):
                    if iPower:
                        dCheckValue = CHECKS[strKey][strCheckKey]
                    else:
                        dCheckValue = 0
                    gResult = self.TestFunction(glstValues, iPower + 1)
                    strError='[{}][{}] as a list - power {}, central'.format(
                                                    strKey, strType, iPower + 1)
                    self.assertAlmostEqual(gResult, dCheckValue,
                                            places = self.Precision,
                                                        msg = strError)
                    gResult = self.TestFunction(tuple(glstValues), iPower + 1)
                    strError='[{}][{}] as a tuple - power {}, central'.format(
                                                    strKey, strType, iPower + 1)
                    self.assertAlmostEqual(gResult, dCheckValue,
                                            places = self.Precision,
                                                        msg = strError)

class Test_GetCovariance(Test_GetMean):
    """
    Test cases for the function
    statistics_lib.base_functions.GetCovariance()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetCovariance)
        cls.CheckKey = 'COV'
    
    def test_TypeError(self):
        """
        Checks that the tested function raises TypeError (or its sub-class)
        if any of the passed arguments is not a sequence of real numbers or
        measurements data with the uncertainties.
        """
        for gItem in self.BadInput:
            if isinstance(gItem, (list, tuple)):
                lstOther = [1] * len(gItem)
            else:
                lstOther = [1]
            with self.assertRaises(TypeError,
                                        msg = '{} - first'.format(str(gItem))):
                self.TestFunction(gItem, lstOther)
            with self.assertRaises(TypeError,
                                        msg = '{} - second'.format(str(gItem))):
                self.TestFunction(lstOther, gItem)
    
    def test_ValueError(self):
        """
        Checks that the tested function raises ValueError (or its sub-class)
        if any of the passed sequence is empty or the lengths of the sequences
        are not not equal.
        """
        with self.assertRaises(ValueError, msg = 'an empty list - first'):
            self.TestFunction(list(), [1])
        with self.assertRaises(ValueError, msg = 'an empty tuple - first'):
            self.TestFunction(tuple(), [1])
        with self.assertRaises(ValueError, msg = 'an empty list - second'):
            self.TestFunction([1], list())
        with self.assertRaises(ValueError, msg = 'an empty tuple - second'):
            self.TestFunction([1], tuple())
        with self.assertRaises(ValueError, msg = 'inequal length'):
            self.TestFunction([1], [1,2])
    
    def test_CheckOutput(self):
        """
        Checks that the tested function computes the proper value.
        """
        dCheckValue = CHECKS['XY'][self.CheckKey]
        for strType in self.Data['X'].keys():
            glstValuesX = self.Data['X'][strType]
            glstValuesY = self.Data['Y'][strType]
            gResult = self.TestFunction(glstValuesX, glstValuesY)
            strError='{} as lists'.format(strType)
            self.assertAlmostEqual(gResult, dCheckValue,
                                        places = self.Precision, msg = strError)
            gResult = self.TestFunction(tuple(glstValuesX), tuple(glstValuesY))
            strError='{} as tuples'.format(strType)
            self.assertAlmostEqual(gResult, dCheckValue,
                                        places = self.Precision, msg = strError)

class Test_GetPearsonR(Test_GetCovariance):
    """
    Test cases for the function
    statistics_lib.base_functions.GetPearsonR()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetPearsonR)
        cls.CheckKey = 'PEARSON'

class Test_GetMoment2(Test_GetMean):
    """
    Test cases for the function
    statistics_lib.base_functions.GetMoment2()
    
    Implements tests: ???. Covers the requirements
    ???.
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(test_module.GetMoment2)
    
    def test_ValueError(self):
        """
        Checks that the tested function raises ValueError (or its sub-class)
        if any of the passed sequence is empty or any of the passed power in an
        integer but not positive or the lengths of the sequences are not not
        equal.
        """
        with self.assertRaises(ValueError, msg = 'an empty list - first'):
            self.TestFunction(list(), [1], 1, 1)
        with self.assertRaises(ValueError, msg = 'an empty tuple - first'):
            self.TestFunction(tuple(), [1], 1, 1)
        with self.assertRaises(ValueError, msg = 'an empty list - second'):
            self.TestFunction([1], list(), 1, 1)
        with self.assertRaises(ValueError, msg = 'an empty tuple - second'):
            self.TestFunction([1], tuple(), 1, 1)
        with self.assertRaises(ValueError, msg = 'inequal length'):
            self.TestFunction([1], [1,2], 1, 1)
        with self.assertRaises(ValueError, msg = 'zero power - first'):
            self.TestFunction(self.Data['X']['Real'], self.Data['Y']['Real'],
                                                                        0, 1)
        with self.assertRaises(ValueError, msg = 'negative power - first'):
            self.TestFunction(self.Data['X']['Real'], self.Data['Y']['Real'],
                                                                        -1, 1)
        with self.assertRaises(ValueError, msg = 'zero power - second'):
            self.TestFunction(self.Data['X']['Real'], self.Data['Y']['Real'],
                                                                        1, 0)
        with self.assertRaises(ValueError, msg = 'negative power - second'):
            self.TestFunction(self.Data['X']['Real'], self.Data['Y']['Real'],
                                                                        1, -1)
    
    def test_TypeError(self):
        """
        Checks that the tested function raises TypeError (or its sub-class)
        if any of the passed argument is not a sequence of real numbers or
        measurements data with the uncertainties, or any of the powers in not an
        integer.
        """
        for gItem in self.BadInput:
            if isinstance(gItem, (list, tuple)):
                lstOther = [1] * len(gItem)
            else:
                lstOther = [1]
            with self.assertRaises(TypeError,
                                        msg = '{} - first'.format(str(gItem))):
                self.TestFunction(gItem, lstOther, 1, 1)
            with self.assertRaises(TypeError,
                                        msg = '{} - second'.format(str(gItem))):
                self.TestFunction(lstOther, gItem, 1, 1)
        for gItem in [1.0, '1', int, float, [1], (2.0, 1)]:
            with self.assertRaises(TypeError,
                        msg = '{} as the first power'.format(gItem)):
                self.TestFunction(self.Data['X']['Real'],self.Data['Y']['Real'],
                                                                    gItem, 1)
            with self.assertRaises(TypeError,
                        msg = '{} as the second power'.format(gItem)):
                self.TestFunction(self.Data['X']['Real'],self.Data['Y']['Real'],
                                                                    1, gItem)
    
    def test_CheckOutput(self):
        """
        Checks that the tested function computes the proper value.
        """
        for iPowerX in range(1, 4):
            for iPowerY in range(1, 4):
                strCheckKey = '{},{}'.format(iPowerX, iPowerY)
                dCheckValue = CHECKS['XY'][strCheckKey]
                for strType in self.Data['X'].keys():
                    glstValuesX = self.Data['X'][strType]
                    glstValuesY = self.Data['Y'][strType]
                    gResult = self.TestFunction(glstValuesX, glstValuesY,
                                            iPowerX, iPowerY, IsCentral = False)
                    strError='{} as lists - powers {}, {}, not centr'.format(
                                            strType, iPowerX, iPowerY)
                    self.assertAlmostEqual(gResult, dCheckValue,
                                            places = self.Precision,
                                                        msg = strError)
                    gResult = self.TestFunction(tuple(glstValuesX),
                                                tuple(glstValuesY),
                                            iPowerX, iPowerY, IsCentral = False)
                    strError='{} as tuples - powers {}, {}, not centr'.format(
                                                    strType, iPowerX, iPowerY)
                    self.assertAlmostEqual(gResult, dCheckValue,
                                            places = self.Precision,
                                                        msg = strError)
                strCheckKey = 'C{},{}'.format(iPowerX, iPowerY)
                dCheckValue = CHECKS['XY'][strCheckKey]
                for strType in self.Data['X'].keys():
                    glstValuesX = self.Data['X'][strType]
                    glstValuesY = self.Data['Y'][strType]
                    gResult = self.TestFunction(glstValuesX, glstValuesY,
                                                            iPowerX, iPowerY)
                    strError='{} as lists - powers {}, {}, central'.format(
                                                    strType, iPowerX, iPowerY)
                    self.assertAlmostEqual(gResult, dCheckValue,
                                            places = self.Precision,
                                                        msg = strError)
                    gResult = self.TestFunction(tuple(glstValuesX),
                                                tuple(glstValuesY),
                                                            iPowerX, iPowerY)
                    strError='{} as tuples - powers {}, {}, central'.format(
                                                    strType, iPowerX, iPowerY)
                    self.assertAlmostEqual(gResult, dCheckValue,
                                            places = self.Precision,
                                                        msg = strError)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMean)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMeanSquares)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_GetVariance)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_GetVarianceBessel)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetStandardDeviation)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetStandardDeviationBessel)
TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetStandardError)
TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetFullStandardError)
TestSuite9 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetSkewness)
TestSuite10 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetSkewnessBessel)
TestSuite11 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetKurtosis)
TestSuite12 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetKurtosisBessel)
TestSuite13 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetMoment)
TestSuite14 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetMoment2)
TestSuite15 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetCovariance)
TestSuite16 = unittest.TestLoader().loadTestsFromTestCase(
                                            Test_GetPearsonR)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6, TestSuite7, TestSuite8, TestSuite9, TestSuite10,
                    TestSuite11, TestSuite12, TestSuite13, TestSuite14,
                    TestSuite15, TestSuite16])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.base_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
