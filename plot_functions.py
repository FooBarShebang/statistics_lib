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
    Plot2Sets(Data, **kwargs)
        Statistics2D OR seq(Statistics1D OR seq(int OR float OR MeasuredValue))
            /, **dict(str -> type A)/ -> None
    PlotBlandAltman(Data, **kwargs)
        Statistics2D OR seq(Statistics1D OR seq(int OR float OR MeasuredValue))
                /, **dict(str -> type A)/ -> None
    PlotMany(*Data, **kwargs)
        *tuple(Statistics2D OR seq(Statistics1D OR seq(int OR float OR
            MeasuredValue)))/, **dict(str -> type A)/ -> None
"""

__version__= '1.0.0.0'
__date__ = '28-10-2026'
__status__ = 'Development'

#imports

#+ standard library

import sys
import os

from typing import Union, Optional

from collections.abc import Sequence

from math import sqrt

#+ 3rd party libraries

import matplotlib.pyplot as ppl

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.data_classes as dc
import statistics_lib.base_functions as bf

#globals

#+ types

TDataSet = Union[Sequence[dc.TNumber], dc.Statistics1D]

TDataSet2D = Union[Sequence[TDataSet], dc.Statistics2D]

#+ plot styles

REF_LINE_STYLE = {
    'marker' : 'none',
    'linestyle' : '-',
    'color' : 'k'
}

NO_LINE_STYLE = {
    'markersize' : 4.0,
    'linestyle' : 'none',
    'markeredgecolor' : 'k',
    'marker' : 'o'
}

ERROR_BARS_STYLE = {
    'ecolor' : 'k',
    'capsize' : 2.0
}

NO_LINE_ERRORS = {Key : Value for Key, Value in NO_LINE_STYLE.items()}
NO_LINE_ERRORS.update(ERROR_BARS_STYLE)

SINGLE_MARKER_STYLE = {Key : Value for Key, Value in NO_LINE_STYLE.items()}
SINGLE_MARKER_STYLE['markerfacecolor'] = 'b'

SINGLE_MARKER_ERRORS={Key : Value for Key, Value in SINGLE_MARKER_STYLE.items()}
SINGLE_MARKER_ERRORS.update(ERROR_BARS_STYLE)

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

#+ plotting / graphics functions

#++ 2 variables

#+++ helper function

def _Check2Dset(Data: TDataSet2D) -> tuple[Sequence[dc.TReal], ...]:
    """
    Helper function to check the validity of input for functions expecting 2
    equal 1D data sets. If the check is successful, X-values and errors, and
    Y-values and errors are extracted and returned.

    Signature:
        Statistics2D OR seq(Statistics1D OR seq(int OR float OR MeasuredValue)) 
            -> tuple(seq(int OR float), seq(int OR float), seq(int OR float),
                seq(int OR float))
    
    Signature:
        Statistics2D OR seq(Statistics1D OR seq(int OR float OR MeasuredValue))
            /, **dict(str -> type A)/ -> None
    
    Args:
        Data: Statistics2D OR seq(Statistics1D OR seq(int OR float
            OR MeasuredValue)); expected an instance of Statistics2D or
            2-element sequence of instances of Statistics1D or generic numeric
            sequences
    
    Returns:
        tuple(seq(int OR float), seq(int OR float), seq(int OR float),
            seq(int OR float)); 4 elements tuple of real numbers sequences in
            the order X-values, X-errors, Y-values, Y-errors
    
    Raises:
        UT_TypeError: unexpected type of the argument OR its elements
        UT_ValueError: unequal length of 1D datasets, OR not exactly 2 data sets
            are passed
    
    Version 1.0.0.0
    """
    if isinstance(Data, dc.Statistics2D):
        XValues = Data.X.Values
        XErrors = Data.X.Errors
        YValues = Data.Y.Values
        YErrors = Data.Y.Errors
    elif isinstance(Data, Sequence):
        if len(Data) == 2:
            if isinstance(Data[0], dc.Statistics1D):
                XValues = Data[0].Values
                XErrors = Data[0].Errors
            elif dc._CheckIfNumberSequence(Data[0]):
                XValues = bf._ExtractMeans(Data[0], DoCheck = False)
                XErrors = bf._ExtractErrors(Data[0], DoCheck = False)
            else:
                Error = dc.UT_TypeError(Data[0], (dc.Statistics1D, Sequence),
                                                                SkipFrames = 1)
                Error.appendMessage('- X data set is not generic numeric seq')
                raise Error
            if isinstance(Data[1], dc.Statistics1D):
                YValues = Data[1].Values
                YErrors = Data[1].Errors
            elif dc._CheckIfNumberSequence(Data[1]):
                YValues = bf._ExtractMeans(Data[1], DoCheck = False)
                YErrors = bf._ExtractErrors(Data[1], DoCheck = False)
            else:
                Error = dc.UT_TypeError(Data[1], (dc.Statistics1D, Sequence),
                                                                SkipFrames = 1)
                Error.appendMessage('- Y data set is not generic numeric seq')
                raise Error
            if len(XErrors) != len(YErrors):
                raise dc.UT_ValueError(len(XErrors),
                                    f'== {len(YErrors)} - unequal data sets',
                                                                SkipFrames = 1)
        else:
            raise dc.UT_ValueError(len(Data), '== 2 - number of data sets',
                                                                SkipFrames = 1)
    else:
        Error = dc.UT_TypeError(Data, (dc.Statistics2D, Sequence),
                                                                SkipFrames = 1)
        Error.appendMessage('- Data argument is not two 1D data sets')
        raise Error
    return (XValues, XErrors, YValues, YErrors)

def _ExtractTitles(Data: TDataSet2D
                                ) -> tuple[str | None, str | None, str | None]:
    """
    Helper function, tries to extract the X- and Y- axis labels from the passed
    data set, which is possible if the passed data is an instance of
    Statistics2D class, or a sequence containing, at least, one instance of
    Statistics1D class as X- or Y- or both variables. Plot title can be
    extracted from data only if it an instance of Statistics2D class, and its
    attribute Name is not None.

    Signature:
        Statistics2D OR seq(Statistics1D OR seq(int OR float OR MeasuredValue))
            -> tuple(str OR None, str OR None, str OR None)
    
    Args:
        Data: Statistics2D OR seq(Statistics1D OR seq(int OR float
            OR MeasuredValue)); expected an instance of Statistics2D or
            2-element sequence of instances of Statistics1D or generic numeric
            sequences

    Returns:
        tuple(str OR None, str OR None, str OR None); X-axis title, Y-axis title, plot title
    
    Version 1.0.0.0
    """
    _Title = None
    _XLabel = None
    _YLabel = None
    if isinstance(Data, dc.Statistics2D):
        _XLabel = Data.X.Name
        _YLabel = Data.Y.Name
        _Title = Data.Name
    else:
        if isinstance(Data[0], dc.Statistics1D):
            _XLabel = Data[0].Name
        if isinstance(Data[1], dc.Statistics1D):
            _YLabel = Data[1].Name
    return (_XLabel, _YLabel, _Title)

def _MakeTitles(Data: TDataSet2D, XTitle: str | None, YTitle: str | None,
                Title: str | None) -> tuple[str, str, str | None]:
    """
    Helper function, tries to extract the X- and Y- axis labels from the passed
    data set, which is possible if the passed data is an instance of
    Statistics2D class, or a sequence containing, at least, one instance of
    Statistics1D class as X- or Y- or both variables. If either X- or Y- title
    cannot be extracted, it is substituted by a generic name 'X variable' or
    'Y variable'. Plot title can be extracted from data only if it an instance
    of Statistics2D class, and its attribute Name is not None.

    If not None value is passed as XTitle, YTitle or Title argument, its value
    overwrites the extracted one.

    Signature:
        Statistics2D OR seq(Statistics1D OR seq(int OR float OR MeasuredValue)),
            str OR None, str OR None, str OR None
                -> tuple(str, str, str OR None)
    
    Args:
        Data: Statistics2D OR seq(Statistics1D OR seq(int OR float
            OR MeasuredValue)); expected an instance of Statistics2D or
            2-element sequence of instances of Statistics1D or generic numeric
            sequences
        XTitle: str OR None; if not None - overwrites the X-axis title extracted
            or automatically created
        YTitle: str OR None; if not None - overwrites the X-axis title extracted
            or automatically created
        Title: str OR None; if not None - overwrites the plot title extracted
            or automatically created
    
    Returns:
        tuple(str, str, str OR None); X-axis title, Y-axis title, plot title
    
    Version 1.0.0.0
    """
    _XLabel, _YLabel, _Title = _ExtractTitles(Data)
    if _XLabel is None:
        _XLabel = 'X variable'
    if _YLabel is None:
        _YLabel = 'Y variable'
    if not XTitle is None:
        _XLabel = str(XTitle)
    if not YTitle is None:
        _YLabel = str(YTitle)
    if not Title is None:
        _Title = str(Title)
    return (_XLabel, _YLabel, _Title)

#+++ actual plot functions

def Plot2Sets(Data: TDataSet2D, /, Slope: Optional[dc.TReal] = None,
                YIntercept: Optional[dc.TReal] = None,
                    VSplit: Optional[dc.TReal] = None,
                        ShowXErrors: bool = False, ShowYErrors: bool = False,
                            XTitle: Optional[str] = None,
                                YTitle: Optional[str] = None,
                                    Title: Optional[str] = None,
                                        Filename: Optional[str] = None) -> None:
    """
    Plots Y-variable against X-variable with markers without lines. Both
    variables can be passed as an instance of Statistics2D class, or as a
    2-element sequence of generic numeric sequences or instances of Statistics1D
    class. When possible, X- and Y-axis titles are extracted from the labels
    (Name attribute) of the passed data sets, as well as the plot title,
    otherwise generic titles are created automatically. X-, Y-axis and plot
    titles can be specified explicitely. X- and / or Y-erorbars can be requested
    as well as sloped (or horizontal) and / or vertical reference line.

    If filename is provided, the plot is also saved using the respective path,
    relative to the current working directory.

    Signature:
        Statistics2D OR seq(Statistics1D OR seq(int OR float OR MeasuredValue))
            /, **dict(str -> type A)/ -> None
    
    Args:
        Data: Statistics2D OR seq(Statistics1D OR seq(int OR float
            OR MeasuredValue)); expected an instance of Statistics2D or
            2-element sequence of instances of Statistics1D or generic numeric
            sequences
        kwargs: **dict(str -> type A); only allowed settings are
            Slope: int OR float OR None; in not None - adds a sloped reference
                line, can be used with or without YIntercept as y(x) = a * x + b
            YIntercept: int OR float OR None; if not None - adds a vertical
                offset to the sloped reference line, if used without Slope -
                creates a horizontal reference line y(x) = b
            VSplit: int OR float OR None; if not None - adds a vertical
                reference line at x = VSplit
            ShowXErrors: bool; if True - adds X-errorbars to the markers
            ShowYErrors: bool; if True - adds Y-errorbars to the markers
            XTitle: str OR None; if not None - overwrites the X-axis title
                extracted from data or automatically created
            YTitle: str OR None; if not None - overwrites the X-axis title
                extracted from data or automatically created
            Title: str OR None; if not None - overwrites the plot title
                extracted from data or automatically created
            Filename: str OR None; if not None - saves the figure into a file
    
    Raises:
        UT_TypeError: unexpected type of the argument OR its elements
        UT_ValueError: unequal length of 1D datasets, OR not exactly 2 data sets
            are passed
    
    Version 1.0.0.0
    """
    XValues, XErrors, YValues, YErrors = _Check2Dset(Data)
    _XTitle, _YTitle, _Title = _MakeTitles(Data, XTitle, YTitle, Title)
    fig, ax = ppl.subplots()
    if ShowYErrors and ShowXErrors:
        ax.errorbar(XValues, YValues, yerr = YErrors, xerr = XErrors,
                                                    **SINGLE_MARKER_ERRORS)
    elif ShowYErrors:
        ax.errorbar(XValues, YValues, yerr = YErrors, **SINGLE_MARKER_ERRORS)
    elif ShowXErrors:
        ax.errorbar(XValues, YValues, xerr = XErrors, **SINGLE_MARKER_ERRORS)
    else:
        ax.plot(XValues, YValues, **SINGLE_MARKER_STYLE)
    if isinstance(VSplit, (int, float)):
        XData = [VSplit, VSplit]
        YData = [min(YValues), max(YValues)]
        ax.plot(XData, YData, **REF_LINE_STYLE)
    bCond1 = isinstance(Slope, (int, float))
    bCond2 = isinstance(YIntercept, (int, float))
    if bCond1 or bCond2:
        XData = [min(XValues), max(XValues)]
        if bCond1:
            YData = [Slope * XData[0], Slope * XData[1]]
        else:
            YData = [0, 0]
        if bCond2:
            YData = [YData[0] + YIntercept, YData[1] + YIntercept]
        ax.plot(XData, YData, **REF_LINE_STYLE)
    ax.set_xlabel(_XTitle)
    ax.set_ylabel(_YTitle)
    if _Title is None:
        _Title = f'Direct comparison of {_YTitle} to {_XTitle}'
    ax.set_title(_Title)
    if not Filename is None:
        try:
            fig.savefig(Filename)
            print(f'Figure is saved as {Filename}')
        except Exception as err:
            print(f'Couldn`t save the figure as {Filename}')
            print(f'Exception raised {err.__class__.__name__}: {str(err)}')
    ppl.show()

def PlotBlandAltman(Data: TDataSet2D, /, Slope: Optional[dc.TReal] = None,
                YIntercept: Optional[dc.TReal] = None,
                    VSplit: Optional[dc.TReal] = None,
                        ShowXErrors: bool = False, ShowYErrors: bool = False,
                            XTitle: Optional[str] = None,
                                YTitle: Optional[str] = None,
                                    Title: Optional[str] = None,
                                        Filename: Optional[str] = None) -> None:
    """
    Plots Balnd-Altman (difference vs mean) of Y-variable against X-variable
    with markers without lines. Both variables can be passed as an instance of
    Statistics2D class, or as a 2-element sequence of generic numeric sequences
    or instances of Statistics1D class. When possible, X- and Y-vars titles are
    extracted from the labels (Name attribute) of the passed data sets, as well
    as the plot title, otherwise generic titles are created automatically. X-,
    Y-vars and plot titles can be specified explicitely. X- and / or Y-erorbars
    can be requested as well as sloped (or horizontal) and / or vertical
    reference line.

    If filename is provided, the plot is also saved using the respective path,
    relative to the current working directory.

    Signature:
        Statistics2D OR seq(Statistics1D OR seq(int OR float OR MeasuredValue))
            /, **dict(str -> type A)/ -> None
    
    Args:
        Data: Statistics2D OR seq(Statistics1D OR seq(int OR float
            OR MeasuredValue)); expected an instance of Statistics2D or
            2-element sequence of instances of Statistics1D or generic numeric
            sequences
        kwargs: **dict(str -> type A); only allowed settings are
            Slope: int OR float OR None; in not None - adds a sloped reference
                line, can be used with or without YIntercept as y(x) = a * x + b
            YIntercept: int OR float OR None; if not None - adds a vertical
                offset to the sloped reference line, if used without Slope -
                creates a horizontal reference line y(x) = b
            VSplit: int OR float OR None; if not None - adds a vertical
                reference line at x = VSplit
            ShowXErrors: bool; if True - adds X-errorbars to the markers
            ShowYErrors: bool; if True - adds Y-errorbars to the markers
            XTitle: str OR None; if not None - overwrites the X-variable title
                extracted from data or automatically created
            YTitle: str OR None; if not None - overwrites the X-axis title
                extracted from data or automatically created
            Title: str OR None; if not None - overwrites the plot title
                extracted from data or automatically created
            Filename: str OR None; if not None - saves the figure into a file
    
    Raises:
        UT_TypeError: unexpected type of the argument OR its elements
        UT_ValueError: unequal length of 1D datasets, OR not exactly 2 data sets
            are passed
    
    Version 1.0.0.0
    """
    XValues, XErrors, YValues, YErrors = _Check2Dset(Data)
    XData = [0.5 * (x + y) for x, y in zip(XValues, YValues)]
    YData = [y - x for x, y in zip(XValues, YValues)]
    Errors = [sqrt(xe**2 + ye**2) for xe, ye in zip(XErrors, YErrors)]
    _XTitle, _YTitle, _Title = _MakeTitles(Data, XTitle, YTitle, Title)
    fig, ax = ppl.subplots()
    if ShowYErrors and ShowXErrors:
        ax.errorbar(XData, YData, yerr = Errors, xerr = XErrors,
                                                    **SINGLE_MARKER_ERRORS)
    elif ShowYErrors:
        ax.errorbar(XData, YData, yerr = Errors, **SINGLE_MARKER_ERRORS)
    elif ShowXErrors:
        ax.errorbar(XData, YData, xerr = Errors, **SINGLE_MARKER_ERRORS)
    else:
        ax.plot(XData, YData, **SINGLE_MARKER_STYLE)
    if isinstance(VSplit, (int, float)):
        _XData = [VSplit, VSplit]
        _YData = [min(YData), max(YData)]
        ax.plot(_XData, _YData, **REF_LINE_STYLE)
    bCond1 = isinstance(Slope, (int, float))
    bCond2 = isinstance(YIntercept, (int, float))
    if bCond1 or bCond2:
        _XData = [min(XData), max(XData)]
        if bCond1:
            _YData = [Slope * _XData[0], Slope * _XData[1]]
        else:
            _YData = [0, 0]
        if bCond2:
            _YData = [_YData[0] + YIntercept, _YData[1] + YIntercept]
        ax.plot(_XData, _YData, **REF_LINE_STYLE)
    ax.set_xlabel(f'mean of {_XTitle} and {_YTitle}')
    ax.set_ylabel(f'Difference of {_YTitle} and {_XTitle}')
    if _Title is None:
        _Title = f'Bland-Altman comparison of {_YTitle} to {_XTitle}'
    ax.set_title(_Title)
    if not Filename is None:
        try:
            fig.savefig(Filename)
            print(f'Figure is saved as {Filename}')
        except Exception as err:
            print(f'Couldn`t save the figure as {Filename}')
            print(f'Exception raised {err.__class__.__name__}: {str(err)}')
    ppl.show()

#++ multiple variables

#+++ actual plot functions

def PlotMany(*Data: *tuple[TDataSet2D], Slope: Optional[dc.TReal] = None,
                YIntercept: Optional[dc.TReal] = None,
                    VSplit: Optional[dc.TReal] = None,
                        ShowXErrors: bool = False, ShowYErrors: bool = False,
                            XTitle: Optional[str] = None,
                                YTitle: Optional[str] = None,
                                    Title: Optional[str] = None,
                                        Filename: Optional[str] = None,
                                            Labels: Sequence[str] = []) -> None:
    """
    Plots multiple Y-variables against X-variables with markers without lines.
    In each set the both variables can be passed as an instance of Statistics2D
    class, or as a 2-element sequence of generic numeric sequences or instances
    of Statistics1D class. When possible, X- and Y-axis titles are extracted
    from the labels (Name attribute) of the passed data sets, as well as the
    plot title, otherwise generic titles are created automatically. X-, Y-axis
    and plot titles can be specified explicitely. X- and / or Y-erorbars can be
    requested as well as sloped (or horizontal) and/or vertical reference line.

    If filename is provided, the plot is also saved using the respective path,
    relative to the current working directory.

    Signature:
        *tuple(Statistics2D OR seq(Statistics1D OR seq(int OR float OR
            MeasuredValue))) /, **dict(str -> type A)/ -> None
    
    Args:
        Data: *tuple(Statistics2D OR seq(Statistics1D OR seq(int OR float
            OR MeasuredValue))); two or more data sets, expected an instance of
            Statistics2D or 2-element sequence of instances of Statistics1D or
            generic numeric sequences for each element
        kwargs: **dict(str -> type A); only allowed settings are
            Slope: int OR float OR None; in not None - adds a sloped reference
                line, can be used with or without YIntercept as y(x) = a * x + b
            YIntercept: int OR float OR None; if not None - adds a vertical
                offset to the sloped reference line, if used without Slope -
                creates a horizontal reference line y(x) = b
            VSplit: int OR float OR None; if not None - adds a vertical
                reference line at x = VSplit
            ShowXErrors: bool; if True - adds X-errorbars to the markers
            ShowYErrors: bool; if True - adds Y-errorbars to the markers
            XTitle: str OR None; if not None - overwrites the X-axis title
                extracted from data or automatically created
            YTitle: str OR None; if not None - overwrites the X-axis title
                extracted from data or automatically created
            Title: str OR None; if not None - overwrites the plot title
                extracted from data or automatically created
            Filename: str OR None; if not None - saves the figure into a file
            Labels: seq(str OR None); optional labels / names of the deatasets,
                applied in not gready manner, None values are ignored, missing
                or superficial entires are ignored, overwrites the data set
                names extracted from the arguments or auto-generated ones
    
    Raises:
        UT_TypeError: unexpected type of the arguments OR their elements
        UT_ValueError: unequal length of 1D datasets, OR not exactly 2 data sets
            are passed in any dataset, OR less than 2 x-y data sets are passed 
    
    Version 1.0.0.0
    """
    DataX = []
    DataY = []
    ErrorsX = []
    ErrorsY = []
    _Labels = []
    TitleX = None
    TitleY = None
    TitleP = None
    if len(Data) < 2:
        raise dc.UT_ValueError(len(Data), ' >=2 - number of x-y datasets')
    for Index, DataSet in enumerate(Data):
        try:
            XValues, XErrors, YValues, YErrors = _Check2Dset(DataSet)
        except (dc.UT_ValueError, dc.UT_TypeError) as err:
            err.appendMessage(f'- datased {DataSet} at position {Index}')
        DataX.append(XValues)
        DataY.append(YValues)
        ErrorsX.append(XErrors)
        ErrorsY.append(YErrors)
        _XTitle, _YTitle, _Title=_ExtractTitles(DataSet)
        print(_XTitle, _YTitle, _Title)
        if (TitleX is None) and (not _XTitle is None):
            TitleX = _XTitle
            print('!', TitleX)
        if (TitleY is None) and (not _YTitle is None):
            TitleY = _YTitle
        if not _Title is None:
            _Labels.append(_Title)
            if TitleP is None:
                TitleP = _Title
        elif not _YTitle is None:
            _Labels.append(_YTitle)
        else:
            _Labels.append(f'Data set {Index + 1}')
    for Index, Label in enumerate(Labels):
        if (not Label is None) and Index < len(_Labels):
            _Labels[Index] = str(Label)
    if not XTitle is None:
        TitleX = str(XTitle)
    elif TitleX is None:
        TitleX = 'X variable'
    if not YTitle is None:
        TitleY = str(YTitle)
    elif TitleY is None:
        TitleY = 'Y variable'
    if not Title is None:
        TitleP = str(Title)
    elif TitleP is None:
        TitleP = f'Direct comparison of {TitleY} to {TitleX}'
    fig, ax = ppl.subplots()
    for Index, XValues in enumerate(DataX):
        YValues = DataY[Index]
        XErrors = ErrorsX[Index]
        YErrors = ErrorsY[Index]
        if ShowYErrors and ShowXErrors:
            ax.errorbar(XValues, YValues, yerr = YErrors, xerr = XErrors,
                                    label = _Labels[Index], **NO_LINE_ERRORS)
        elif ShowYErrors:
            ax.errorbar(XValues, YValues, yerr = YErrors,
                                    label = _Labels[Index], **NO_LINE_ERRORS)
        elif ShowXErrors:
            ax.errorbar(XValues, YValues, xerr = XErrors,
                                    label = _Labels[Index], **NO_LINE_ERRORS)
        else:
            ax.plot(XValues, YValues, label = _Labels[Index], **NO_LINE_STYLE)
    if isinstance(VSplit, (int, float)):
        XData = [VSplit, VSplit]
        YData = [min(min(YValues) for YValues in DataY),
                    max(max(YValues) for YValues in DataY)]
        ax.plot(XData, YData, **REF_LINE_STYLE)
    bCond1 = isinstance(Slope, (int, float))
    bCond2 = isinstance(YIntercept, (int, float))
    if bCond1 or bCond2:
        XData = [min(min(XValues) for XValues in DataX),
                            max(max(XValues) for XValues in DataX)]
        if bCond1:
            YData = [Slope * XData[0], Slope * XData[1]]
        else:
            YData = [0, 0]
        if bCond2:
            YData = [YData[0] + YIntercept, YData[1] + YIntercept]
        ax.plot(XData, YData, **REF_LINE_STYLE)
    ax.set_xlabel(TitleX)
    ax.set_ylabel(TitleY)
    ax.set_title(TitleP)
    ppl.legend()
    if not Filename is None:
        try:
            fig.savefig(Filename)
            print(f'Figure is saved as {Filename}')
        except Exception as err:
            print(f'Couldn`t save the figure as {Filename}')
            print(f'Exception raised {err.__class__.__name__}: {str(err)}')
    ppl.show()