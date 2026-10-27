#usr/bin/python3
"""
Module statistics_lib.plot_functions

Implements functions automating data distribution plotting and analysis.

Functions:
    GetCorrelationMatrix
        *tuple(seq(int OR float OR MeasuredValue) OR Statistics1D, ...)
            -> tuple(list(list(int OR float)), str)
    
    GetCovarianceMatrix
            *tuple(seq(int OR float OR MeasuredValue) OR Statistics1D, ...)
                -> tuple(list(list(int OR float)), str)
"""

__version__= '1.0.0.0'
__date__ = '27-10-2026'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os

from typing import Union

from collections.abc import Sequence

#+ 3rd party libraries

import matplotlib

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.data_classes as dc

#globals

#+ types

TDataSet = Union[Sequence[dc.TNumber], dc.Statistics1D]

#functions

#+ cross-correlation, etc.

def GetCorrelationMatrix(*Data: *tuple[TDataSet, ...]
                                        ) -> tuple[list[list[dc.TReal]], str]:
    """
    Calculates correlation matrix of two or more data sets of equal length.
    Above diagonal - Pearson`s r correlation coefficients, below - Spearman
    rho correlation coefficients.

    Signature:
        *tuple(seq(int OR float OR MeasuredValue) OR Statistics1D, ...)
            -> tuple(list(list(int OR float)), str)
    
    Args:
        Data: *tuple(seq(int OR float OR MeasuredValue) OR Statistics1D, ...);
            two or more generic numeric sequences, including instances of
            Statistics1D class, of the same length
    
    Returns:
        tuple(list(list(int OR float)), str); first element is N x N correlation
            matrix in the form of N lists of lists of N numbers for N passed
            data sets, second element is string summary with TSV table
            representation of the matrix and variables names (if known)
    
    Raises:
        UT_TypeError: either of the passed arguments is of unexpected data type
        UT_ValueError: less than 2 data sets are passed OR any of the data sets
            is of unequal length
    
    Version 1.0.0.0
    """
    NSets = len(Data)
    if NSets < 2:
        raise dc.UT_TypeError(NSets, '>= 2 - number of data sets')
    Matrix = [[1 for _ in range(NSets)] for _ in range(NSets)]
    Names = list()
    for IndexX in range(NSets):
        DataX = Data[IndexX]
        if isinstance(DataX, dc.Statistics1D) and (not DataX.Name is None):
            Names.append(DataX.Name)
        else:
            Names.append(f'Variable_{IndexX}')
        for IndexY in range(IndexX + 1, NSets):
            Comparator = dc.Statistics2D(DataX, Data[IndexY])
            r = Comparator.Pearson
            rho = Comparator.Spearman
            del Comparator
            Matrix[IndexX][IndexY] = r
            Matrix[IndexY][IndexX] = rho
    Summary = '\n'.join([
        'Correlation matrix report.',
        f'N points = {len(Data[0])}, N sets = {NSets}.',
        'Above diagonal - Pearson`s r, below - Spearman \u03C1.',
        '=====================================================',
        '\t'.join(['#', '\t'.join(Names)]),
        '\n'.join(['\t'.join([Name, '\t'.join(f'{Value: .5f}'
                                    for Value in Matrix[Index])])
                                        for Index, Name in enumerate(Names)]),
        '====================================================='
    ])
    return (Matrix, Summary)

def GetCovarianceMatrix(*Data: *tuple[TDataSet, ...]
                                        ) -> tuple[list[list[dc.TReal]], str]:
    """
    Calculates covariance matrix of two or more data sets of equal length.

    Signature:
        *tuple(seq(int OR float OR MeasuredValue) OR Statistics1D, ...)
            -> tuple(list(list(int OR float)), str)
    
    Args:
        Data: *tuple(seq(int OR float OR MeasuredValue) OR Statistics1D, ...);
            two or more generic numeric sequences, including instances of
            Statistics1D class, of the same length
    
    Returns:
        tuple(list(list(int OR float)), str); first element is N x N covariance
            matrix in the form of N lists of lists of N numbers for N passed
            data sets, second element is string summary with TSV table
            representation of the matrix and variables names (if known)
    
    Raises:
        UT_TypeError: either of the passed arguments is of unexpected data type
        UT_ValueError: less than 2 data sets are passed OR any of the data sets
            is of unequal length
    
    Version 1.0.0.0
    """
    NSets = len(Data)
    if NSets < 2:
        raise dc.UT_TypeError(NSets, '>= 2 - number of data sets')
    Matrix = [[0 for _ in range(NSets)] for _ in range(NSets)]
    Names = list()
    for IndexX in range(NSets):
        DataX = Data[IndexX]
        Var = DataX.Var
        Matrix[IndexX][IndexX] = Var
        if isinstance(DataX, dc.Statistics1D) and (not DataX.Name is None):
            Names.append(DataX.Name)
        else:
            Names.append(f'Variable_{IndexX}')
        for IndexY in range(IndexX + 1, NSets):
            Comparator = dc.Statistics2D(DataX, Data[IndexY])
            Cov = Comparator.Cov
            del Comparator
            Matrix[IndexX][IndexY] = Cov
            Matrix[IndexY][IndexX] = Cov
    Summary = '\n'.join([
        'Covariance matrix report.',
        f'N points = {len(Data[0])}, N sets = {NSets}.',
        'Above diagonal - Pearson`s r, below - Spearman \u03C1.',
        '=====================================================',
        '\t'.join(['#', '\t'.join(Names)]),
        '\n'.join(['\t'.join([Name, '\t'.join(f'{Value: .5E}'
                                    for Value in Matrix[Index])])
                                        for Index, Name in enumerate(Names)]),
        '====================================================='
    ])
    return (Matrix, Summary)