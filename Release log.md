# Release log of library statistics_lib

# 2026-??-?? v1.3.0-rc1

* Added support of Statistics1D class instances as the instantiation argument(s) of Statistics1D and Statistics2D classes
* Added module *plot\_functions* with the following functionality
  * Calculation of correlation matrix of 2 or more data sets of equal length
  * Calculation of covariance matrix of 2 or more data sets of equal length
  * Q-Q plot of a data set vs another data set or model distribution
  * P-P plot of a data set vs another data set or model distribution
  * Direct comparison plot of two data sets of the equal length
  * Bland-Altman comparison plot of two data sets of the equal length
  * Histogram comparison of a data set vs another data set or model distibution
  * Plot of multiple data sets at the same X-Y coordinates (single subplot), each data set has own X- and Y- points
  * Plot of 2 to 9 (inclusively) different data sets arranged in a grid of individual sub-plots
  * Histogram graph of one or more data sets using the same X-coordinates / characterization

## 2026-10-14 v1.2.0-rc1

* Added to Statistic1D and Statistics2D classes support for
  * built-in len() function
  * built-in iter() function, therefore 'for loop' and enumeration()
  * integer indexing
* Added to Statistics1D class support for
  * array-scalar and scalar-array basic arithmetics: addition, subtraction, multiplication, division
  * array-array (per element) basic arithmetics: addition, subtraction, multiplication, division
  * raising to an integer power
  * generation of z-score distribution from the stored data

## 2023-05-01 v1.1.0-rc1

* Moved implementation of the special functions into a different library *math\_extra\_lib*. Module *special\_functions* now simply aliases them.
* Cleaned-up code

## 2022-05-16 v1.0.0-rc1

The first release.

## 2022-05-12 v0.8.0-dev1

Implemented and tested module *stat_tests*, which provided functions for the statistical hypothesis significance testing, including z-test, one sample and two samples (paired and unpaired) Student's t-tests, Welch t-test, F-test on samples variances, chi-squared test on the sample's variance, as well as ANOVA F-test, Levene's and Brown-Forsythe tests.

## 2022-04-28 v0.7.0-dev1

Implemented and tested module *inverse_distributions*, which provides implementation of a number of additional model distributions: inverse Gaussian, inverse Gamma, inverse Chi-squared, Cauchy and Levy distribution.

## 2022-04-21 v0.6.0-dev1

Implemented and tested module *distribution_classes*, which provides implementation of the model distributions: continuous and discrete - from which some are used in the statistical tests, including Gaussian / Z-distribution, Student`s t-distribution, Chi-squared distribution and F-distribution.

## 2022-04-07 v0.5.0-dev1

Implemented and tested module *special_functions*, which provides inverse error function, beta function, incomplete beta functions and incomplete gamma functions.

## 2022-03-09 v0.4.0-dev1

Implemented and tested module *data_classes*, which provides classes for 1D and 2D statistical data encapsulation and calculation of the relevant statistical properties.

## 2022-02-24 v0.3.0-dev1

Implemented and tested module *ordered_functions*, which provides functionality to calculate median, quartiles, quantiles and modes of a sample data distribution, as well as Spearman and Kendall rank correlation coefficients.

## 2022-02-10 v0.2.0-dev1

* Refactored the code of *base_functions* module to avoid redundant input data sanity checks and allow proper exception traceback manipulation with the chained functions call
* Redefined the unit-tests for that module to use randomly generated sequences instead of pre-defined ones

## 2021-01-12 v0.1.0-dev1

Implemented, tested and documented module *base_functions* - 1D and 2D statistics supporting measurement with uncertainty data type.
