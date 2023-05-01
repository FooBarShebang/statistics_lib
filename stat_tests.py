#usr/bin/python3
"""
Module statistics_lib.stat_tests

Implements statistical significance tests as functions returning a class
instance, which can generate human-readable report. The input data must be
passed as instance(s) of Statistics1D class, and the test type (1-sided left- or
right-tailed, 2-sided) must be indicated using the enumeration values GT_TEST,
LT_TEST or NEQ_TEST defined in this module.

Classes:
    TestTypes
    TestResult

Functions:
    z_test(Data, Mean, Sigma, Type, *, Confidence = 0.95):
        Statistics1D, int OR float, int > 0 OR float > 0, TestTypes
            /, *, 0 < float < 1/ -> TestResult
    t_test(Data, Mean, Type, *, Confidence = 0.95):
        Statistics1D, int OR float, TestTypes/, *, 0 < float < 1/ -> TestResult
    chi_squared_test(Data, Sigma, Type, *, Confidence = 0.95):
        Statistics1D, int > 0 OR float > 0, TestTypes
            /, *, 0 < float < 1/ -> TestResult
    unpaired_t_test(Data1, Data2, Type, *, Confidence = 0.95):
        Statistics1D, Statistics1D, TestTypes/, *, 0 < float < 1/ -> TestResult
    paired_t_test(Data1, Data2, Type, *, Confidence = 0.95, Bias = 0.0):
        Statistics1D, Statistics1D, TestTypes
            /, *, 0 < float < 1, int OR float/ -> TestResult
    Welch_t_test(Data1, Data2, Type, *, Confidence = 0.95):
        Statistics1D, Statistics1D, TestTypes/, *, 0 < float < 1/ -> TestResult
    f_test(Data1, Data2, Type, *, Confidence = 0.95, Delta = 1.0):
        Statistics1D, Statistics1D, TestTypes
            /, *, 0 < float < 1, int > 0 OR float > 0/ -> TestResult
    ANOVA_test(Data1, Data2, *, Confidence = 0.95):
        Statistics1D, Statistics1D/, *, 0 < float < 1/ -> TestResult
    Levene_test(Data1, Data2, *, Confidence = 0.95):
        Statistics1D, Statistics1D/, *, 0 < float < 1/ -> TestResult
    Brown_Forsythe_test(Data1, Data2, *, Confidence = 0.95):
        Statistics1D, Statistics1D/, *, 0 < float < 1/ -> TestResult

Constants:
    GT_TEST: enum(TestType) - indication for 1-sided right-tailed test
    LT_TEST: enum(TestType) - indication for 1-sided left-tailed test
    NEQ_TEST: enum(TestType) - indication for 2-sided test
"""

__version__= '1.1.0.0'
__date__ = '01-05-2023'
__status__ = 'Production'

#imports

#+ standard library

import sys
import os
import math

from typing import Tuple, Union, Any

from enum import Enum

from .base_functions import TReal

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

from .data_classes import Statistics1D as DC

import statistics_lib.distribution_classes as MC

#globals

DEF_CONF = 0.95

MIN_CDF = 0.0000001

