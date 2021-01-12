# Test Report on the Module statistics_lib.base_functions

## Conventions

Each test is defined following the same format. Each test receives a unique test identifier and a reference to the ID(s) of the requirements it covers (if applicable). The goal of the test is described to clarify what is to be tested. The test steps are described in brief but clear instructions. For each test it is defined what the expected results are for the test to pass. Finally, the test result is given, this can be only pass or fail.

The test format is as follows:

**Test Identifier:** TEST-\[I/A/D/T\]-XYZ

**Requirement ID(s)**: REQ-uvw-xyz

**Verification method:** I/A/D/T

**Test goal:** Description of what is to be tested

**Expected result:** What test result is expected for the test to pass

**Test steps:** Step by step instructions on how to perform the test

**Test result:** PASS/FAIL

The test ID starts with the fixed prefix 'TEST'. The prefix is followed by a single letter, which defines the test type / verification method. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the test ordering number for this object. E.g. 'TEST-T-112'. Each test type has its own counter, thus 'TEST-T-112' and 'TEST-A-112' tests are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Tests preparations

Create a 2D data set in a spreadsheet (see, *../../Tests/Test_statistics_base.ods*) with, at least, 10 pairs of (X, Y) values, where each X and Y value are randomly chosen integer or floating point number (positive, negative or zero). Also add 2 columns of the same length as the associated measurements errors X_SE and Y_SE; only non-negative values are allowed.

* Calculate the sample and population variance, standard deviation and skewness as well as sample excess kurtosis for the both X and Y sub-sets using the built-in spreadsheet functions.
* Calculate the population covariance and Pearson's correlation coefficient *r* for the X-Y 2D data set using the built-in spreadsheet functions.
* Manually calculate the central and non-central 1D moments of both X and Y sub-sets up to the 4th power inclusively.
* Manually calculate the central and non-central 2D (cross-) moments of X-Y data set up to the 3rd-3rd moment.
* Manually calculate the standard error of the mean of the X and Y data sub-sets as full populations - SE(X) and SE(Y)
* Manually calculate the 'full' standard errors accounting for the the individual uncertainties (SE_X and SE_Y) as SEF(X) = SQRT(SE^2(X) + \<SE\_X\>^2) and SEF(Y) = SQRT(SE^2(Y) + \<SE\_Y\>^2)

Copy the data sets and the expected values into the Python unit test module [UT001_base_functions.py](../../Tests/UT001_base_functions.py).

## Tests definition (Test)

**Test Identifier:** TEST-T-100

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-101

**Verification method:** T

**Test goal:** Input data types and correctness of calculations with 1D statistics functions, except 'full' standard error calculation.

**Expected result:** Any (generic) flat sequence of real numbers and / or measurements with uncertainty instances can be used as the input data set for the functions, and they return a single integer or floating point number, which (rounded) value is equal to the corresponding value exported from the spreadsheet up to, at least, 8 digits after the digital comma.

**Test steps:** Review the source code and ensure that all required functions are implemented. Then perform the following unit test with each of the concerned functions.

* Create a list of int / float numbers mixture from the X data set exported from the spreadsheet
* Pass this list as the argument into the function being tested and compare the returned result with the expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Convert this list into a tuple
* Pass this tuple as the argument into the function being tested and compare the returned result with the **same** expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Create a list of instances of **phyqus_lib.base_classes.MeasuredValue** class from the X + X_SE data set exported from the spreadsheet
* Pass this list as the argument into the function being tested and compare the returned result with the **same**  expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Convert this list into a tuple
* Pass this tuple as the argument into the function being tested and compare the returned result with the **same**  expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Create a list with each element being randomly chosen to be a plain real number (only X-value) or an instance of **phyqus_lib.base_classes.MeasuredValue** class (both the X-value and X_SE-value)
* Pass this list as the argument into the function being tested and compare the returned result with the **same**  expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Convert this list into a tuple
* Pass this tuple as the argument into the function being tested and compare the returned result with the **same**  expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Repeat these steps with the Y + Y_SE data set
* In case of the testing of the function implementing a generic 1D statistical moment calculation - perform these test with the respective argument (moment power) as an integer in the range 1 to 4 inclusively; check both central and non-central moment variants

**Test result:** PASS
___

**Test Identifier:** TEST-T-101

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-101

**Verification method:** T

**Test goal:** Input data types and correctness of the 'full' standard error calculation.

**Expected result:** Any (generic) flat sequence of real numbers and / or measurements with uncertainty instances can be used as the input data set for the function, and it returns a single integer or floating point number, which (rounded) value is equal to the corresponding value exported from the spreadsheet up to, at least, 8 digits after the digital comma.

**Test steps:** This test is performed only on the function implementing the 'full' standard error calculations.

* Create a list of int / float numbers mixture from the X data set exported from the spreadsheet
* Pass this list as the argument into the function being tested and compare the returned result with the expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument), which is the usual standard error of the mean of population SE(X) (i.e. standard deviation of population divided by the square root of the number of points.)
* Convert this list into a tuple
* Pass this tuple as the argument into the function being tested and compare the returned result with the **same** expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Create a list of instances of **phyqus_lib.base_classes.MeasuredValue** class from the X + X_SE data set exported from the spreadsheet
* Pass this list as the argument into the function being tested and compare the returned result with the expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument), i.e. SEF(X) = SQRT(SE^2(X) + \<SE\_X\>^2)
* Convert this list into a tuple
* Pass this tuple as the argument into the function being tested and compare the returned result with the **same**  expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Create a list with each element being randomly chosen to be a plain real number (only X-value) or an instance of **phyqus_lib.base_classes.MeasuredValue** class (both the X-value and X_SE-value)
* Pass this list as the argument into the function being tested and compare the returned result, which should be greater than or equal to SE(X), but less than or equal to SEF(X)
* Convert this list into a tuple
* Pass this tuple as the argument into the function being tested and compare the returned result, which should be greater than or equal to SE(X), but less than or equal to SEF(X)
* Repeat these steps with the Y + Y_SE data set

