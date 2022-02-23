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

"""

__project__ = 'Statistics of the measurements with experimental uncertainties'
__version_info__= (0, 3, 0)
__version_suffix__= '-dev1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '23-02-2022'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['base_functions', 'ordered_functions']