MAX_CDF = 1 - MIN_CDF

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
    
    Version 1.0.1.0
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
        
        Version 1.0.1.0
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
        Message = f'{CritValues} is not 2-tuple of real numbers or None'
        Cond1 = len(CritValues) != 2
        Cond2 = (CritValues[0] is None) and (CritValues[1] is None)
        Cond3 = False
        for Item in CritValues:
            if (not isinstance(Item, (int, float))) and (not (Item is None)):
                Cond3 = True
                break
        if Cond1 or Cond2 or Cond3:
            Error = UT_TypeError(CritValues, tuple, SkipFrames = 1)
            Error.setMessage(Message)
            raise Error
        if CDF_Value >= 1.0 or CDF_Value <= 0.0:
            raise UT_ValueError(CDF_Value, 'in the range (0, 1)', SkipFrames= 1)
        Cond = (not (CritValues[0] is None)) and (not (CritValues[1] is None))
        if Cond and CritValues[1] < CritValues[0]:
            Message = 'second item must be greater then or equal to the first'
            raise UT_ValueError(CritValues, Message, SkipFrames = 1)
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
        
        Version 1.0.1.0
        """
        _Data = self._Data
        CritValues = _Data['CritValues']
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
                            f'Name: {_Data["TestName"]}',
                            f'Data: {_Data["DataName"]}',
                            f'Type: {TestType}',
                            f'Model distribution: {_Data["ModelName"]}',
                            f'Null hypothesis: {H0}',
                            f'Alternative hypothesis: {H1}',
                            CritValueLine,
                            f'Test value: {_Data["TestValue"]}',
                            f'p-value: {self.p_Value}',
                            f'Is null hypothesis rejected?: {IsRejected}'])
        return Result

#functions

#+ 'private' check functions

def _CheckData1D(Data: Any) -> None:
    """
    Helper function to check that the passed argument is an instance of class
    statistics_lib.data_classes.Statistics1D, and it contains more than a single
    data point.
    
    Signature:
        type A -> None
    
    Raises:
        UT_TypeError: the passed argument is not an instance of Statistics1D
        UT_ValueError: it contains less than 2 data points
    
    Version 1.0.0.0
    """
    if not isinstance(Data, DC):
        raise UT_TypeError(Data, DC, SkipFrames = 2)
    if Data.N < 2:
        raise UT_ValueError(Data.N, '> 1 - data length', SkipFrames = 2)

def _CheckData2D(Data1: Any, Data2: Any) -> None:
    """
    Helper function to check that the passed arguments are the instances of
    statistics_lib.data_classes.Statistics1D class, and they contain more than a
    single data point each.
    
    Signature:
        type A, type B -> None
    
    Raises:
        UT_TypeError: any of the passed arguments is not an instance of
            Statistics1D class
        UT_ValueError: any of the passed arguments contains less than 2 data
            points
    
    Version 1.0.0.0
    """
    if not isinstance(Data1, DC):
        raise UT_TypeError(Data1, DC, SkipFrames = 2)
    if not isinstance(Data2, DC):
        raise UT_TypeError(Data2, DC, SkipFrames = 2)
    if Data1.N < 2:
        raise UT_ValueError(Data1.N, '> 1 - data length, first sample',
                                                                SkipFrames = 2)
    if Data2.N < 2:
        raise UT_ValueError(Data2.N, '> 1 - data length, second sample',
                                                                SkipFrames = 2)

def _CheckTestParameters(Type: Any, Confidence: Any) -> None:
    """
    Helper function to check the statistics test definition parameters.
    
    Signature:
        type A, type B -> None
        
    Raises:
        UT_TypeError: test type is not an instance of TestType enumeration, OR
            confidence value is not a floating point number
        UT_ValueError: confidence value in not in the open range (0, 1)
    
    Version 1.0.0.0
    """
    if not isinstance(Type, TestTypes):
        raise UT_TypeError(Type, TestTypes, SkipFrames = 2)
    if not isinstance(Confidence, float):
        raise UT_TypeError(Confidence, float, SkipFrames = 2)
    if Confidence <= 0 or Confidence >= 1:
        raise UT_ValueError(Confidence, 'in range (0, 1) - confidence',
                                                                SkipFrames = 2)

#+ 'private' work base function

def _GetCDF(Model: MC.ContinuousDistributionABC, TestValue: TReal) -> TReal:
    """
    Helper funtion to calculate the cummulative distribution function value at
    the given test value. The values are capped to [0.0000001, 1 - 0.0000001]
    closed interval.
    
    Signature:
        statistics_lib.distribution_classes.ContinuousDistributionABC,
            int OR float -> int OR float 
    
    Args:
        Model: ContinuousDistributionABC; instance of any sub-class off, the
            model data distribution
        TestValue: int OR float; the test value
    
    Returns:
        int OR float: the calculated CDF value
    
    Version 1.0.0.0
    """
    CDF_Value = Model.cdf(TestValue)
    if CDF_Value <= 0.0:
        CDF_Value = MIN_CDF
    elif CDF_Value >= 1.0:
        CDF_Value = MAX_CDF
    return CDF_Value

def _GetBoundariesSym(Model: MC.ContinuousDistributionABC, Type: TestTypes,
                                            Confidence: float) -> T_CRIT_BOUNDS:
    """
    Helper function to calculate the critical value bounds of the test in the
    case of the symmetric model distribution.
    
    Signature:
        statistics_lib.distribution_classes.ContinuousDistributionABC,
            TestTypes, float -> tuple(None OR int OR float)
    
    Args:
        Model: ContinuousDistributionABC; instance of any sub-class off, the
            model data distribution
        Type: TestType; instance of the enum class representing left-, right-
            or two-tailed test
        Confidence: float; value of the test confidence
    
    Returns:
        (int OR float, None): for the left-tailed test
        (None, int OR float): for the right-tailed test
        (int OR float, int OR float): for the two-tailed test
    
    Version 1.0.0.0
    """
    if Type is TestTypes.LEFT:
        CritValue = Model.qf(1-Confidence)
        CriticalValues = (CritValue, None)
    elif Type is TestTypes.RIGHT:
        CritValue = Model.qf(Confidence)
        CriticalValues = (None, CritValue)
    else:
        CritValue = Model.qf(0.5 * (1 + Confidence))
        CriticalValues = (-CritValue, CritValue)
    return CriticalValues

def _GetBoundariesAsym(Model: MC.ContinuousDistributionABC, Type: TestTypes,
                                            Confidence: float) -> T_CRIT_BOUNDS:
    """
    Helper function to calculate the critical value bounds of the test in the
    case of the asymmetric model distribution.
    
    Signature:
        statistics_lib.distribution_classes.ContinuousDistributionABC,
            TestTypes, float -> tuple(None OR int OR float)
    
    Args:
        Model: ContinuousDistributionABC; instance of any sub-class off, the
            model data distribution
        Type: TestType; instance of the enum class representing left-, right-
            or two-tailed test
        Confidence: float; value of the test confidence
    
    Returns:
        (int OR float, None): for the left-tailed test
        (None, int OR float): for the right-tailed test
        (int OR float, int OR float): for the two-tailed test
    
    Version 1.0.0.0
    """
    if Type is TestTypes.LEFT:
        CritValue = Model.qf(1-Confidence)
        CriticalValues = (CritValue, None)
    elif Type is TestTypes.RIGHT:
        CritValue = Model.qf(Confidence)
        CriticalValues = (None, CritValue)
    else:
        CritValueUpper = Model.qf(0.5 * (1 + Confidence))
        CritValueLower = Model.qf(0.5 * (1 - Confidence))
        CriticalValues = (CritValueLower, CritValueUpper)
    return CriticalValues

def _DoTest1D(Model: MC.ContinuousDistributionABC, Data: DC, TestValue: TReal,
            Confidence: float, Type: TestTypes, TestName: str) -> TestResult:
    """
    Helper function to create the report for 1-sample test.
    
    Signature:
        statistics_lib.distribution_classes.ContinuousDistributionABC,
            Statistics1D, Statistics1D, int OR float, float, TestTypes,
                str -> TestResult
    
    Args:
        Model: ContinuousDistributionABC; instance of any sub-class off, the
            model data distribution
        Data: Statistics1D; instance of, the test data
        TestValue: int OR float; the calculated test value
        Confidence: float; value of the test confidence
        Type: TestType; instance of the enum class representing left-, right-
            or two-tailed test
        TestName: str; human-readable test name / information
    
    Returns:
        TestResult: instance of the class, containg the full test report
    
    Version 1.0.0.0
    """
    CDF_Value = _GetCDF(Model, TestValue)
    CriticalValues = _GetBoundariesSym(Model, Type, Confidence)
    DataName = str(Data.Name)
    ModelName = Model.Name
    Result = TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                CriticalValues)
    return Result

def _DoTest2D(Model: MC.ContinuousDistributionABC, Data1: DC, Data2: DC,
                    TestValue: TReal, Confidence: float,
                                Type: TestTypes, TestName: str) -> TestResult:
    """
    Helper function to create the report for 2-samples test.
    
    Signature:
        statistics_lib.distribution_classes.ContinuousDistributionABC,
            Statistics1D, Statistics1D, int OR float, float, TestTypes,
                str -> TestResult
    
    Args:
        Model: ContinuousDistributionABC; instance of any sub-class off, the
            model data distribution
        Data1: Statistics1D; instance of, the first test data
        Data2: Statistics1D; instance of, the second test data
        TestValue: int OR float; the calculated test value
        Confidence: float; value of the test confidence
        Type: TestType; instance of the enum class representing left-, right-
            or two-tailed test
        TestName: str; human-readable test name / information
    
    Returns:
        TestResult: instance of the class, containg the full test report
    
    Version 1.0.0.0
    """
    CDF_Value = _GetCDF(Model, TestValue)
    CriticalValues = _GetBoundariesSym(Model, Type, Confidence)
    DataName = '{} vs {}'.format(Data1.Name, Data2.Name)
    ModelName = Model.Name
    Result = TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                CriticalValues)
    return Result

#+ work functions

def z_test(Data: DC, Mean: T_REAL, Sigma: T_REAL, Type: TestTypes, *,
                                    Confidence: float = DEF_CONF) -> TestResult:
    """
    Implementation of the Z-test, comparing the sample's mean with the known
    population mean. The actual population standard deviation must be known.
    
    Signature:
        Statistics1D, int OR float, int > 0 OR float > 0, TestTypes
            /, *, 0 < float < 1/ -> TestResult
    
    Args:
        Data: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class
        Mean: int OR float; the mean of the population parameter of the model
            distribution
        Sigma: int > 0 OR float > 0; the standard deviation of the population
            parameter of the model distribution
        Type: TestTypes; an enumeration value indicating the 1- or 2-sided
            nature of the test, use values GT_TEST, LT_TEST and NEQ_TEST defined
            in this module
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%.
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Sigma argument is zero or negative, OR Confidence
            argument is not in the range (0, 1), OR data sequence is less than
            2 elements long
    
    Version 2.0.0.0
    """
    _CheckData1D(Data)
    _CheckTestParameters(Type, Confidence)
    if not isinstance(Mean, (int, float)):
        raise UT_TypeError(Mean, (int, float), SkipFrames = 1)
    if not isinstance(Sigma, (int, float)):
        raise UT_TypeError(Sigma, (int, float), SkipFrames = 1)
    if Sigma <= 0:
        raise UT_ValueError(Sigma, '> 0 - population sigma', SkipFrames = 1)
    TestValue = math.sqrt(Data.N) * (Data.Mean - Mean) / Sigma
    Model = MC.Z_Distribution()
    TestName = ' '.join(['Z-test at {:.1f}%'.format(100 * Confidence),
                            'confidence on the sample`s mean vs population',
                                        f'mean = {Mean} and sigma = {Sigma}'])
    Result = _DoTest1D(Model, Data, TestValue, Confidence, Type, TestName)
    del Model
    return Result

def t_test(Data: DC, Mean: T_REAL, Type: TestTypes, *,
                                    Confidence: float = DEF_CONF) -> TestResult:
    """
    Implementation of the one sample Student`s t-test, comparing the sample's
    mean with the known population mean. The actual population standard
    deviation is unknown.
    
    Signature:
        Statistics1D, int OR float, TestTypes/, *, 0 < float < 1/ -> TestResult
    
    Args:
        Data: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class
        Mean: int OR float; the mean of the population parameter of the model
            distribution
        Type: TestTypes; an enumeration value indicating the 1- or 2-sided
            nature of the test, use values GT_TEST, LT_TEST and NEQ_TEST defined
            in this module
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%.
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Confidence argument is not in the range (0, 1), OR the
            data sequence is less than 2 elements long
    
    Version 2.0.0.0
    """
    _CheckData1D(Data)
    _CheckTestParameters(Type, Confidence)
    if not isinstance(Mean, (int, float)):
        raise UT_TypeError(Mean, (int, float), SkipFrames = 1)
    TestValue = math.sqrt(Data.N - 1) * (Data.Mean - Mean) / Data.FullSigma
    Model = MC.Student(Degree = Data.N - 1)
    TestName = ' '.join(['One sample Student`s t-test at {:.1f}%'.format(
                                                            100 * Confidence),
                            'confidence on the sample`s mean vs population',
                                                            f'mean = {Mean}'])
    Result = _DoTest1D(Model, Data, TestValue, Confidence, Type, TestName)
    del Model
    return Result
    
