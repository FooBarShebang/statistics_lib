# Calculation of the special functions

## Scope

This document provides details on the implementation of the special functions required for calculations of probability density functions (PDF), cummulative distribution functions (CDF) and quantile functions (QF, a.k.a. inverse cummulative distribution function ICDF).

The concerned special functions are either polynomial approximations or are constructed from other special functions, implemented in this library or in the Standard Python Library.

### Inverse error function

TODO:

* [Wiki](https://en.wikipedia.org/wiki/Error_function#Inverse_functions)
* [Pure python](https://stackoverflow.com/questions/42381244/pure-python-inverse-error-function)
* [Scipy1](https://github.com/scipy/scipy/blob/main/scipy/special/cephes/ndtri.c)
* [Scipy2](https://github.com/jeremybarnes/cephes/blob/master/cprob/polevl.c)
