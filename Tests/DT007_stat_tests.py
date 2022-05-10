#usr/bin/python3
"""
Module statistics_lib.Tests.DT007_stat_tests

Implements the demonstration test TEST-D-700, verifying the requirements
REQ-FUN-7B0 and REQ-FUN-7B1.
"""

__version__= '1.0.0.0'
__date__ = '10-05-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import datetime

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
TEST_FOLDER = os.path.dirname(MODULE_PATH)
LIB_FOLDER = os.path.dirname(TEST_FOLDER)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.stat_tests as st

from statistics_lib.data_classes import Statistics1D

#globals

FILE_PATH = os.path.join(TEST_FOLDER, 'DT007_test_results.txt')

#execution entry point

if __name__ == '__main__':
    #just demonstration of the basic functionality of the report class
    TestName = ' '.join(['Z-test at 90% confidence on sample`s mean vs',
                                    'population mean = 1.2 and sigma = 0.3'])
    DataName = 'Some test data'
    ModelName = 'Z_Distribution()'
    CritValues = (-1.65, 1.65) #2-sided
    TestValue = 1.42
    CDF_Value = 0.9222
    objTest = st.TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                    CritValues)
    print(objTest.Report, '\n')
    del objTest
    CritValues = (None, 1.28) #1-sided right-tailed
    objTest = st.TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                    CritValues)
    print(objTest.Report, '\n')
    del objTest
    CritValues = (-1.28, None) #1-sided left-tailed
    objTest = st.TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                    CritValues)
    print(objTest.Report, '\n')
    del objTest
    TestName = 'F-test at 90% confidence on samples` variances equality'
    ModelName = 'F_Distribution(Degree1 = 10, Degree2 = 15)'
    CritValues = (1.28, 1.28) #1-sided right-tailed - special
    objTest = st.TestResult(TestName, DataName, ModelName, TestValue, CDF_Value,
                                                                    CritValues)
    print(objTest.Report, '\n')
    del objTest