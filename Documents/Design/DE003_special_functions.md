# Calculation of the special functions

## Scope

This document provides details on the implementation of the special functions required for calculations of probability density functions (PDF), cummulative distribution functions (CDF) and quantile functions (QF, a.k.a. inverse cummulative distribution function ICDF). Only the real number arguments are considered, in which case the respective functions yield real numbers; although they can be continued onto complex numbers.

The concerned special functions can be implemented as polynomial or rational functions approximations or constructed from other special functions, implemented in this library or in the Standard Python Library.

The proposed implementation is either inspired by or translated into Python from:

[1] William H. Press, Saul A. Teukolsky, William T. Vetterling and Brian P. Flannery. **Numerical Recipes in C: The Art of Scientific Computing**. 2nd Ed. Cambridge University Press (1992). ISBN: 0-521-43108-5

further on referred to as *Numerical Recipes*.

## Background - combinatorics functions

Considering the discrete distributions the probability is often related to *combinatorics*, i.e. number of combinations under specific limitations.

The first function to consider is *factorial*, which calculates the number of possible arrangement of exactly *n* unique objects, if the order is important (i.e. {1, 2, 3} and {2, 1, 3} are considered to be different outcomes of the experiment). Basically, for the first position we have *n* possible choices of an object, for the second position - *n-1* possible choice (since one object is already removed), for the third position - *n-2* possible choice, etc., until only two objects remain with 2 possible choices, then for the last remaining object there is only a single possibility. Thus, the total number of possible arrangements, i.e. *full permutation* is (note different notations often used):

$$
P_n \equiv {}_n P_n \equiv P(n,n) = n * (n-1) * (n-2) * ... * 2 * 1 = n! = \prod_{k=1}^n{k} \equiv \prod_{k=0}^{n-1}{(n-k)}
$$

Basically, permutation of an empty set is 1, since there are no elements, and there is only one possible way to select nothing from any set. Similarly, for the set containing only 1 element there is only one possible way to select this element. Thus, 0! = 1 and 1! = 0. Therefore, it is possible to define factorial recursively as:

$$
n! = \begin{cases}
    1 \; \mathtt{if} \; n = 0 \\
    1 \; \mathtt{if} \; n = 1 \\
    n * (n-1)! \; \forall \; n>1, \; n \in \mathbb{N}
\end{cases}
$$

The factorial function is available as *math.factorial*() function in Standard Python Library.

The second relevant function is *partial permutation* or *k-permutation*, which calculates the number of possible arrangement of exactly *k* unique objects chosen of a set of *n* unique objects, if the order is important (i.e. {1, 2, 3} and {2, 1, 3} are considered to be different outcomes of the experiment). Similarly, for the first position we have *n* possible choices of an object, for the second position - *n-1* possible choice (since one object is already removed), for the third position - *n-2* possible choice, etc., but we stop at the k-th object, for which there are still *n-k+1* possible choices. Thus (note the different often used notations)

$$
A_n^k \equiv {}_n P_k \equiv P(n,k) = n * (n-1) * (n-2) * ... * (n-k+1) = \frac{n!}{(n-k)!} = \prod_{m=n-k+1}^n{m} \equiv \prod_{m=0}^{k-1}{(n-m)} \newline
A_n^k = \frac{n}{n-k} A_{n-1}^k = n A_{n-1}^{k-1} = (n-k+1) A_n^{k-1}
$$

This function is implemented as *math.perm*(n, k) in the Standard Python Library (version >= 3.8). In the case of an older Python interpreter is should be impemented as looped multiplication form (n-k+1) towards n instead of ratio of factorials in order to achieve beter accuracy in favour of the $\mathtt{exp}[\mathtt{ln}(\Gamma(n+1)) - \mathtt{ln}(\Gamma(k+1))]$ approach[^1], because Python supports an arbitrary length integer arithmetics.

The last relevant function is *combinations*, which says how many unique sub-sets of k elements can be formed from a set of *n* unique elements, i.e. selection with the order being unimportant (i.e. {1, 2, 3} and {2, 1, 3} are the same sub-set). Basically, there are $A_n^k$ in total ways to select k elements from a set of n elements, whereas within a selected sub-set of k elements there are k! ways to re-arrange the elements. Therefore, the number of combinations is (note the different notations often used):

$$
C_n^k \equiv \binom{n}{k} = \frac{A_n^k}{P_k} = \frac{n!}{k! (n-k)!} \equiv \frac{A_n^{n-k}}{P_{n-k}} = C_n^{n-k} \newline
C_n^k = \frac{n}{k} C_{n-1}^{k-1} = \frac{n}{n-k} C_{n-1}^k = \frac{n-k+1}{k} C_n^{k-1} = C_{n-1}^k + C_{n-1}^{k-1}
$$

