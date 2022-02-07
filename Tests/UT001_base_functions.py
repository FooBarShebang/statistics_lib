#usr/bin/python3
"""
Module statistics_lib.Tests.UT001_base_functions

Set of unit tests on the module stastics_lib.base_functions.
"""


__version__= '1.0.0.0'
__date__ = '07-02-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import unittest
import random
import statistics

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(os.path.dirname(MODULE_PATH))
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

import statistics_lib.base_functions as test_module

from phyqus_lib.base_classes import MeasuredValue

#globals


FLOAT_CHECK_PRECISION = 8 #digits after comma

#classes

#+ test cases

class Test_Basis(unittest.TestCase):
    """
    """
    pass

class Test_GetMean(Test_Basis):
    """
    """
    pass

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GetMean)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, ])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting statistics_lib.base_functions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)