**Test result:** PASS
___

**Test Identifier:** TEST-T-102

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-101

**Verification method:** T

**Test goal:** Input data types and correctness of calculations with 2D statistics functions.

**Expected result:** Any two (generic) flat sequences of real numbers and / or measurements with uncertainty instances can be used as the input data set for the functions, and they return a single integer or floating point number, which (rounded) value is equal to the corresponding value exported from the spreadsheet up to, at least, 8 digits after the digital comma.

**Test steps:** Review the source code and ensure that all required functions are implemented. Then perform the following unit test with each of the concerned functions.

* Create a list of int / float numbers mixture from the X data set exported from the spreadsheet, and the second list of int / float numbers mixture from the Y data set
* Pass the both lists as the arguments into the function being tested and compare the returned result with the expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Convert both lists into tuples
* Pass these tuples as the arguments into the function being tested and compare the returned result with the **same** expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Create a list of instances of **phyqus_lib.base_classes.MeasuredValue** class from the X + X_SE data set exported from the spreadsheet, and the second list of such instances from the Y + Y_SE data set
* Pass these lists as the arguments into the function being tested and compare the returned result with the **same**  expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Convert both lists into tuples
* Pass these tuples as the arguments into the function being tested and compare the returned result with the **same**  expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Create a list with each element being randomly chosen to be a plain real number (only X-value) or an instance of **phyqus_lib.base_classes.MeasuredValue** class (both the X-value and X_SE-value), make the similar mixted content list for the Y + Y_SE data set
* Pass these lists as the arguments into the function being tested and compare the returned result with the **same**  expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Convert both lists into tuples
* Pass these tuples as the arguments into the function being tested and compare the returned result with the **same**  expected value (from the spreadsheet) using *assertAlmostEqual*() method with 8 digits precision (*places = 8* keyword argument)
* Repeat these steps with the Y + Y_SE data set
* In case of the testing of the funciton implementing the generic 2D moment, perform this test in a nested loop, iterating both X- and Y-powers in the range 1 to 3 inclusively, and check both the central and the non-central moment variant

**Test result:** PASS

___

**Test Identifier:** TEST-T-103

**Requirement ID(s)**: REQ-AWM-100

**Verification method:** T

**Test goal:** A sub-class of **TypeError** exception is raised in response to the improper type of the input data.

**Expected result:** Such an exception is raised if, at least, one of the data set arguments is not a flat sequence of real numbers and / or measurements with uncertainties, or any of the moment powers is not an integer.

**Test steps:** Use the following procedure:

* Define a sequence of values, which are not a flat sequence of real numbers and / or measurements with uncertainties, e.g. just a number, a string, a numeric data type (not its instance!), a list or a tuple containg a string or a nested sequence as one of its arguments, etc.
* In a loop try to pass each element of that sequence as the data set into the function being tested within the context of *assertRaises*() method with catching by the **TypeError**
  * In the case of 2D statistics functions use any valid numeric sequence as the second data sub-set, but make sure that its length is equal to the length of the improper sequence argument, if the first argument is a sequence
  * Try also swapting the proper and improper sequences as X- and Y-data arguements
* Specifically for the moment calculation functions also try proper X- (and Y-) data set(s) as the input, but pass anything but integer as the requried power of the moment
  * In the case of 2D moment use 1 as the second power, also try to swap the powers

**Test result:** PASS

___

**Test Identifier:** TEST-T-104

**Requirement ID(s)**: REQ-AWM-101

**Verification method:** T

**Test goal:** Input data types and correctness of calculations with 1D statistics functions, except 'full' standard error calculation.

**Expected result:** A sub-class of **ValueError** exception is raised in response to the improper type of the input data.

**Test steps:** Use the following procedure:

* All described 'try' calls are to made within the context of *assertRaises*() method with catching by the **ValueError** exception
* Try to call the function being tested with an empty list and an empty tuple as the data set argument
  * In the case of the Bessel corrected variance and standard deviation calculations - also try a list or tuple containg only a single real number element
  * In the case of the Bessel corrected skewness calculation - also try a list or tuple containg only a single real number element, and a sequence of 2 real numbers
  * In the case of the Bessel corrected kurtosis calculation - also try a list or tuple containg only a single real number element, a sequence of 2 real numbers, and a sequence of 3 real numbers
* In the case of 2D statistics functions:
  * Try this with the first (X-data) set being an empty sequence, whilst the secod data set being non-empty list of real numbers of an arbitrary length
  * Try it with the data set arguments being swapped
  * Also try to pass two proper, flat lists or tuples of real numbers as the data set arguments, provided that the lengths of the both sequences are greater than zero, but they are not equal
* In the case of 1D generic moment calculation function pass a proper real number sequence as the data set, but a zero or a negative integer as the power
* In the case of 2D generic moment calculation function pass two proper real number sequences of the same length as the data seta, but a zero or a negative integer as the first power, and 1 as the second power; try also with the power arguments being swapped

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**             | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------------------- | :----------------------- |
| REQ-FUN-100        | TEST-T-100, TEST-T-101, TEST-T-102 | YES                      |
| REQ-FUN-101        | TEST-T-100, TEST-T-101, TEST-T-102 | YES                      |
| REQ-AWM-100        | TEST-T-103                         | YES                      |
| REQ-AWM-101        | TEST-T-104                         | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| YES                                          | All tests are passed |
