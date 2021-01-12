# Module statistics_lib.base_functions Reference

## Scope

This document describes the intended usage, design and implementation of the functionality implemented in the module **base_functions** of the library **statistics_lib**. The API reference is also provided.

This module provides functions for calculation of:

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

## Intended Use and Functionality

The module should provide functionality to calcualte specific statistic moments of 1D or 2D data sets, which could be used as the back-end for higher abstraction functionality within this library as well as called from another libraries or modules by an end user.

The unique feature of this module is that the statistic properties can be computed not only on sequences of real numbers (integers or floating point), but the measurements with uncertainties can also be included into the data set. A measurement with uncertainty is, basically, a tuple of two real numbers $(x_i, z_i)$, where $x_i$ represents the 'mean' of the measured value, and $z_i \geq 0$ is the measurement uncertainty. Thus, any real number $x_i$ can also be represented as a measurement with *zero* uncertainty, i.e. $(x_i, 0)$.

The functions defined in this module can accept an arbirary mixture of real numbers and such measurements with uncertainties tuples - as a generic sequence argument - and treat it as a list or tuple of real numbers (ignoring the measurement uncertainties in all but one function).

The second assumption is that in the majority of the practical cases the data set $<X>$ is large, i.e. its length $N\gg1$, and, most probably, it represents the entire population to be analyzed. Therefore, the Bessel correction is not applied.

The aritmetic mean of the data distribution is calculated as the first non-central moment

$$<X> = E[X] = \frac{\sum\limits_{i=1}^{N}{x_i}}{N}$$

The generic K-th non-central moment is

$$E[X^K] = \frac{\sum\limits_{i=1}^{N}{x_i^K}}{N}$$

For instance, the mean of squares is the 2nd non-central moment

$$<X^2> = E[X^2] = \frac{\sum\limits_{i=1}^{N}{x_i^2}}{N}$$

The generic K-th central moment is

$$E[(X-<X>)^K] = \frac{\sum\limits_{i=1}^{N}{(x_i - <X>)^K}}{N}$$

For instance, the variance is the second central moment

$$Var(X) = E[(X-<X>)^2] = \frac{\sum\limits_{i=1}^{N}{(x_i - <X>)^2}}{N}$$

The standard deviation is computed as the square root of the variance

$$\sigma(X) = \sqrt{Var(X)}$$

The standard error of the mean is

$$SE(X) = \frac{\sigma(X)}{\sqrt{N}} = \frac{\sqrt{\sum\limits_{i=1}^{N}{(x_i - <X>)^2}}}{N}$$

However, for the measurements with the associated individual uncertainties these uncertainties must be taken into account - the so called 'full standard error'

$$SE_F(X) = \frac{\sqrt{\sum\limits_{i=1}^{N}{(x_i - <X>)^2 + \left(\sum\limits_{i=1}^{N}{z_i}\right)^2}}}{N}$$

Note that, generally, $SE_F(X) \geq SE(X)$, and $SE_F(X) = SE(X)$ only if the data set consists of only real numbers, or all associated individual uncertainties are zero. This functionality is added for the implementation of the standard error propagation model, specifically - averaging of multiple measurements.

It is also possible to define the normalized central moment as

$$E\left[\left(\frac{X-<X>}{\sigma(X)}\right)^K\right] = \frac{\sum\limits_{i=1}^{N}{(x_i - <X>)^K}}{N \times {\sigma(X)}^K}$$

This functionality (as generic moment) is not implemented in the module, however, two special cases are indeed implemented - skewness and kurtosis:

$$Skew(X) = E\left[\left(\frac{X-<X>}{\sigma(X)}\right)^3\right] = \frac{\sum\limits_{i=1}^{N}{(x_i - <X>)^3}}{N \times {\sigma(X)}^3}$$

$$KurtEx(X) = E\left[\left(\frac{X-<X>}{\sigma(X)}\right)^4\right] - 3 = \frac{\sum\limits_{i=1}^{N}{(x_i - <X>)^3}}{N \times {\sigma(X)}^4} - 3$$

Note, that the *excess kurtosis* is, in fact, calculated.

In general, especially in the cases of small samples (N ~ 10) then mean and standard deviation calculated from a sample are not, generally speaking, the same as the *true* mean and standard deviation of the distribution of the entire population, from which the sample is taken: $<X> \neq \mu$ and $\sigma(X) \neq \sigma_X$. The formulas above are *biased* estimators of the *true* moments based on $<X>$ and $\sigma(X)$ instead of $\mu$ and $\sigma_X$. The Bessel correction provides *unbiased* (but not *per se* accurate) estimators, known as *sample* variance, standard deviation, skewness and (excess) kurtosis.