def chi_squared_test(Data: DC, Sigma: T_REAL, Type: TestTypes, *,
                                        Confidence: float = 0.95) -> TestResult:
    """
    Implementation of the chi-squared test, comparing the sample's standard
    deviation with the known population standard deviation.
    
    Signature:
        Statistics1D, int > 0 OR float > 0, TestTypes
            /, *, 0 < float < 1/ -> TestResult
    
    Args:
        Data: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class
        Sigma: int > 0 OR float > 0; the standard deviation of the population
            parameter of the model distribution
        Type: TestTypes; an enumeration value indicating the 1- or 2-sided
            nature of the test, use values GT_TEST, LT_TEST and NEQ_TEST defined
            in this module
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%.
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Confidence argument is not in the range (0, 1), OR the
            data sequence is less than 2 elements long, OR the Sigma argument
            is not positive
    
    Version 2.0.0.0
    """
    _CheckData1D(Data)
    _CheckTestParameters(Type, Confidence)
    if not isinstance(Sigma, (int, float)):
        raise UT_TypeError(Sigma, (int, float), SkipFrames = 1)
    if Sigma <= 0:
        raise UT_ValueError(Sigma, '> 0 - population sigma', SkipFrames = 1)
    TestValue = Data.N * Data.FullVar / (Sigma * Sigma)
    Model = MC.ChiSquared(Degree = Data.N - 1)
    CDF_Value = _GetCDF(Model, TestValue)
    CriticalValues = _GetBoundariesAsym(Model, Type, Confidence)
    TestName = ' '.join(['Chi-squared test at {:.1f}% confidence'.format(
                                                            100 * Confidence),
                            'on the sample`s standard deviation vs population',
                                                            f'sigma = {Sigma}'])
    DataName = str(Data.Name)
    ModelName = Model.Name
    Result = TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                CriticalValues)
    del Model
    return Result