This function is implemented as *math.comb*(n, k) in the Standard Python Library (version >= 3.8). In the case of an older Python interpreter is should be impemented as follows in order to achieve beter accuracy:

* If k > (n-k) - calculate $A_n^{n-k}$ and (n-k)!, then $C_n^k = \frac{A_n^{n-k}}{(n - k)!}$
* Otherwise -  calculate $A_n^k$ and k!, then $C_n^k = \frac{A_n^k}{k!}$

This approach is preferable to $\mathtt{exp}[\mathtt{ln}(\Gamma(n+1)) - \mathtt{ln}(\Gamma(k+1)) - \mathtt{ln}(\Gamma(n-k+1))]$ approach[^2], because Python supports an arbitrary length integer arithmetics.

## Inverse error function

The *error function* erf() is defined as:

$$
\mathtt{erf}(x > 0) = \frac{2}{\sqrt{\pi}} \int_0^x {e^{- t^2} dt} \newline
\mathtt{erf}(0) = 0 \newline
\mathtt{erf}(x < 0) = - \mathtt{erf}(-x)
$$

The *inverse error function* is the solution of equation $\mathtt{erf}(x) = y \; \Rightarrow \; x = \mathtt{erf}^{-1}(y)$, whith the following (obvious) prorperties:

$$
\mathtt{erf}(\mathtt{erf}^{-1}(y)) = y \newline
\mathtt{erf}^{-1}(\mathtt{erf}(x)) = x \newline
\mathtt{erf}^{-1}(-y) = - \mathtt{erf}^{-1}(y)
$$

This function is defined on the range (-1, 1); it is monotonically growing, and it yields values in the range $(- \infin, + \infin)$.

## Beta function

The *beta function* is defined as:

$$
B(x,y) = \int_0^1 {t^{x-1} (1-t)^{y-1} dt}
$$

In the case of *real* arguments *x* and *y*, it is defined for *x* > 0 and *y* > 0. It also can be defined in terms of *gamma function*, i.e.

$$
B(x,y) = \frac{\Gamma(x) \Gamma(y)}{\Gamma(x+y)}
$$

where gamma function is defined

$$
\Gamma(x) = \int_0^{\infin} {t^{x-1} e^{-t} dt}
$$

for $x$ > 0. Note, that $\Gamma(n \in \mathbb{N}) = (n-1)!$ on the natural numbers. The gamma function is implemented as *math.gamma*() in the Standard Python Library

Thus, the (complete) beta function can be calculated as:

$$
B(x,y) = \mathtt{exp} \left[ \mathtt{ln} \left( \frac{\Gamma(x) \Gamma(y)}{\Gamma(x+y)} \right) \right] = \mathtt{exp} \left[ \mathtt{ln} (\Gamma (x)) + \mathtt{ln} (\Gamma (y)) - \mathtt{ln} (\Gamma (x+y)) \right]
$$

for the better precision, where $\mathtt{ln} (\Gamma (x))$ is implemented as *math.lgamma*() function in the Standard Python Library, and exp() is *math.exp*() function.

## Incomplete beta functions

The generalization of the *beta function*, i.e. *incomplete beta function* is defined as:

$$
B(z;x,y) = \int_0^z {t^{x-1} (1-t)^{y-1} dt}
$$

for z > 0; and its *regularized* version is

$$
I_z(x,y) = \frac{B(z;x,y)}{B(x,y)}
$$

## Incomplete gamma functions

The (complete) gamma function is defined as integral from 0 to infinity, which can also be split into two integrals

$$
\Gamma(x) = \int_0^{\infin} {t^{x-1} e^{-t} dt} = \int_0^{y} {t^{x-1} e^{-t} dt} + \int_y^{\infin} {t^{x-1} e^{-t} dt} = \gamma(x,y) + \Gamma(x,y)
$$

where $\gamma(x,y) = \int_0^{y} {t^{x-1} e^{-t} dt}$ is the *lower incomplete gamma function* and $\Gamma(x,y) = \int_y^{\infin} {t^{x-1} e^{-t} dt}$ is the *upper incomplete gamma function*. In practice, the *reqularized* versions of incomplete gamma functions are often used, which are:

$$
P(x,y) = \frac{\gamma(x,y)}{\Gamma(x)} \newline
Q(x,y) = \frac{\Gamma(x,y)}{\Gamma(x)} \newline
P(x,y) + Q(x,y) = 1
$$

Note that they are defined for x > 0 and y > 0.

## References / implementation

TODO:

* [Pure python](https://stackoverflow.com/questions/42381244/pure-python-inverse-error-function)
* [Scipy1](https://github.com/scipy/scipy/blob/main/scipy/special/cephes/ndtri.c)
* [Scipy2](https://github.com/jeremybarnes/cephes/blob/master/cprob/polevl.c)

[^1]: Numerical Recipes. p 214.
[^2]: Numerical Recipes. p 215.