$$Var_S(X)  = \frac{\sum\limits_{i=1}^{N-1}{(x_i - <X>)^2}}{N} \approx E[(X-\mu)^2]$$

$$\sigma_S(X) = \sqrt{Var_S(X)} \approx \sigma_X$$

$$Skew_S(X) = \frac{\sum\limits_{i=1}^{N}{(x_i - <X>)^3}}{{\sigma(X)}^3} \times \sqrt{\frac{N \times (N-1)}{N-2}} \approx E\left[\left(\frac{X-\mu}{\sigma_X}\right)^3\right]$$

$$KurtEx_S(X) = \frac{\sum\limits_{i=1}^{N}{(x_i - <X>)^3}}{{\sigma(X)}^4} \times \frac{(N-1) \times (N+1)}{N \times (N-2) \times (N-3)} - 3 \times \frac{\left(N-1\right)^2}{(N-2) \times (N-3)} \approx E\left[\left(\frac{X-\mu}{\sigma_X}\right)^4\right] - 3$$

Finally, the module implements calculation of the basic 2D statistic properties ignoring the individual uncertainties and Bessel correction, e.g. covariance

$$Cov(X, Y) = E[(X-<X>) \times (Y - <Y>)] = \frac{\sum\limits_{i=1}^{N}{(x_i - <X>) \times (y_i - <Y>)}}{N}$$

Non-central generic cross-moment

$$E[X^K \times Y^M] = \frac{\sum\limits_{i=1}^{N}{x_i^K \times y_i^M}}{N}$$

Central generic cross-moment

$$E[(X-<X>)^K \times (Y-<Y>)^M] = \frac{\sum\limits_{i=1}^{N}{(x_i - <X>)^K \times (y_i - <Y>)^M}}{N}$$

And the Pearson's coefficient of correlation

$$r = \frac{Cov(X,Y)}{\sqrt{Var(X) \times Var(Y)}}$$

## Design and Implementation

The required functionality is implemented as a number of functions. The table below provides the correspondence between the implemented function names, their functionality and the corresponding spreadsheet function (MS Excel or LibreOffice Calc):

| **Function name**          | **Functionality**                                          | **Spreadsheet** |
| -------------------------- | ---------------------------------------------------------- | --------------- |
| GetMean                    | E[X]                                                       | AVERAGE         |
| GetMeanSquares             | E[X^2]                                                     | N/A             |
| GetVariance                | E[(X-\<X\>)^2]                                             | VAR.P           |
| GetVarianceBessel          | N*E[(X-\<X\>)^2]/(N-1)                                     | VAR.S           |
| GetStandardDeviation       | SQRT(E[(X-\<X\>)^2])                                       | STDEV.P         |
| GetStandardDeviationBessel | SQRT(N*E[(X-\<X\>)^2]/(N-1))                               | STDEV.S         |
| GetStandardError           | SQRT(E[(X-\<X\>)^2]/N)                                     | N/A             |
| GetFullStandardError       | see text above                                             | N/A             |
| GetSkewness                | E[(X-\<X\>)^3] / E[(X-\<X\>)^2]^3/2                        | SKEWP           |
| GetSkewnessBessel          | see text above                                             | SKEWS           |
| GetKurtosis                | (E[(X-\<X\>)^4] / E[(X-\<X\>)^2]^2) - 3                    | N/A             |
| GetSkewnessBessel          | see text above                                             | KURT            |
| GetMoment                  | E[X^N] and E[(X-\<X\>)^N]                                  | N/A             |
| GetCovariance              | E[(X-\<X\>)*(Y-\<Y\>)]                                     | COVARIANCE.P    |
| GetMoment2                 | E[(X^N)\*(Y^M)] and E[((X-\<X\>)^N)\*((Y-\<Y\>)^M)]        | N/A             |
| GetPearsonR                | E[(X-\<X\>)*(Y-\<Y\>)]/SQRT(E[(X-\<X\>)^2]*E[(Y-\<Y\>)^2]) | PEARSON         |

All these functions are designed to accept a generic sequence (or two sequences) containing only real number (integer or floating point) and / or instances of a class implementing measurements with uncertainty, which is expected to be API compatible with the **phyqus_lib.base_classes.MeasuredValue** class, i.e. to have fields / properties *Value* and *SE*. A different type of the input data set results in a **TypeError** typed exception. An empty data sequence, or unequal length X- and Y-data sequences result in **ValueError** typed exception.