def unpaired_t_test(Data1: DC, Data2: DC, Type: TestTypes, *,
                                        Confidence: float = 0.95) -> TestResult:
    """
    Implementation of the unpaired Student`s t-test, comparing the samples`
    means. The samples`s variances are expected to differ no more by 2 times.
    
    Signature:
        Statistics1D, Statistics1D, TestTypes/, *, 0 < float < 1/ -> TestResult
    
    Args:
        Data1: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the first sample
        Data2: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the second sample
        Type: TestTypes; an enumeration value indicating the 1- or 2-sided
            nature of the test, use values GT_TEST, LT_TEST and NEQ_TEST defined
            in this module
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%.
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Confidence argument is not in the range (0, 1), OR the
            data sequence is less than 2 elements long for any of the samples
    
    Version 2.0.0.0
    """
    _CheckData2D(Data1, Data2)
    _CheckTestParameters(Type, Confidence)
    N1 = Data1.N
    N2 = Data2.N
    Temp = (N1 - 1) * Data1.FullVar + (N2 - 1) * Data2.FullVar
    Temp /= N1 + N2 - 2
    Temp *= (N1 + N2) / (N1 * N2)
    TestValue = (Data1.Mean - Data2.Mean) / math.sqrt(Temp)
    Model = MC.Student(Degree = N1 + N2 - 2)
    TestName = ' '.join(['Unpaired Student`s t-test at {:.1f}%'.format(
                                                            100 * Confidence),
                            'confidence on the samples` means.'])
    Result=_DoTest2D(Model, Data1, Data2, TestValue, Confidence, Type, TestName)
    del Model
    return Result

