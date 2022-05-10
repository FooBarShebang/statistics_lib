#usr/bin/python3
"""
Module statistics_lib.stat_tests

Implements statistical significance tests as functions returning a class
instance, which can generate human-readable report.

Classes:
    TestTypes
    TestResult

Functions:
    

Constants:
    GT_TEST: enum(TestType) - indication for 1-sided right-tailed test
    LT_TEST: enum(TestType) - indication for 1-sided left-tailed test
    NEQ_TEST: enum(TestType) - indication for 2-sided test
"""

__version__= '1.0.0.0'
__date__ = '10-05-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os

from typing import Tuple, Union

from enum import Enum

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#globals

#+ data types

T_REAL = Union[int, float]

T_BOUND = Union[T_REAL, None]

T_CRIT_BOUNDS = Tuple[T_BOUND, T_BOUND]

#classes

class TestTypes(Enum):
    """
    Enumeration (meta-) class for the identification of the 1- / 2-sided
    statistical significance tests. Each enumaration value is definced by two
    strings - the null hypothesis and the alternative hypothesis, which will
    be accessible via properties H0 and H1.
    
    Version 1.0.0.0
    """
    LEFT = ('greater than or equal to', 'less than')
    RIGHT = ('less than or equal to', 'greater than')
    TWO_SIDED = ('equal to', 'not equal to')
    
    def __init__(self, H0: str, H1: str):
        self._ExtraData = {'H0' : H0, 'H1' : H1}
    
    @property
    def H0(self) -> str:
        return self._ExtraData['H0']
    
    @property
    def H1(self) -> str:
        return self._ExtraData['H1']

#aliases

GT_TEST = TestTypes.RIGHT
LT_TEST = TestTypes.LEFT
NEQ_TEST = TestTypes.TWO_SIDED

