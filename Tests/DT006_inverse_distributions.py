#usr/bin/python3
"""
Module statistics_lib.Tests.DT006_inverse_distributions

Implements the demonstration test TEST-D-600, verifying the requirements
REQ-FUN-607 and REQ-FUN-608.
"""

__version__= '1.0.0.0'
__date__ = '28-04-2022'
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

import statistics_lib.inverse_distributions as dc

from statistics_lib.data_classes import Statistics1D

#globals

FILE_PATH = os.path.join(TEST_FOLDER, 'DT006_test_results.txt')

TEST_CLASSES = (dc.InverseGaussian, dc.InverseGamma, dc.InverseChiSquared,
                dc.ScaledInverseChiSquared, dc.Cauchy, dc.Levy)

PARAMETERS = ((1.5, 2.5), (2.5, 1.5), (5,), (5.5, 2.0), (1.5, 1.5), (1.5, 0.5),)

N_POINTS = 10000

N_BINS = 20

#functions

#execution entry point

if __name__ == '__main__':
    #preparation
    with open(FILE_PATH, 'wt') as fFile:
        strLine = 'DT006 test results on {}'.format(datetime.date.today())
        print(strLine)
        fFile.write(strLine)
        fFile.write('\n')
        strLine = 'N_Points = {}, N_Bins = {}'.format(N_POINTS, N_BINS)
        print(strLine)
        fFile.write(strLine)
        fFile.write('\n')
        for Index, TestClass in enumerate(TEST_CLASSES):
            Parameters = PARAMETERS[Index]
            if not (Parameters is None):
                objTest = TestClass(*Parameters)
            else:
                objTest = TestClass()
            strLine = 'Testing {}'.format(objTest.Name)
            print(strLine)
            fFile.write(strLine)
            fFile.write('\n')
            strLine = 'Bin\tRnd\tHist\tPDF'
            print(strLine)
            fFile.write(strLine)
            fFile.write('\n')
            Q3 = objTest.Q3
            Q1 = objTest.Q1
            IQD = 0.5 * (Q3 - Q1)
            MinAcc = Q1 - IQD
            MaxAcc = Q3 + IQD
            Generated = 0
            lstRandom = list()
            for _ in range(N_POINTS):
                Item = objTest.random()
                if (MinAcc <= Item) and (MaxAcc >= Item):
                    lstRandom.append(Item)
            objStat1D = Statistics1D(lstRandom)
            tupHistorgam = objStat1D.getHistogram(NBins = N_BINS)
            del objStat1D
            tupBins = tuple(Item[0] for Item in tupHistorgam)
            tupRnd = tuple(Item[1] / N_POINTS for Item in tupHistorgam)
            Min = tupBins[0]
            Max = tupBins[-1]
            S = (Max - Min) / (N_BINS - 1)
            tupHistorgam = objTest.getHistogram(Min, Max, N_BINS)
            tupHist = tuple(Item[1] for Item in tupHistorgam)
            for Index in range(N_BINS):
                Center = tupBins[Index]
                Left = Center - 0.5 * S
                Right = Center + 0.5 * S
                PDF = (objTest.pdf(Left) + objTest.pdf(Center)
                                                + objTest.pdf(Right)) / 3
                strLine = '\t'.join([str(Center), str(tupRnd[Index]),
                                            str(tupHist[Index]), str(PDF * S)])
                print(strLine)
                fFile.write(strLine)
                fFile.write('\n')