def paired_t_test(Data1: DC, Data2: DC, Type: TestTypes, *,
                    Confidence: float = 0.95, Bias: TReal = 0.0) -> TestResult:
    """
    Implementation of the paired Student`s t-test, comparing the samples` means.
    The samples`s lengths MUST be equal.
    
    Signature:
        Statistics1D, Statistics1D, TestTypes
            /, *, 0 < float < 1, int OR float/ -> TestResult
    
    Args:
        Data1: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the first sample
        Data2: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the second sample
        Type: TestTypes; an enumeration value indicating the 1- or 2-sided
            nature of the test, use values GT_TEST, LT_TEST and NEQ_TEST defined
            in this module
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%
        Bias: (keyword) int OR float; the expected difference between means,
            defaults to 0.0
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Confidence argument is not in the range (0, 1), OR the
            data sequence is less than 2 elements long for any of the samples,
            OR the data samples have unequal lengths
    
    Version 2.0.0.0
    """
    _CheckData2D(Data1, Data2)
    _CheckTestParameters(Type, Confidence)
    if Data1.N != Data2.N:
        raise UT_ValueError(Data1.N, '= {} - samples lengths'.format(Data2.N),
                                                                SkipFrames = 1)
    N = Data1.N
    Temp = [Data1.Values[Index] - Data2.Values[Index] for Index in range(N)]
    Data = DC(Temp)
    del Temp
    TestValue = (Data.Mean - Bias) * math.sqrt(N - 1) / Data.FullSigma
    Model = MC.Student(Degree = N - 1)
    TestName = ' '.join(['Paired Student`s t-test at {:.1f}%'.format(
                                                            100 * Confidence),
                            'confidence on the samples` means with the',
                                            f'expected difference = {Bias}.'])
    Result=_DoTest2D(Model, Data1, Data2, TestValue, Confidence, Type, TestName)
    del Data
    del Model
    return Result

