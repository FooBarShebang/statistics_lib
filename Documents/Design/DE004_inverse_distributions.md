# Definition and properties of the inverse distributions

## Introduction

This document provides definition and properties of the inverse distributions. In simple terms, such distributions describe the distribution of the values *reciprocal* to those sampled from a randomly distributed population.

For example, consider a drift of charged particles in a medium in constant electric field. On average, all particles move with a *drift speed u* defined by their *mobility*, however, this motion is also disturbed by the Brownian motion due to collisions with non-stationary particles, which can be approximated by the Gaussian distribution. Thus, for a given period of time *t* the displacement of particles is distributed as:

$$
X_t = u \times t + \sigma \times W_t \sim \mathbb{N}(u \times t, \sigma^2 \times t)
$$

where $W_t \sim \mathbb{N}(0, t)$ is, so called Wiener process, normally distributed with the zero mean and standard deviation *t*. Thus, the displacement of the particles over the period of time *t* is normally distributed with the both *mean* and *standard deviation* increasing directly proportional to the time. The *inverse Gaussian distribution* arises concerning the distribution of the time required for a particle to reach distance *x*. Without the influence of the Brownian process the drift time would have been $t = \frac{x}{u}$, however, due to the impact of the random collisions (Brownian process) the actual arrival time will be randomly distributed. Further more, some of the particles may not reach that point at all, if the Brownian motion overcomes the drift. However, the distribution of the *first passage time* (i.e. time when the first particle from multiple emitted reaches the target) is well defined as an inverse Gaussian distribution:

$$
T_{\alpha} = \mathtt{inf} \lbrace t>0 | X_t =\alpha\rbrace \sim \mathtt{IG}\left( \frac{\alpha}{u}, \left(\frac{\alpha}{\sigma}\right)^2 \right)
$$

In general, the *inverse distributions* are special cases of *ratio distributions* with the constant numerator being an *degenerate distributed* random variable. The *ratio distributions* describe the distribution of a random variable constructed as a ratio of two indepenended random variables with the known distributions. For instance, if *X* follows the standard normal distribution $\mathbb{N}(0,1)$ and *Y* follows chi-squared distribution with *n* degrees of freedom, then $Z = \frac{X}{\sqrt{Y/n}}$ follows Student's t-distribution with *n* degrees of freedom (see [DE002](./DE002_continuous_distributions.md)). If *X* and *Y* are ch-squared distributed with *n* and *m* degrees of freedom, then $Z = \frac{X/n}{Y/m}$ if F-distributed with *n* and *m* degrees of freedom (see [DE002](./DE002_continuous_distributions.md)).

The inverse distributions are not required for the statistical testing usually, however they may be helpfull for the analysis of the shape of the sample's distribution.

## Inverse Gaussian distribituion

The inverse Gaussian distribution $\mathtt{IG}(\mu, \lambda)$ has two parameters:

* Mean $\mu > 0$, and
* Shape $\lambda > 0$

and it is defined for $x \in (0, + \infin)$. Its PDF and CDF are:

$$
f(x) = \sqrt{\frac{\lambda}{2 \pi x^3}} \mathtt{exp}\left[ - \frac{\lambda (x - \mu)^2}{2 \mu^2 x} \right] \newline
\Phi(x) = \Phi_G\left( \sqrt{\frac{\lambda}{x}} \left( \frac{x}{\mu} - 1\right) \right) + \mathtt{exp}\left[ \frac{2 \lambda}{\mu} \right] \Phi_G\left( - \sqrt{\frac{\lambda}{x}} \left( \frac{x}{\mu} + 1\right) \right) \; \mathtt{where} \newline
\Phi_G(z) = \frac{1}{2} \left[ 1 + \mathtt{erf} \left( \frac{z}{\sqrt{2}} \right) \right]
$$

The QF should be calculated numerically using bi-section, therefore, the median and the first and the third quartiles. However, the following statistical properties have simple forms:

* Mean is $\mu$
* Variance is $\frac{\mu^3}{\lambda}$
* Skewness is $3 \sqrt{\frac{\mu}{\lambda}}$
* Excess kurtosis is $15 \frac{\mu}{\lambda}$

The meaning and application of this distribution is discussed above (in the *Introduction* section).

## Inverse Gamma distribution

The inverse Gamma distribution has two parameters:

* Shape $\alpha > 0$, and
* Scale $\beta > 0$

and it is defined for $x \in (0, + \infin)$. Its PDF and CDF are:

