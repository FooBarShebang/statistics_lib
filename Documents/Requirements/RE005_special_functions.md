# Requirements for the Module statistics_lib.distribution_classes

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

**Requirement ID:** REQ-FUN-500

**Title:** Functionality implemented by the module (scope)

**Description:** The module should implement the following special mathematical functions:

* Calculation of k-permutations (n permute k) and combinations (n choose k) - to cover the older Python interpreters v < 3.8
* Calculation of the inverse error function
* Calculation of beta function
* Calculation of incomplete beta function as well as of the regularized version of the same function
* Calculation of incomplete lower and upper gamma functions as well as of the regularized versions of the same functions

All these functions should perform calculations correctly.

**Verification Method:** A

___

**Requirement ID:** REQ-FUN-510

**Title:** Permutations function

**Description:** The function *permutation*(n, k) accepts two non-negative integer numbers 0 <= k <= n and returns an integer number equal to n! / (n-k)!

**Verification Method:** T

___

**Requirement ID:** REQ-FUN-520

**Title:** Combination function

**Description:** The function *combination*(n, k) accepts two non-negative integer numbers 0 <= k <= n and returns an integer number equal to n! / [k! (n-k)!]

**Verification Method:** T

___

**Requirement ID:** REQ-FUN-530

**Title:** ?

**Description:** ?

**Verification Method:** T

___

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AWM-500

**Title:** Improper type of an agrument

**Description:** The **TypeError** or its sub-class should be raised if an improper data type argument is passed into any function.

**Verification Method:** T

___

**Requirement ID:** REQ-AWM-501

**Title:** Improper value of an agrument

**Description:** The **ValueError** or its sub-class should be raised if an argument of a proper data type, but of unacceptable value is passed into any function.

**Verification Method:** T