def Welch_t_test(Data1: DC, Data2: DC, Type: TestTypes, *,
                                        Confidence: float = 0.95) -> TestResult:
    """
    Implementation of the Welch t-test, comparing the samples` means. This test
    is more reliable than the unpaired Student`s t-test when the samples`s
    variances differ by more than 2 times.
    
    Signature:
        Statistics1D, Statistics1D, TestTypes/, *, 0 < float < 1/ -> TestResult
    
    Args:
        Data1: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the first sample
        Data2: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the second sample
        Type: TestTypes; an enumeration value indicating the 1- or 2-sided
            nature of the test, use values GT_TEST, LT_TEST and NEQ_TEST defined
            in this module
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%.
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Confidence argument is not in the range (0, 1), OR the
            data sequence is less than 2 elements long for any of the samples
    
    Version 2.0.0.0
    """
    _CheckData2D(Data1, Data2)
    _CheckTestParameters(Type, Confidence)
    NormVar1 = Data1.FullVar / (Data1.N - 1)
    NormVar2 = Data2.FullVar / (Data2.N - 1)
    NormVarSum = NormVar1 + NormVar2
    Divident = math.pow(NormVarSum, 2)
    Divisor = math.pow(NormVar1, 2) / (Data1.N - 1)
    Divisor += math.pow(NormVar2, 2) / (Data2.N - 1)
    Degree = Divident / Divisor
    TestValue = (Data1.Mean - Data2.Mean) / math.sqrt(NormVarSum)
    Model = MC.Student(Degree = Degree)
    TestName = ' '.join(['Welch t-test at {:.1f}%'.format(100 * Confidence),
                            'confidence on the samples` means.'])
    Result=_DoTest2D(Model, Data1, Data2, TestValue, Confidence, Type, TestName)
    del Model
    return Result
    
