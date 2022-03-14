# Calculation of the special functions

## Scope

This document provides details on the implementation of the special functions required for calculations of probability density functions (PDF), cummulative distribution functions (CDF) and quantile functions (QF, a.k.a. inverse cummulative distribution function ICDF).

The concerned special functions are either polynomial approximations or are constructed from other special functions, implemented in this library or in the Standard Python Library.

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
A_n^k \equiv {}_n P_k \equiv P(n,k) = n * (n-1) * (n-2) * ... * (n-k+1) = \frac{n!}{(n-k)!} = \prod_{m=n-k+1}^n{m} \equiv \prod_{m=0}^{k-1}{(n-m)}
$$

This function is implemented as *math.perm*(n, k) in the Standard Python Library (version >= 3.8). In the case of an older Python interpreter is should be impemented as looped multiplication form (n-k+1) towards n instead of ratio of factorials in order to achieve beter accuracy.

The last relevant function is *combinations*, which says how many unique sub-sets of k elements can be formed from a set of *n* unique elements, i.e. selection with the order being unimportant (i.e. {1, 2, 3} and {2, 1, 3} are the same sub-set). Basically, there are $A_n^k$ in total ways to select k elements from a set of n elements, whereas within a selected sub-set of k elements there are k! ways to re-arrange the elements. Therefore, the number of combinations is (note the different notations often used):

$$
C_n^k \equiv \binom{n}{k} = \frac{A_n^k}{P_k} = \frac{n!}{k! (n-k)!} \equiv \frac{A_n^{n-k}}{P_{n-k}} = C_n^{n-k}
$$

This function is implemented as *math.comb*(n, k) in the Standard Python Library (version >= 3.8). In the case of an older Python interpreter is should be impemented as follows in order to achieve beter accuracy:

* If k > (n-k) - calculate $A_n^{n-k}$ and (n-k)!, then $C_n^k = \frac{A_n^{n-k}}{(n - k)!}$
* Otherwise -  calculate $A_n^k$ and k!, then $C_n^k = \frac{A_n^k}{k!}$

## Inverse error function

TODO:

* [Wiki](https://en.wikipedia.org/wiki/Error_function#Inverse_functions)
* [Pure python](https://stackoverflow.com/questions/42381244/pure-python-inverse-error-function)
* [Scipy1](https://github.com/scipy/scipy/blob/main/scipy/special/cephes/ndtri.c)
* [Scipy2](https://github.com/jeremybarnes/cephes/blob/master/cprob/polevl.c)

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

## Incomplete gamma functions
