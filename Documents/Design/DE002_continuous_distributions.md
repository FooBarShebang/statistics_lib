# Design of classes implementing continuous distributions

## Scope

This document describes the design of classes implementing continuous distributions, i.e. which methods and properties they must provide, relation between properties and methods for a specific distribution and special mathematical functions required to implement those distributions.

## Background information

### Discrete distributions

A random variable *X* has a *discrete distribution* if there is only a finite (or countable) set of values, which it can have. In this case the probability of observation of value *x* is defined by the *probability mass function* (PMF), which is:

$$
p(x) = \begin{cases}
    \mathtt{Pr}[X = x] \; \forall \; x \in X,\\
    0 \; \forall \; x \notin X
\end{cases}
$$

The mean of the distribution is calculated as:

$$
\mathtt{Mean} = \mu = \mathtt{E}[X] = \sum_{x \in X} {x \times p(x)}
$$

The higher moments are calculated as

$$
\mathtt{Var}(X) = \sigma^2 = \mathtt{E}[(X - \mu)^2] =\sum_{x \in X} {(x - \mu)^2 \times p(x)} \newline
\mathtt{Skew}[X] = \mathtt{E}[\left( \frac{X - \mu}{\sigma} \right)^3] =\sum_{x \in X} {\left( \frac{x - \mu}{\sigma} \right)^3 \times p(x)} \newline
\mathtt{Kurt}[X] = \mathtt{E}[\left( \frac{X - \mu}{\sigma} \right)^4] =\sum_{x \in X} {\left( \frac{x - \mu}{\sigma} \right)^4 \times p(x)} \newline
$$

Usually, the *excess kurtosis* is used instead, which is defined as $\mathtt{Kurt}[X] - 3$.

The *cummulative distribution function* (CDF) *F(x)* is the probability of observation of the random variable *X* at the value less than or equal to the given value *x*, i.e.

$$
F(x) = \mathtt{Pr}[X \leq x] = \sum_{y \in X, \; y \leq x} {p(y)}
$$

CDF has the following properties:

$$
F(x) \in (0, 1] \; \forall \; x \in X \newline
F(x) > F(y) \; \forall \; x > y, \; x \in X, \; y \in X \newline
\mathtt{Pr}[a < X \leq b] = F(b) - F(a)
$$

The *median*, the *first quartile*, the *third quartile* and the generic k-th of m-quantile are formaly defined as:

$$
\mathtt{Median} = x: F(x) = 0.5 \newline
Q1 = Q_4^1 = x : F(x) = 0.25 \newline
Q3 = Q_4^3 = x : F(x) = 0.75 \newline
Q_m^k = x : F(x) = \frac{k}{m} \; \forall \; 0 < k \leq m
$$

Since the CDF is not a continuous function, but a *step function*, the quantiles (including median and quartiles) are calculated by sorting all possible values of the discrete random variable *X*, calculation of the corresponding *F(x)* values sequence and using the linear interpolation between two consecutive values, for which *F(x)* is below and above the required value respectively (see [DE001](./DE001_order_related.md) document).

### Continuous distributions

When a random variable *X* does not have a finite set of values, but may have any value within an interal $[a, b]$ the distribution is *continuous* and is described by the *probability denisty function* (PDF) $f(x)$ instead of set of probilities for specific values. For the many common and useful distributions the interval is the entire set of real numbers, i.e. $(-\infin, +\infin)$. Thus, for a continuous distribution there is no probability of any exact value, but the probability of the value being within a specific interval:

$$
\mathtt{Pr}[a \leq X \leq b] = \int_{a}^{b} {f(x) dx} \Rightarrow f(x) = \lim_{a \rightarrow x, b \rightarrow x} {\frac{\mathtt{Pr}[a \leq X \leq b]}{b-a}}
$$

The PDF has the following important properties:

$$
f(x) > 0 \; \forall \; x \in \mathbb{R} \newline
\int_{- \infin}^{+ \infin} {f(x) dx} = 1
$$

Hence, the *arithmetic mean* of the distribution is:

$$
\mathtt{Mean} = \mu = \mathtt{E}[X] = \int_{- \infin}^{+ \infin} {x f(x) dx}
$$

Similarly, the higher moments are defined as:

$$
\mathtt{Var}(X) = \sigma^2 = \mathtt{E}[(X - \mu)^2] =\int_{- \infin}^{+ \infin} {(x - \mu)^2 f(x) dx} \newline
\mathtt{Skew}[X] = \mathtt{E}[\left( \frac{X - \mu}{\sigma} \right)^3] =\int_{- \infin}^{+ \infin} {\left( \frac{x - \mu}{\sigma} \right)^3 f(x) dx} \newline
\mathtt{Kurt}[X] = \mathtt{E}[\left( \frac{X - \mu}{\sigma} \right)^4] =\int_{- \infin}^{+ \infin} {\left( \frac{x - \mu}{\sigma} \right)^4 f(x) dx} \newline
$$