Since the described input data sanity check is a routine common for all functions, it is implemented in special, helper functions (separate for 1D and 2D statistic functions), which are not intended to be used outside this module, and they are not discussed in the 'API Reference' section.

The checks on the argument(s) type, i.e. the input data being a sequence, is performed as 'IS A' test, but using the generic, ABC **collections.abc.Sequence**. The elements of a sequence are checked 2-ways (with OR conjunction):

* 'IS A' test on being instance of **int** or **float** type
* 'HAS A' test on having *Value* attribute

Apart from the data sanity checks these helper functions also 'unify' the input, i.e. they return the same length sequence of only real numbers, into which each real number from the input sequence is copied, and for the measurements with uncertainty the value its attribute *Value* is copied instead.

There is also the third helper function, which extracts the measurements uncertainties from a mixed sequence. It returns the same length sequence of only real numbers, into which for each real number from the input sequence a zero is placed, and for the measurements with uncertainty the value its attribute *SE* is copied instead. Note, that in this case 'HAS A' check is based on the presence of *SE* attribute.

In case of an improper input data these helper functions raise **UT_TypeError** and **UT_ValueError** exceptions defined in *introspection_lib.base_exceptions* module, and explicitely indicate to skip the 2 innermost frames from the traceback analysis. E.g., consider the following code, there the raised exception is caught.

```python
import statistics_lib.base_functions as bsf
...
#do something
...
#make faulty call
try:
    Mean = bsf.GetMean([1, 2.3, '1'])
except (TypeError, ValueError) as err:
    print(err.__class__.__name__, ':', err)
    print(err.Traceback.Info)
...
```

In this case, the traceback printed by the statement ```print(err.Traceback.Info)``` will end in the frame of the call ```Mean = bsf.GetMean([1, 2.3, '1'])```, thus hiding the implementation details, i.e. where inside *GetMean*() function the helper function was called, and where inside the helper function the exception was actually raised.

Note that if the raised exception is not caught, and it has propagated to the interactive console, the printed (system) traceback will include both frames - for the *GetMean*() and the helper function, with the helper function being the innermost (last) frame.

The functions implementing Bessel corrected calculations: *GetStandardDeviationBessel*(), *GetVarianceBessel*(), *GetSkewnessBessel*() and *GetKurtosisBessel*() also checks that the length of the sequence is not smaller than the reduced 'degrees of freedom' number (2, 3 and 4 respectively), and they raise **UT_ValueError** otherwise, indicating to skip the innermost frame from the traceback analysis.

The functions *GetMoment*() and *GetMoment2*() also check that the passed required power(s) of the moment to be calculated is (are) positive integer(s), raising **UT_TypeError** or **UT_ValueError** otherwise, and they indicate to skip the innermost frame from the traceback analysis.

Thus, using *try...except* paradigm, the traceback analysis provided by the custom exceptions allows 'hiding' of the implementation details, which facilites the debugging procedure, since the last (innermost) frame will point to the 'offending' call.

The actual calculations performed by the provided functions are, in principle, reduced to finding a specific central or non-central moment of the input data distribution, which is implemented using the built-in *pow*() function (since all powers in moments are positive integers) and *math.fsum*() function, which ensures extended precision of the floating point summation.

## API Reference

### Functions

**GetMean**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is empty

*Description*:

Calculates the arithmetic mean of a sequence, which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetMeanSquares**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is empty

*Description*:

Calculates the arithmetic mean of the squares of the values in a sequence, which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetVariance**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is empty

*Description*:

