#usr/bin/python3
"""
Module statistics_lib.Tests.DT003_data_classes

Implements the demonstration test TEST-D-300, verifying the requirements
REQ-FUN-315 and REQ-FUN-324.
"""

__version__= '1.0.0.0'
__date__ = '08-03-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import random

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from statistics_lib.data_classes import Statistics1D, Statistics2D
from phyqus_lib.base_classes import MeasuredValue

if __name__ == '__main__':
    #preparation
    DataX = list()
    DataY = list()
    for _ in range(random.randrange(10, 100)):
        Temp = random.random()
        if Temp >= 0.5:
            Mean = random.uniform(-10.0, 10.0)
        else:
            Mean = random.randint(-100, 100)
        Temp = random.random()
        if Temp >= 0.6:
            DataX.append(MeasuredValue(Mean, random.random()))
        else:
            DataX.append(Mean)
        Temp = random.random()
        if Temp >= 0.5:
            Mean = random.uniform(-10.0, 10.0)
        else:
            Mean = random.randint(-100, 100)
        Temp = random.random()
        if Temp >= 0.6:
            DataY.append(MeasuredValue(Mean, random.random()))
        else:
            DataY.append(Mean)
    #1D statistics summary test
    print('Statistics1D - no name')
    objTest = Statistics1D(DataX)
    print(objTest.Summary)
    input('Press Enter')
    print('Statistics1D - assigned name test_X')
    objTest.Name = 'test_X'
    print(objTest.Summary)
    input('Press Enter')
    print('Statistics1D - check values')
    print('Name:', objTest.Name)
    print('N:', objTest.N)
    print('Mean:', objTest.Mean)
    print('Median:', objTest.Median)
    print('Q1:', objTest.Q1)
    print('Q3:', objTest.Q3)
    print('Min:', objTest.Min)
    print('Max:', objTest.Max)
    print('Var:', objTest.Var)
    print('FullVar:', objTest.FullVar)
    print('Skew:', objTest.Skew)
    print('Kurt:', objTest.Kurt)
    input('Press Enter')
    del objTest
    #2D statistics summary test
    print('Statistics2D - no names')
    objTest = Statistics2D(DataX, DataY)
    print(objTest.Summary)
    input('Press Enter')
    print('Statistics2D - assigned names')
    objTest.Name = 'test_paired'
    objTest.X.Name = 'test_X'
    objTest.Y.Name = 'test_Y'
    print(objTest.Summary)
    input('Press Enter')
    print('Statistics2D - check values')
    print('Name:', objTest.Name)
    print('Cov:', objTest.N)
    print('Pearson:', objTest.Pearson)
    print('Spearman:', objTest.Spearman)
    print('Kendall:', objTest.Kendall)
    print('Check X data properties')
    print(objTest.X.Summary)
    print('Check Y data properties')
    print(objTest.Y.Summary)
    print('Test is done!')