$$
f(x) = \frac{\beta^\alpha}{\Gamma(\alpha)} x^{-\alpha - 1} \mathtt{exp}\left( -\frac{\beta}{x} \right) \newline
\Phi(x) = \frac{\Gamma(\alpha, \frac{\beta}{x})}{\Gamma(\alpha)} = Q(\alpha, \frac{\beta}{x})
$$

where *Q*() is the *regularized upper incomplete gamma function* (see [DE003](./DE003_special_functions.md) document). The QF should be calculated numerically using bi-section, therefore, the median and the first and the third quartiles. However, the following statistical properties have simple forms:

* Mean is $\frac{\beta}{\alpha - 1}$ for $\alpha > 1$, and undefined otherwise
* Variance is $\frac{\beta^2}{(\alpha - 1)^2 (\alpha - 2)}$ for $\alpha > 2$, and undefined otherwise
* Skewness is $\frac{4 \sqrt{\alpha - 2}}{\alpha - 3}$ for $\alpha > 3$, and undefined otherwise
* Excess kurtosis is $\frac{6 (5 \alpha - 11)}{(\alpha - 3) (\alpha - 4)}$ for $\alpha > 4$, and undefined otherwise

The Gamma distribution is related to many other disributions, for instance, the distribution of the sample mean of *exponential distribution* follows Gamma distribution, etc. In fact, the *exponentail distribution* itself is a special case of Gamma distribution as well as *chi-squared distribution*. Thus, the *inverse Gamma distribution* is a convenient fitting model for the description of the reciprocal of random values in many cases.

## Inverse chi-squared distribution

The inverse chi-squared distribution has a single parameter: degree of freedoms $\nu > 0$, and it is defined for $x \in (0, + \infin)$. Its PDF and CDF are:

$$
f(x) = \frac{2^{ - \nu /2}}{\Gamma(\frac{\nu}{2})} x^{-\nu /  2 - 1} \mathtt{exp}\left( -\frac{1}{2x} \right) \newline
\Phi(x) = \frac{\Gamma(\frac{\nu}{2}, \frac{1}{2x})}{\Gamma(\frac{\nu}{2})} = Q(\frac{\nu}{2}, \frac{1}{2x})
$$

The QF should be calculated numerically using bi-section, therefore, the median and the first and the third quartiles. However, the following statistical properties have simple forms:

* Mean is $\frac{1}{\nu - 2}$ for $\nu > 2$, and undefined otherwise
* Variance is $\frac{2}{(\nu - 2)^2 (\nu - 4)}$ for $\nu > 4$, and undefined otherwise
* Skewness is $\frac{4 \sqrt{2 (\nu - 4)}}{\nu - 6}$ for $\nu > 6$, and undefined otherwise
* Excess kurtosis is $\frac{12 (5 \nu - 22)}{(\nu - 6) (\nu - 8)}$ for $\nu > 8$, and undefined otherwise

The inverse chi-squared distribution is a special case of the inverse Gamma distribution with $\alpha = \frac{\nu}{2}$ and $\beta = \frac{1}{2}$. It describes the distribution of the reciprocal of the sum of the squared values of a sample taken from a random variable following standard normal distribution $\mathbb{N}(0, 1)$.

## Scaled inverse chi-squared distribution

The inverse Gamma distribution has two parameters:

* Degree of freedoms $\nu > 0$
* Scale $\tau^2 > 0$

and it is defined for $x \in (0, + \infin)$. Its PDF and CDF are:

$$
f(x) = \frac{\left({\frac{\tau^2 \nu}{2}}\right)^{ \nu /2}}{\Gamma(\frac{\nu}{2})} x^{-\nu /  2 - 1} \mathtt{exp}\left( -\frac{\nu \tau^2}{2x} \right) \newline
\Phi(x) = \frac{\Gamma(\frac{\nu}{2}, \frac{\tau^2 \nu}{2x})}{\Gamma(\frac{\nu}{2})} = Q(\frac{\nu}{2}, \frac{\tau^2 \nu}{2x})
$$

The QF should be calculated numerically using bi-section, therefore, the median and the first and the third quartiles. However, the following statistical properties have simple forms:

