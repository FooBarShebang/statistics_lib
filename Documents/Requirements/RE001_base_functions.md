# Requirements for the Module statistics_lib.base_functions

## Conventions

Requirements listed in this document are constructed according to the following structure:

**Requirement ID:** REQ-UVW-XYZ

**Title:** Title / name of the requirement

**Description:** Description / definition of the requirement

**Verification Method:** I / A / T / D

The requirement ID starts with the fixed prefix 'REQ'. The prefix is followed by 3 letters abbreviation (in here 'UVW'), which defines the requiement type - e.g. 'FUN' for a functional and capability requirement, 'AWM' for an alarm, warnings and operator messages, etc. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the requirement ordering number for this object. E.g. 'REQ-FUN-112'. Each requirement type has its own counter, thus 'REQ-FUN-112' and 'REQ-AWN-112' requirements are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Functional and capability requirements

**Requirement ID:** REQ-FUN-100

**Title:** Functionality implemented by the module (scope)

**Description:** The module should implement a number of functions to calculate the basic 1D and 2D statistical properties of a data set:

* 1D statstics
  * Arithmetic mean
  * Variance with the Bessel correction (sample variance) and without the correction (population variance)
  * Standard deviation with the Bessel correction (sample deviation) and without the correction (population deviation)
  * Standard error of the mean of a data set (as population - i.e. without Bessel correction)
  * Skewness with the Bessel correction (sample skewness) and without the correction (population skewness)
  * Excess kurtosis with the Bessel correction (sample kurtosis) and without the correction (population kurtosis)
  * Generic Nth moment of a data set distributiion (as population - i.e. without Bessel correction) - both central and non-central variants
  * 'Full' standard error of the mean of a data set as population and including the individual data ppints 'measurement uncertainties'
* 2D statics
  * Covariance of a 2D data set (as population - i.e. without Bessel correction)
  * Pearson's coefficient of correlation *r* of a 2D data set (as population - i.e. without Bessel correction)
  * Generic Nth-Mth moment of a 2D data set distributiion (as population - i.e. without Bessel correction) - both central and non-central variants

**Verification Method:** T
___

**Requirement ID:** REQ-FUN-101

**Title:** Input and ouput data format

**Description:** The 1D statistics functions should accept the input data set as any flat sequence (e.g. list or tuple) of real numbers (int or float) or instances of a data type class imlementing a 'real life measurement' with the associated uncertainty of the measurement, which is API compatible with the **phyqus_lib.base_classes.MeasuredValue** class, i.e. the 'mean' value of the measurement being accessible via field / property *Value* and the associated uncertainty - via field / property *SE*. Such sequence does not have to be homogeneous, and it may be an arbitrary mixture of such instances, integer and floating point numbers. A 2D statistical data set should be passed as two such sequences of the same length.

**Verification Method:** T

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AWM-100

**Title:** Unacceptable type of the input data

**Description:** The **TypeError** or its sub-class should be raised in response to the unacceptable input (argument(s) data type(s)) in the following situations:

* A 1D data set (or one of the sub-sets of the 2D data set) is not a flat sequence of real numbers of 'real life measurements' with the associated uncertainties, which means:
  * The respective argument is not a sequence, OR
  * The respective argument is a sequence, but, at least, one element of it is neither integer, or floating point number, or an instance of a measurement with the associated uncertainty data type class
* A power of a statistical moment is not an integer number

**Verification Method:** T
___

**Requirement ID:** REQ-AWM-101

**Title:** Unacceptable value(s) of the input data

**Description:** The **ValueError** or its sub-class should be raised in response to the unacceptable input (argument(s) data value(s)) in the following situations:

* A 1D data set (or one of the sub-sets of the 2D data set) is an empty sequence
* The length of the sequence is shorter than the 'number of the degrees of freedom' in the case of the Bessel-corrected functions; i.e. 2 for the sample variance and standard deviation, 3 for the sample skewness, and 4 for the sample kurtosis
* The lengths of the sub-sets of a 2D data set are not equal
* A power of a statistical moment is an integer, but it is not positive

**Verification Method:** T
