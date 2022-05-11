#usr/bin/python3
"""
Module statistics_lib.Tests.DT007_stat_tests

Implements the demonstration test TEST-D-700, verifying the requirements
REQ-FUN-7B0 and REQ-FUN-7B1.
"""

__version__= '1.0.0.0'
__date__ = '11-05-2022'
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

from statistics_lib.distribution_classes import Gaussian

#globals

FILE_PATH = os.path.join(TEST_FOLDER, 'DT007_test_results.txt')

#execution entry point

if __name__ == '__main__':
    with open(FILE_PATH, 'wt') as fFile:
        #just demonstration of the basic functionality of the report class
        TestName = ' '.join(['Z-test at 90% confidence on sample`s mean vs',
                                    'population mean = 1.2 and sigma = 0.3'])
        DataName = 'Some test data'
        ModelName = 'Z_Distribution()'
        CritValues = (-1.65, 1.65) #2-sided
        TestValue = 1.42
        CDF_Value = 0.9222
        objTest = st.TestResult(TestName, DataName, ModelName, TestValue,
                                                        CDF_Value, CritValues)
        print(objTest.Report, '\n')
        fFile.write(objTest.Report)
        fFile.write('\n\n')
        del objTest
        CritValues = (None, 1.28) #1-sided right-tailed
        objTest = st.TestResult(TestName, DataName, ModelName, TestValue,
                                                        CDF_Value, CritValues)
        print(objTest.Report, '\n')
        fFile.write(objTest.Report)
        fFile.write('\n\n')
        del objTest
        CritValues = (-1.28, None) #1-sided left-tailed
        objTest = st.TestResult(TestName, DataName, ModelName, TestValue,
                                                        CDF_Value, CritValues)
        print(objTest.Report, '\n')
        fFile.write(objTest.Report)
        fFile.write('\n\n')
        del objTest
        TestName = 'F-test at 90% confidence on samples` variances equality'
        ModelName = 'F_Distribution(Degree1 = 10, Degree2 = 15)'
        CritValues = (1.28, 1.28) #1-sided right-tailed - special
        objTest = st.TestResult(TestName, DataName, ModelName, TestValue,
                                                        CDF_Value, CritValues)
        print(objTest.Report, '\n')
        fFile.write(objTest.Report)
        fFile.write('\n\n')
        del objTest
        objGenerator1 = Gaussian(1.5, 0.5)
        objGenerator2 = Gaussian(2.5, 0.3)
        objData1 = Statistics1D([objGenerator1.random() for _ in range(15)])
        objData1.Name = 'test set 1'
        objData2 = Statistics1D([objGenerator2.random() for _ in range(15)])
        objData2.Name = 'test set 2'
        print(objData1.Summary, '\n')
        fFile.write(objData1.Summary)
        fFile.write('\n\n')
        print(objData2.Summary, '\n')
        fFile.write(objData2.Summary)
        fFile.write('\n\n')
        objTest = st.z_test(objData1, 1.5, 0.5, st.NEQ_TEST)
        print(objTest.Report, '\n')
        fFile.write(objTest.Report)
        fFile.write('\n\n')
        del objTest
        objTest = st.t_test(objData1, 1.0, st.GT_TEST)
        print(objTest.Report, '\n')
        fFile.write(objTest.Report)
        fFile.write('\n\n')
        del objTest
        objTest = st.chi_squared_test(objData1, 0.6, st.LT_TEST)
        print(objTest.Report, '\n')
        fFile.write(objTest.Report)
        fFile.write('\n\n')
        del objTest