def f_test(Data1: DC, Data2: DC, Type: TestTypes, *,
                    Confidence: float = 0.95, Delta: TReal = 1.0) -> TestResult:
    """
    Implementation of the f-test, comparing the samples` standard deviations.
    
    Signature:
        Statistics1D, Statistics1D, TestTypes
            /, *, 0 < float < 1, int > 0 OR float > 0/ -> TestResult
    
    Args:
        Data1: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the first sample
        Data2: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the second sample
        Type: TestTypes; an enumeration value indicating the 1- or 2-sided
            nature of the test, use values GT_TEST, LT_TEST and NEQ_TEST defined
            in this module
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%
        Delta: (keyword) int > 0 OR float > 0; the expected ratio of the true
            underlying population variances, defaults to 1.0
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Confidence argument is not in the range (0, 1), OR the
            data sequence is less than 2 elements long for any of the samples,
            OR the Delta parameter is not positive
    
    Version 2.0.0.0
    """
    _CheckData2D(Data1, Data2)
    _CheckTestParameters(Type, Confidence)
    if not isinstance(Delta, (int, float)):
        raise UT_TypeError(Delta, (int, float), SkipFrames = 1)
    if Delta <= 0:
        raise UT_ValueError(Delta, '> 0 - delta parameter', SkipFrames = 1)
    Correction = Data1.N * (Data2.N - 1) / (Data2.N * (Data1.N - 1))
    TestValue = Correction * Delta * Data1.FullVar / Data2.FullVar
    Model = MC.F_Distribution(Degree1 = Data1.N - 1, Degree2 = Data2.N - 1)
    CDF_Value = _GetCDF(Model, TestValue)
    CriticalValues = _GetBoundariesAsym(Model, Type, Confidence)
    TestName = ' '.join(['F-test at {:.1f}%'.format(100 * Confidence),
                            'confidence on the samples` variances with',
                                                        f'delta = {Delta}'])
    DataName = '{} vs {}'.format(Data1.Name, Data2.Name)
    ModelName = Model.Name
    Result = TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                CriticalValues)
    del Model
    return Result

def ANOVA_test(Data1: DC, Data2: DC, *, Confidence: float = 0.95) -> TestResult:
    """
    Implementation of the ANOVA F-test on the homoscedasticity of two samples.
    
    Signature:
        Statistics1D, Statistics1D/, *, 0 < float < 1/ -> TestResult
    
    Args:
        Data1: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the first sample
        Data2: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the second sample
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Confidence argument is not in the range (0, 1), OR the
            data sequence is less than 2 elements long for any of the samples
    
    Version 2.0.0.0
    """
    _CheckData2D(Data1, Data2)
    _CheckTestParameters(TestTypes.RIGHT, Confidence)
    N1 = Data1.N
    N2 = Data2.N
    Mean1 = Data1.Mean
    Mean2 = Data2.Mean
    TotalMean = (N1 * Mean1 + N2 * Mean2) / (N1 + N2)
    TestValue = N1 * math.pow(Mean1 - TotalMean, 2)
    TestValue += N2 * math.pow(Mean2 - TotalMean, 2)
    TestValue /= N1 * Data1.FullVar + N2 * Data2.FullVar
    TestValue *= (N1 + N2 - 2)
    Model = MC.F_Distribution(Degree1 = 1, Degree2 = N1 + N2 - 2)
    CDF_Value = _GetCDF(Model, TestValue)
    CritValue = Model.qf(Confidence)
    CriticalValues = (CritValue, CritValue)
    TestName = ' '.join(['ANOVA F-test at {:.1f}%'.format(100 * Confidence),
                            'confidence on the samples` homoscedasticity'])
    DataName = '{} vs {}'.format(Data1.Name, Data2.Name)
    ModelName = Model.Name
    Result = TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                CriticalValues)
    del Model
    return Result

