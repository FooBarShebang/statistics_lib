"""
Module statistics_lib.Tests.UT004_distribution_classes

Set of unit tests on the module stastics_lib.distribution_classes. See the test
plan / report TE004_distribution_classes.md
"""


__version__= '1.0.0.0'
__date__ = '16-03-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import unittest

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.distribution_classes as test_module