class TestResult:
    """
    Helper class to represent the results of the statistical significance tests.
    The end-user is not supposed to instantiate this class manually, but only
    to receive such an instance as the return value of the corresponding
    function.
    
    Properties:
        IsRejected: (read-only) bool
        p_Value: (read-only) 0 <= float <= 1
        Report: (read-only) str
    
    Version 1.0.0.0
    """
    
    #special methods
    
    def __init__(self, TestName: str, DataName: str, ModelName: str,
                            TestValue: T_REAL, CDF_Value: float,
                                            CritValues: T_CRIT_BOUNDS) -> None:
        """
        Initialization. Performs the input data sanity checks and stores the
        passed data as the object state.
        
        Signature:
            str, str, str, int OR float, 0 < float < 1,
                tuple(int OR float OR None, int OR float OR None) -> None
        
        Args:
            TestName: str; the name of the test, including the parameters and
                confidence level
            DataName: str; the identificator of the data set(s)
            ModelName: str; the name of the class implementing the model
                distribution, including the parameters
            TestValue: int or float; the calculated test value
            CDF_Value: 0 < float < 1; the calculated CDF value at the test value
            CritValues: tuple(int OR float OR None, int OR float OR None);
                the lower and upper critical values, both cannot be None
                simultaneously
        
        Raises:
            UT_TypeError: any of the arguments is on an unexpected / wrong
                data types
            UT_ValueError: CDF_Value is not in the range (0, 1), OR the upper
                critical value is not greater than or equal to the lower one
        
        Version 1.0.0.0
        """
        if not isinstance(TestName, str):
            raise UT_TypeError(TestName, str, SkipFrames = 1)
        if not isinstance(DataName, str):
            raise UT_TypeError(DataName, str, SkipFrames = 1)
        if not isinstance(ModelName, str):
            raise UT_TypeError(ModelName, str, SkipFrames = 1)
        if not isinstance(TestValue, (int, float)):
            raise UT_TypeError(TestName, (int, float), SkipFrames = 1)
        if not isinstance(CDF_Value, float):
            raise UT_TypeError(CDF_Value, float, SkipFrames = 1)
        if not isinstance(CritValues, tuple):
            raise UT_TypeError(CritValues, tuple, SkipFrames = 1)
        strError= '{} is not 2-tuple of real numbers or None'.format(CritValues)
        bCond1 = len(CritValues) != 2
        bCond2 = (CritValues[0] is None) and (CritValues[1] is None)
        bCond3 = False
        for Item in CritValues:
            if (not isinstance(Item, (int, float))) and (not (Item is None)):
                bCond3 = True
                break
        if bCond1 or bCond2 or bCond3:
            objError = UT_TypeError(CritValues, tuple, SkipFrames = 1)
            objError.args = (strError, )
            raise objError
        if CDF_Value >= 1.0 or CDF_Value <= 0.0:
            raise UT_ValueError(CDF_Value, 'in the range (0, 1)', SkipFrames= 1)
        bCond = (not (CritValues[0] is None)) and (not (CritValues[1] is None))
        if bCond and CritValues[1] < CritValues[0]:
            strError = 'second item must be greater then or equal to the first'
            raise UT_ValueError(CritValues, strError, SkipFrames = 1)
        self._Data = dict()
        self._Data['TestName'] = TestName
        self._Data['DataName'] = DataName
        self._Data['ModelName'] = ModelName
        self._Data['TestValue'] = TestValue
        self._Data['CDF_Value'] = CDF_Value
        self._Data['CritValues'] = CritValues
    
    #public API - properties
    
    @property
    def IsRejected(self) -> bool:
        """
        Getter (read-only) property to access the total outcome of the test.
        
        Signature:
            None -> bool
        
        Returns:
            bool: if the null hypothesis is rejected (True) or the test fails
                to reject the null hypothesis (False)
        
        Version 1.0.0.0
        """
        CritValues = self._Data['CritValues']
        TestValue = self._Data['TestValue']
        Result = False
        if CritValues[1] is None: #1-sided left-tailed
            if TestValue <= CritValues[0]:
                Result = True
        elif CritValues[0] is None: #1-sided right-tailed
            if TestValue >= CritValues[1]:
                Result = True
        elif CritValues[0] is CritValues[1]: #1-sided right-tailed special
            if TestValue >= CritValues[1]:
                Result = True
        else: #2-sided
            if TestValue >= CritValues[1] or TestValue <= CritValues[0]:
                Result = True
        return Result
    
    @property
    def p_Value(self) -> float:
        """
        Getter (read-only) property to access the p_Value of the test.
        
        Signature:
            None -> 0 <= float <= 1
        
        Version 1.0.0.0
        """
        CritValues = self._Data['CritValues']
        TestValue = self._Data['CDF_Value']
        if CritValues[1] is None: #1-sided left-tailed
            Result = TestValue
        elif CritValues[0] is None: #1-sided right-tailed
            Result = 1.0 - TestValue
        elif CritValues[0] is CritValues[1]: #1-sided right-tailed special
            Result = 1.0 - TestValue
        else: #2-sided
            if TestValue >= 0.5:
                Result = 2 * ( 1.0 - TestValue)
            else:
                Result = 2.0 * TestValue
        return Result
    
    @property
    def Report(self) -> str:
        """
        Getter (read-only) property to access the human-readable, multi-line
        string report on the test.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        CritValues = self._Data['CritValues']
        if CritValues[1] is None: #1-sided left-tailed
            TestType = '1-sided left-tailed'
            CritValueLine = 'Critical value: {}'.format(CritValues[0])
            TestID = TestTypes.LEFT
        elif CritValues[0] is None: #1-sided right-tailed
            TestType = '1-sided right-tailed'
            CritValueLine = 'Critical value: {}'.format(CritValues[1])
            TestID = TestTypes.RIGHT
        elif CritValues[0] is CritValues[1]: #1-sided right-tailed special
            TestType = '1-sided right-tailed'
            CritValueLine = 'Critical value: {}'.format(CritValues[1])
            TestID = TestTypes.TWO_SIDED
        else: #2-sided
            TestType = '2-sided'
            CritValueLine = 'Critical values: {} and {}'.format(CritValues[0],
                                                                CritValues[1])
            TestID = TestTypes.TWO_SIDED
        H0 = TestID.H0
        H1 = TestID.H1
        if self.IsRejected:
            IsRejected = 'Yes'
        else:
            IsRejected = 'No'
        Result = '\n'.join(['Statistical test report.',
                    'Name: {}'.format(self._Data['TestName']),
                    'Data: {}'.format(self._Data['DataName']),
                    'Type: {}'.format(TestType),
                    'Model distribution: {}'.format(self._Data['ModelName']),
                    'Null hypothesis: {}'.format(H0),
                    'Alternative hypothesis: {}'.format(H1),
                    CritValueLine,
                    'Test value: {}'.format(self._Data['TestValue']),
                    'p-value: {}'.format(self.p_Value),
                    'Is null hypothesis rejected?: {}'.format(IsRejected)])
        return Result
