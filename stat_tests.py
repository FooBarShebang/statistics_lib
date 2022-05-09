#usr/bin/python3
"""
Module statistics_lib.stat_tests

???

Classes:
    TestResult

"""

__version__= '1.0.0.0'
__date__ = '09-05-2022'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os

from typing import Tuple, Union

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

class TestResult:
    """
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
        if CritValues[1] < CritValues[0]:
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
        elif CritValues[0] is CritValues[1]: #1-sided right-tailed
            if TestValue >= CritValues[1]:
                Result = True
        else: #2-sided
            if TestValue >= CritValues[1] or TestValue <= CritValues[0]:
                Result = True
        return Result