Calculates the variance of the values in a sequence (without the Bessel correction, i.e. assuming the sequence is the full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetVarianceBessel**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is shorter than 2 elements

*Description*:

Calculates the variance of the values in a sequence (with the Bessel correction, i.e. assuming the sequence is not full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetStandardDeviation**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is empty

*Description*:

Calculates the Std.Deviation of the values in a sequence (without the Bessel correction, i.e. assuming the sequence is the full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetStandardDeviationBessel**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is shorter than 2 elements

*Description*:

Calculates the Std.Deviation of the values in a sequence (with the Bessel correction, i.e. assuming the sequence is not full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetStandardError**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is empty

*Description*:

Calculates the standard error of the mean of the values in a sequence (without the Bessel correction, i.e. assuming the sequence is the full population) and without the acccount for the measurements uncertainties, which sequence can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetFullStandardError**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is empty

*Description*:

Calculates the standard error of the mean of the values in a sequence (without the Bessel correction, i.e. assuming the sequence is the full population) and including the individual measurements uncertainties, which sequence can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetSkewness**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is empty

*Description*:

Calculates the skewness of the values in a sequence (without the Bessel correction, i.e. assuming the sequence is the full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetSkewnessBessel**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is shorter than 3 elements

*Description*:

Calculates the skewness of the values in a sequence (with the Bessel correction, i.e. assuming the sequence is not full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetKurtosis**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is empty

*Description*:

Calculates the excess kurtosis of the values in a sequence (without the Bessel correction, i.e. assuming the sequence is the full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetKurtosisBessel**(Data)

*Signature*:

seq(type A) -> float

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: the passed sequence is shorter than 4 elements

*Description*:

Calculates the excess kurtosis of the values in a sequence (with the Bessel correction, i.e. assuming the sequence is not full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetMoment**(Data, N, *, IsCentral = True)

*Signature*:

seq(type A), int > 0 /, bool/ -> float

*Args*:

* *Data*: seq(type A); the input data sequence, expected a mixture of real numbers and 'real life measurements' (mean + associated uncertainty)
* *N*: int > 0; the power of the moment
* *IsCentral*: (keyword) bool; flag if the central moment should be calculated, defaults to True

*Raises*:

* **UT_TypeError**: the passed argument is not a sequence, OR any of its elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check); OR the second passed argument is not an integer
* **UT_ValueError**: the passed sequence is empty; OR the second passed argument is not positive

*Description*:

Calculates the Nth moment of the values in a sequence (without the Bessel correction, i.e. assuming the sequence is the full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty. By default, the central moment is calculated, pass keyword argument *IsCentral = False* explicitely to calculate a non-central moment.

**GetCovariance**(DataX, DataY)

*Signature*:

seq(type A), seq(type A) -> float

*Args*:

* *DataX*: seq(type A); the input data sequence, expected a mixture of real numbers and 'real life measurements' (mean + associated uncertainty) - the first data set sequence
* *DataY*: seq(type A); the input data sequence, expected a mixture of real numbers and 'real life measurements' (mean + associated uncertainty) - the second data set sequence

*Raises*:

* **UT_TypeError**: any of the passed data sets is not a sequence, OR any of their elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: any of the passed sequence is empty, OR their lengths are not equal

*Description*:

Calculates the covariance of the values in two data sets (without the Bessel correction, i.e. assuming the sequence is the full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.

**GetMoment2**(DataX, DataY, NX, NY, *, IsCentral = True)

*Signature*:

seq(type A), seq(type A), int > 0, int > 0 /, bool/ -> float

*Args*:

* *DataX*: seq(type A); the input data sequence, expected a mixture of real numbers and 'real life measurements' (mean + associated uncertainty) - the first data set sequence
* *DataY*: seq(type A); the input data sequence, expected a mixture of real numbers and 'real life measurements' (mean + associated uncertainty) - the second data set sequence
* *NX*: int > 0; the power of the moment for X data set
* *NY*: int > 0; the power of the moment for Y data set
* *IsCentral*: (keyword) bool; flag if the central moment should be calculated, defaults to True

*Raises*:

* **UT_TypeError**: any of the passed data sets is not a sequence, OR any of their elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check), OR any of the passed powers in not integer
* **UT_ValueError**: any of the passed sequence is empty, OR their lengths are not equal, OR any of the passed powers is not positive

*Description*:

Calculates the Nth-Mth moment of the values in two data sets (without the Bessel correction, i.e. assuming the sequence is the full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty. By default, the central moment is calculated, pass keyword argument *IsCentral = False* explicitely to calculate a non-central moment.

**GetPearsonR**(DataX, DataY)

*Signature*:

seq(type A), seq(type A) -> float

*Args*:

* *DataX*: seq(type A); the input data sequence, expected a mixture of real numbers and 'real life measurements' (mean + associated uncertainty) - the first data set sequence
* *DataY*: seq(type A); the input data sequence, expected a mixture of real numbers and 'real life measurements' (mean + associated uncertainty) - the second data set sequence

*Raises*:

* **UT_TypeError**: any of the passed data sets is not a sequence, OR any of their elements is not a real number (int or float, 'is a' check) or an instance of 'real life measurement' class ('has a' check)
* **UT_ValueError**: any of the passed sequence is empty, OR their lengths are not equal

*Description*:

Calculates the Pearson's coefficient of correlation r of the values in two data sets (without the Bessel correction, i.e. assuming the sequence is the full population), which can be a mix of int or float (real) numbers and instances of the 'real life measurements' class, i.e. the 2-tuples of the 'mean' value of a measurement and the associated measurement uncertainty.
