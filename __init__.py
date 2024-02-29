#!/usr/bin/python3
"""
Library statistics_lib

Implements a basic statistics on sequences of not only real numbers, but also
the 'real life measurements', i.e. 2-tuple values of the most probale / mean
value and asssociated uncertainty / standard error.

Modules:
    base_functions: Implements functions calculating the statistical properties
        of 1D or 2D data set related to the (cross-) moments of the sample data
        distribution. These functions accept a generic sequence of a mixed
        integers, floating point number values and instances of a class
        implementing 'measurements with uncertainty'
    ordered_functions: Implements functions calculating the statistical
        properties of 1D or 2D data set related to the shape of the sample data
        distribution. These functions accept a generic sequence of a mixed
        integers, floating point number values and instances of a class
        implementing 'measurements with uncertainty'.
    data_classes: Implements classes for storing (encapsulation) of 1D and 2D
        data sets as the (paired) sequence(s) of real numbers (integers and / or
        floating point numbers) and / or measurements with uncertainty, which
        are treated as the entire population. The statistical properties of the
        population distribution are calculated and returned on demand.
    distribution_classes: Provides classes implementing a number of commonly
        used discrete and continuous distributions. All classes have properties
        returning the basic statistical properties of the distribution: mean,
        median, the first and the third quartile, variance and standard
        deviation, skewness and excess kurtosis. They also have methods to
        calculate PDF / PMF and CDF for a given value, QF and a generic k-th of
        m quantile, with 0 < k < m, as well as a histogram of the distribution
        within specific bounds and with the specified number of bins. The
        parameters of a distribution are defined during instantiation, and they
        can be changed later via setter properties.
    inverse_distributions: Provides classes implementing a number of inverse and
        ratio distributions. All classes have properties returning the basic
        statistical properties of the distribution: mean, median, the first and
        the third quartile, variance and standard deviation, skewness and excess
        kurtosis. They also have methods to calculate PDF / PMF and CDF for a
        given value, QF and a generic k-th of m quantile, with 0 < k < m, as
        well as a histogram of the distribution within specific bounds and with
        the specified number of bins. The parameters of a distribution are
        defined during instantiation, and they can be changed later via setter
        properties.
    stat_tests: Implements statistical significance tests as functions returning
        a class instance, which can generate human-readable report. The input
        data must be passed as instance(s) of Statistics1D class, and the test
        type (1-sided left- or right-tailed, 2-sided) must be indicated using
        the enumeration values GT_TEST, LT_TEST or NEQ_TEST defined in this
        module.
"""

__project__ = 'Statistics of the measurements with experimental uncertainties'
__version_info__= (1, 1, 0)
__version_suffix__= '-rc1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '01-05-2023'
__status__ = 'Production'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['base_functions', 'ordered_functions', 'data_classes',
            'distribution_classes', 'inverse_distributions', 'stat_tests']