def Levene_test(Data1: DC, Data2: DC, *, Confidence: float= 0.95) -> TestResult:
    """
    Implementation of the Levene test on the homoscedasticity of two samples.
    
    Signature:
        Statistics1D, Statistics1D/, *, 0 < float < 1/ -> TestResult
    
    Args:
        Data1: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the first sample
        Data2: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the second sample
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Confidence argument is not in the range (0, 1), OR the
            data sequence is less than 2 elements long for any of the samples
    
    Version 2.0.0.0
    """
    _CheckData2D(Data1, Data2)
    _CheckTestParameters(TestTypes.RIGHT, Confidence)
    N1 = Data1.N
    N2 = Data2.N
    Mean1 = Data1.Mean
    Mean2 = Data2.Mean
    MData1 = DC([abs(Value - Mean1) for Value in Data1.Values])
    MData2 = DC([abs(Value - Mean2) for Value in Data2.Values])
    Mean1 = MData1.Mean
    Mean2 = MData2.Mean
    TotalMean = (N1 * Mean1 + N2 * Mean2) / (N1 + N2)
    TestValue = N1 * math.pow(Mean1 - TotalMean, 2)
    TestValue += N2 * math.pow(Mean2 - TotalMean, 2)
    TestValue /= N1 * MData1.Var + N2 * MData2.Var
    TestValue *= (N1 + N2 - 2)
    Model = MC.F_Distribution(Degree1 = 1, Degree2 = N1 + N2 - 2)
    del MData1
    del MData2
    CDF_Value = _GetCDF(Model, TestValue)
    CritValue = Model.qf(Confidence)
    CriticalValues = (CritValue, CritValue)
    TestName = ' '.join(['Levene test at {:.1f}%'.format(100 * Confidence),
                            'confidence on the samples` homoscedasticity'])
    DataName = '{} vs {}'.format(Data1.Name, Data2.Name)
    ModelName = Model.Name
    Result = TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                CriticalValues)
    del Model
    return Result

def Brown_Forsythe_test(Data1: DC, Data2: DC, *,
                                        Confidence: float = 0.95) -> TestResult:
    """
    Implementation of the Brown-Forsythe test on the homoscedasticity of two
    samples.
    
    Signature:
        Statistics1D, Statistics1D, TestTypes/, *, 0 < float < 1/ -> TestResult
    
    Args:
        Data1: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the first sample
        Data2: Statistics1D; instance of, the sampled data stored in an instance
            of specialized statistical class - the second sample
        Confidence: (keyword) 0 < float < 1; the confidence level of test,
            defaults to 0.95, i.e. 95%
    
    Returns:
        TestResult: instance of the class (defined in this module), which can
            generate a human-readable report on the performed test
    
    Raises:
        UT_TypeError: either of the arguments is of the improper data type
        UT_ValueError: Confidence argument is not in the range (0, 1), OR the
            data sequence is less than 2 elements long for any of the samples
    
    Version 2.0.0.0
    """
    _CheckData2D(Data1, Data2)
    _CheckTestParameters(TestTypes.RIGHT, Confidence)
    N1 = Data1.N
    N2 = Data2.N
    Mean1 = Data1.Median
    Mean2 = Data2.Median
    MData1 = DC([abs(Value - Mean1) for Value in Data1.Values])
    MData2 = DC([abs(Value - Mean2) for Value in Data2.Values])
    Mean1 = MData1.Mean
    Mean2 = MData2.Mean
    TotalMean = (N1 * Mean1 + N2 * Mean2) / (N1 + N2)
    TestValue = N1 * math.pow(Mean1 - TotalMean, 2)
    TestValue += N2 * math.pow(Mean2 - TotalMean, 2)
    TestValue /= N1 * MData1.Var + N2 * MData2.Var
    TestValue *= (N1 + N2 - 2)
    Model = MC.F_Distribution(Degree1 = 1, Degree2 = N1 + N2 - 2)
    del MData1
    del MData2
    CDF_Value = _GetCDF(Model, TestValue)
    CritValue = Model.qf(Confidence)
    CriticalValues = (CritValue, CritValue)
    TestName = ' '.join(['Brown-Forsythe test at {:.1f}%'.format(
                                                            100 * Confidence),
                            'confidence on the samples` homoscedasticity'])
    DataName = '{} vs {}'.format(Data1.Name, Data2.Name)
    ModelName = Model.Name
    Result = TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                CriticalValues)
    del Model
    return Result