**Note**: in practical applications *excess kurtosis* is used instead, which is defined as $\mathtt{Kurt}[X] - 3$. Furthermore, for the majority of the common parameteric distributions (like Gaussian, Binomial, Student's t-distibution, etc.) these properties have simple analitical expressions in terms of the parameters of the distribution; and they do not have to be calculated using numerical integration.

The second way to describe the distribution is the *cummulative distribution function* (CDF) $\Phi(x)$, which is the probability of observation of the random variable *X* at the value less than or equal to the given value *x*, i.e.

$$
\Phi(x) = \mathtt{Pr}[X \leq x] = \int_{- \infin}^{x} {f(y) dy} \Rightarrow f(x) =\frac{d}{dx}\Phi(x)
$$

which is just an alternative representation of the definition of PDF, since $\mathtt{Pr}[a \leq X \leq b] = \Phi(b) - \Phi(a)$. Naturally, CDF has the following properties:

$$
\Phi(x) \in [0, 1] \; \forall \; x \in \mathbb{R} \newline
\Phi(- \infin) = 0 \newline
\Phi(+ \infin) = 1 \newline
\Phi(x) > \Phi(y) \; \forall \; x > y
$$

The *inverse cummulative distribution function* (ICDF) $\Phi^{-1}(p)$, also known as *quantile function* (QF) $Q(p)$ is defined on the interval $[0, 1]$ as the value *x* of the random variable *X* for which the cummulative probability $\Phi(x) = \mathtt{Pr}[X \leq x] = p$. Naturally, the this function has the following properties:

$$
\Phi^{-1}(p) \in \mathbb{R} \; \forall \; p \in [0, 1] \newline
\Phi^{-1}(0) = - \infin \newline
\Phi^{-1}(1) = + \infin \newline
\Phi^{-1}(p) > \Phi^{-1}(q) \; \forall \; p > q \newline
\Phi(\Phi^{-1}(p)) = p \newline
\Phi^{-1}(\Phi(x)) = x
$$

This function allows calcualtion of a generic quantile as:

$$
Q_{m}^{k} = Q(\frac{k}{m}) \equiv \Phi^{-1}(\frac{k}{m}) \Rightarrow \newline
\mathtt{Median} = \Phi^{-1}(0.5) \newline
\mathtt{Q1} = Q_{4}^{1} = \Phi^{-1}(0.25) \newline
\mathtt{Q3} = Q_{4}^{3} =\Phi^{-1}(0.75)
$$

## Gaussian distribution and Z-distribution

The generic *Gaussian distribution*, a.k.a. *normal distribution*, is characterized by its *mean* value $\mu$ and *standard deviation* $\sigma$. Its PDF ans CDF are:

$$
f(x) = \frac{1}{\sigma \sqrt{2 \pi}} \times e^{- \frac{1}{2} \left( \frac{x - \mu}{\sigma} \right)^2} \newline
\Phi(x) = \frac{1}{2} \left[ 1 + \mathtt{erf} \left( \frac{x -\mu}{\sigma \sqrt{2}} \right) \right]
$$

where the *error function* erf() is defined as:

$$
\mathtt{erf}(z > 0) = \frac{2}{\sqrt{\pi}} \int_0^z {e^{- t^2} dt} \newline
\mathtt{erf}(0) = 0 \newline
\mathtt{erf}(z < 0) = - \mathtt{erf}(-z)
$$

**Note** that both the *exponent* and the *error function* are implemented in the module *math* of the Standard Python Library.

The ICDF / QF function is:

$$
\Phi^{-1}(p) = \mu + \sigma \sqrt{2} \mathtt{erf}^{-1}(2p-1)
$$

The *inverse error function* is not part of the Standard Python Library, and it must be implemented among other *special functions* (see [DE003](./DE003_special_functions.md) document).

The Gaussian distribution has the following statistical properties:

* Mean is $\mu$
* Variance is $\sigma^2$
* Skewness is 0
* Excess kurtosis is 0
* Median is $\mu$
* The first quartile Q1 is $\mu - \sigma \sqrt{2} \mathtt{erf}^{-1}(0.5)$
* The third quartile Q3 is $\mu + \sigma \sqrt{2} \mathtt{erf}^{-1}(0.5)$

**Note** that the value of $\sqrt{2} \mathtt{erf}^{-1}(0.5)$ can be pre-calculated in advance, thus all of these properties can be expressed solely in terms of the *parameters* of the distibution.

The Z-distribuion, a.k.a. *standard normal distribution*, is a special case of $\mu$ = 0 and $\sigma$ = 1.

The Gaussian distribution is important due to two facts:

* Many naturally occuring process show Gaussian distribution or a distribution, which can be closely approximated by a Gaussian one
* *Central Limit Theorem*, with the important practical consequence of which being that the distribution of the *samples means* of independent and identically distributed random variable with finite variance *converge* to a normal distribution

The second point is the core of Z-test, which compares the obtained sample mean with the known population mean as long as the population variance is known as well.

## Student's t-distribution

## Chi-squared distribution

## F-distribution

## Poisson distribution

## Binomial distribution

## Hypergeometric distribution