* Mean is $\frac{\nu \tau^2}{\nu - 2}$ for $\nu > 2$, and undefined otherwise
* Variance is $\frac{2 \nu^2 \tau^4}{(\nu - 2)^2 (\nu - 4)}$ for $\nu > 4$, and undefined otherwise
* Skewness is $\frac{4 \sqrt{2 (\nu - 4)}}{\nu - 6}$ for $\nu > 6$, and undefined otherwise
* Excess kurtosis is $\frac{12 (5 \nu - 22)}{(\nu - 6) (\nu - 8)}$ for $\nu > 8$, and undefined otherwise

The scaled inverse chi-squared distribution is a special case of the inverse Gamma distribution with $\alpha = \frac{\nu}{2}$ and $\beta = \frac{\nu \tau^2}{2}$. It describes the distribution of the reciprocal of the mean of the squared values of a sample taken from a random variable following normal distribution with zero mean $\mathbb{N}(0, \sigma)$, where $\tau^2 = 1 / \sigma^2$.

## Cauchy distribution

The Cauchy distribution has two parameters:

* Location $x_0 \in \mathbb{R}$, and
* Scale $\gamma > 0$

and it is defined for $x \in (- \infin, + \infin)$. Its PDF, CDF and QF are:

$$
f(x) = \frac{1}{\pi \gamma\left[ 1 + \left( \frac{x - x_0}{\gamma} \right)^2 \right]}  \newline
\Phi(x) = \frac{1}{\pi} \mathtt{arctan} \left( \frac{x - x_0}{\gamma} \right) + \frac{1}{2}\newline
\Phi^{-1}(p) = x_0 + \gamma * \mathtt{tan}\left( \pi \left( p - \frac{1}{2} \right) \right)
$$

Its basic statistical properties related to the moments are not defined, including mean, variance, standard deviation, skewness and kurtosis. However, the following statistical properties - quartiles - have simple forms:

* Median is $x_0$
* The first quartile is $x_0 - \gamma$
* The third quartile is $x_0 + \gamma$

The Cauchy distribution, also known as Lorenz distribution or Cauchy-Lorenz distribution describes the distribution of the x-intercepts of the rays emitted from the point $(x_0, \gamma)$ with the uniform distribution of an angle, in other words, the transformation $\mathbb{R} \rightarrow \mathtt{tan}(\mathbb{R})$. It is not, *per se*, an inverse distribution, but in the special case of $x_0 = 0$ it does describe the distribution of the *ratio* of two random normally distributed variables with zero means. Cauchy distribution is also a special case of non-standardized Student's t-distribution with 1 degree of freedom, or just Student's with $x_0 = 0$ and $\gamma = 1$.

## Levy distribution

The inverse Gamma distribution has two parameters:

* Location $\mu \in \mathbb{R}$, and
* Scale $\sigma > 0$

and it is defined for $x \in [\mu, + \infin)$. Its PDF, CDF and QF are:

$$
f(x) = \sqrt{\frac{\sigma}{2 \pi}} \times \frac{\mathtt{exp}\left( -\frac{\sigma}{2 (x - \mu)} \right)}{(x - \mu)^{3/2}} \newline
\Phi(x) = 1 - \mathtt{erf}\left( \sqrt{\frac{\sigma}{2 (x - \mu)}}\right) \newline
\Phi^{-1}(p) = \mu + \frac{\sigma}{2 (\mathtt{erf}^{-1}(1 - p))^2}
$$

Its mean, variance and standard deviation are infinite, whereas its skewness and kurtosis are not defined. However, the following statistical properties - quartiles - have simple forms:

* Median is $\mu + \frac{\sigma}{2 (\mathtt{erf}^{-1}(0.5))^2} \approx \mu + \sigma * 2.198109338$
* The first quartile is $\mu + \frac{\sigma}{2 (\mathtt{erf}^{-1}(0.75))^2} \approx \mu + \sigma * 0.75568443$
* The third quartile is $\mu + \frac{\sigma}{2 (\mathtt{erf}^{-1}(0.25))^2} \approx \mu + \sigma * 9.849204322$

The Levy distribution has applications in description of different stochastic processes in physics, e.g. as the limit case of the *inverse Gaussian distribution* describing the Brownian motion with zero drift speed. Furthermore, with a trivial substitution $x - \mu \rightarrow y$ it becomes a special case of the *inverse Gamma distribution* with $\alpha = \frac{1}{2}$ and $\beta = \frac{\sigma}{2}$. Also note that for a random variable $X \sim \mathbb{N}(\mu, \sigma_0)$ the values $(X - \mu)^{-2}$ follow Levy distribution with $x_0 = 0$ and $\sigma = 1 / \sigma_0^2$.
