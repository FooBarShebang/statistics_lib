#usr/bin/python3
"""
Module statistics_lib.special_functions

Implements special functions required for the implementation of the pdf(), cdf()
and qf() methods of the random distribution classes.

Functions:
    permutation(n, k)
        int >= 0, int >= 0 -> int > 0
    combination(n, k)
        int >= 0, int >= 0 -> int > 0
    log_beta(x, y)
        int > 0 OR float > 0, int > 0 OR float > 0 -> float
    beta(x, y)
        int > 0 OR float > 0, int > 0 OR float > 0 -> float > 0
    inv_erg(x)
        -1 < int < 1 OR -1 < float < 1 -> float
    lower_gamma(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> float >= 0
    log_lower_gamma(x, y)
        int > 0 OR float > 0, int > 0 OR float > 0 -> float
    lower_gamma_reg(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> 0 <= float < 1
    upper_gamma(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> float > 0
    log_upper_gamma(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> float
    upper_gamma_reg(x, y)
        int > 0 OR float > 0, int >= 0 OR float > 0 -> 0 < float <= 1
    incomplete_beta(z, x, y)
        0 <= int <= 1 OR 0 <= float <= 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> float >= 0
    log_incomplete_beta(z, x, y)
        int = 1 OR 0 < float <= 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> float
    incomplete_beta_reg(z, x, y)
        0 <= int <= 1 OR 0 <= float <= 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> 0 <= float <= 1
"""

__version__= '1.0.0.0'
__date__ = '06-04-2022'
__status__ = 'Testing'

#imports

#+ standard library

import sys
import os
import math
import functools

import collections.abc as c_abc

from typing import Union, Sequence

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#globals

#+ types

TReal = Union[int, float]

#+ helper constants

PYTHON_MAJOR = sys.version_info[0]

PYTHON_MINOR = sys.version_info[1]

IS_V3_8_PLUS = (PYTHON_MAJOR >= 3) and (PYTHON_MINOR >= 8)

#+ polynomials coefficients

#++ inverse error function

#+++ interval [-0.850, 0.850]

P0_INV_ERF = (
    2.5090809287301226727E3,
    3.3430575583588128105E4,
    6.7265770927008700853E4,
    4.5921953931549871457E4,
    1.3731693765509461125E4,
    1.9715909503065514427E3,
    1.3314166789178437745E2,
    3.3871328727963666080E0,
)

Q0_INV_ERF = (
    5.2264952788528545610E3,
    2.8729085735721942674E4,
    3.9307895800092710610E4,
    2.1213794301586595867E4,
    5.3941960214247511077E3,
    6.8718700749205790830E2,
    4.2313330701600911252E1,
    1.0000000000000000000E0,
)

#+++ intervals [ - (1 - 2.77759E-11), -0.850) and (0.850, 1 - 2.77759E-11]

P1_INV_ERF = (
    7.74545014278341407640E-4,
    2.27238449892691845833E-2,
    2.41780725177450611770E-1,
    1.27045825245236838258E0,
    3.64784832476320460504E0,
    5.76949722146069140550E0,
    4.63033784615654529590E0,
    1.42343711074968357734E0,
)

Q1_INV_ERF = (
    1.05075007164441684324E-9,
    5.47593808499534494600E-4,
    1.51986665636164571966E-2,
    1.48103976427480074590E-1,
    6.89767334985100004550E-1,
    1.67638483018380384940E0,
    2.05319162663775882187E0,
    1.0000000000000000000E0,
)

#+++ intervals (-1, - (1 - 2.77759E-11)) and (1 - 2.77759E-11, 1)

P2_INV_ERF = (
    2.01033439929228813265E-7,
    2.71155556874348757815E-5,
    1.24266094738807843860E-3,
    2.65321895265761230930E-2,
    2.96560571828504891230E-1,
    1.78482653991729133580E0,
    5.46378491116411436990E0,
    6.65790464350110377720E0,
)

Q2_INV_ERF = (
    2.04426310338993978564E-15,
    1.42151175831644588870E-7,
    1.84631831751005468180E-5,
    7.86869131145613259100E-4,
    1.48753612908506148525E-2,
    1.36929880922735805310E-1,
    5.99832206555887937690E-1,
    1.0000000000000000000E0,
)

#+ precision and iteration related

ITMAX = 10000 #maximum length of the iteration loop, 100 in the original
#+ algorithm

EPS = 3.0E-7 #relative precision of series convergence criteria

FPMIN = 1.0E-60 #proxy for the smallest representative floating point number,
#+ affectes the precision . In the original algorithm it is 1.0E-30 - near
#+ single precision float min value; no reason to set it near 2.2E-308 for
#+ double precision.

#functions

#+ helper functions

def _evaluatePolynomial(x: TReal, Coefficients: Sequence[TReal]) -> TReal:
    """
    Evaluates a polynomial a0 + a1 * x + a2 * x^2 + ... + aN * x^N using the
    itterative approach as:
        p = aN-1 + x * aN
        p = aN-2 + x * p
        p = aN-3 + x * p
        ...
        p = a1 + x * p
        p = a0 + x * p
    
    The list of the coefficients must be passed in the order aN to a0.
    
    Signature:
        int OR float, seq(int OR float) -> int OR float
    
    Args:
        x: int OR float; value at which the polynomial is evaluated
        Coefficients: seq(int OR float); list of the coefficients in the inverse
            order - from the highest power to the lowest
    
    Raises:
        UT_TypeError: the value is not a real number, or the list of the
            coefficients is not a sequence of real numbers
        UT_ValueError: the list of coefficients is an empty sequence
    
    Version 1.0.0.0
    """
    if not isinstance(x, (int, float)):
        raise UT_TypeError(x, (int, float))
    if ((not isinstance(Coefficients, c_abc.Sequence))
                                            or isinstance(Coefficients, str)):
        raise UT_TypeError(Coefficients, c_abc.Sequence)
    Length = len(Coefficients)
    if Length == 0:
        raise UT_ValueError(Length, '> 0 - length of the coefficients sequence')
    for Index, Item in enumerate(Coefficients):
        if not isinstance(Item, (int, float)):
            error = UT_TypeError(Item, (int, float))
            error.args = ('{} in sequence at position {}'.format(error.args[0],
                                                                    Index), )
            raise error
    if Length == 1: #zero power polynomial
        Result = Coefficients[0]
    else: #1st or higher power polynomial
        Result = Coefficients[1] + x * Coefficients[0]
        for Index in range(2, Length):
            Result = Coefficients[Index] + x * Result
    return Result

def _evaluateRational(x: TReal, P: Sequence[TReal], Q: Sequence[TReal])-> TReal:
    """
    Evaluates the value of a rational function R(x) = P(x) / Q(x), where
    P(x) and Q(x) are polynomials, i.e. P(x) = p0 + p1 * x + ... pN * x^N and
    Q(x) = q0 + q1 * x + ... + qM * x^M
    
    The lists of the coefficients must be passed in the order pN to p0 and
    qM to q0.
    
    Signature:
        int OR float, seq(int OR float), seq(int OR float) -> int OR float
    
    Args:
        x: int OR float; value at which the polynomial is evaluated
        P: seq(int OR float); list of the coefficients in the inverse
            order - from the highest power to the lowest - for the divident
        Q: seq(int OR float); list of the coefficients in the inverse
            order - from the highest power to the lowest - for the divider
    
    Raises:
        UT_TypeError: the value is not a real number, or any list of the
            coefficients is not a sequence of real numbers
        UT_ValueError: any list of coefficients is an empty sequence
    
    Version 1.0.0.0
    """
    Divident = _evaluatePolynomial(x, P)
    Divider = _evaluatePolynomial(x, Q)
    Result = Divident / Divider
    return Result

#++ rational approximations for the inverse error function

#+++ central part abs(x) <= 0.85

_InvErfRat0 = functools.partial(_evaluateRational, P= P0_INV_ERF, Q= Q0_INV_ERF)

#+++ tails  0.85 < abs(x) <= 1 - 2.77759E-11

_InvErfRat1 = functools.partial(_evaluateRational, P= P1_INV_ERF, Q= Q1_INV_ERF)

#+++ far tails 1 - 2.77759E-11 < abs(x) < 1

_InvErfRat2 = functools.partial(_evaluateRational, P= P2_INV_ERF, Q= Q2_INV_ERF)

def _gammaSeries(x: TReal, y : TReal) -> float:
    """
    Calculates the series part of the lower incomplete gamma function. Note,
    that the data sanity check is not implemented, but it is supposed to be
    incorporated into the higher abstraction level functions.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 216-219. ISBN: 0-521-43108-5
    
    Signature:
        int > 0 OR float > 0, int > 0 OR float > 0 -> float > 0
    
    Args:
        x: int > 0 OR float > 0; power parameter of the function
        y: int > 0 OR float > 0; the integeral boundary parameter of the
            function
    
    Raises:
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    Coeff = x
    Term = 1.0 / x
    Sum = Term
    for n in range(1, ITMAX):
        Coeff += 1
        Term *= y / Coeff
        Sum += Term
        if math.fabs(Term) < EPS * math.fabs(Sum):
            break
    else: #max number of iterations is reached - error
        raise Exception('Unable to converge the gamma series')
    return Sum

def _gammaContFraction(x: TReal, y : TReal) -> float:
    """
    Calculates the continued fraction part of the upper incomplete gamma
    function. Note, that the data sanity check is not implemented, but it is
    supposed to be incorporated into the higher abstraction level functions.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 216-219. ISBN: 0-521-43108-5
    
    Signature:
        int > 0 OR float > 0, int > 0 OR float > 0 -> float > 0
    
    Args:
        x: int > 0 OR float > 0; power parameter of the function
        y: int > 0 OR float > 0; the integeral boundary parameter of the
            function
    
    Raises:
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    b = 1.0 + y - x
    c = 1.0 / FPMIN
    d = 1.0 / b
    h = d
    for i in range(1, ITMAX):
        an = - i * (i - x)
        b += 2.0
        d = an * d + b
        if (math.fabs(d) < FPMIN):
            d = FPMIN
        c = b + an / c
        if (math.fabs(c) < FPMIN):
            c = FPMIN
        d = 1.0 / d
        res = d * c
        h *= res
        if math.fabs(res - 1.0) < EPS:
            break
    else: #max number of iterations is reached - error
        raise Exception('Unable to converge the gamma series')
    return h

def _betaContFraction(z: float, x: TReal, y : TReal) -> float:
    """
    Calculates the continued fraction part of the incomplete beta function.
    Note, that the data sanity check is not implemented, but it is supposed to
    be incorporated into the higher abstraction level functions.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 226-228. ISBN: 0-521-43108-5
    
    Signature:
        0 < float < 1, int > 0 OR float > 0, int > 0 OR float > 0 -> float > 0
    
    Args:
        z: 0 < float < 1; the integeral boundary parameter of the function
        x: int > 0 OR float > 0; the first power parameter of the function
        y: int > 0 OR float > 0; the second power parameter of the function
    
    Raises:
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    qab = x + y
    qap = x + 1.0
    qam = x - 1.0
    c = 1.0
    d = 1.0 - qab * z / qap
    if (math.fabs(d) < FPMIN):
        d = FPMIN
    d = 1.0 / d
    h = d
    for m in range(1, ITMAX):
        m2 = 2 * m
        aa = m * (y - m) * z / ((qam + m2) * (x + m2))
        d = 1.0 + aa * d
        if (math.fabs(d) < FPMIN):
            d = FPMIN
        c = 1.0 + aa / c
        if (math.fabs(c) < FPMIN):
            c = FPMIN
        d = 1.0 / d
        h *= d * c
        aa = - (x + m) * (qab + m) * z / ((x + m2) * (qap + m2))
        d = 1.0 + aa * d
        if (math.fabs(d) < FPMIN):
            d = FPMIN
        c = 1.0 + aa / c
        if (math.fabs(c) < FPMIN):
            c = FPMIN
        d = 1.0 / d
        res = d * c
        h *= res
        if math.fabs(res - 1.0) < EPS:
            break
    else: #max number of iterations is reached - error
        raise Exception('Unable to converge the gamma series')
    return h

def _checkSanity1(n: int, k: int) -> None:
    """
    Performs the input data sanity check - the both arguments must be positive
    real numbers, with the relation 0 <= k <= n
    
    Signature:
        int >= 0, int >= 0 -> None
    
    Raises:
        UT_TypeError: either of the arguments is not an integer
        UT_ValueError: either of the arguments is negative, OR k > n
    
    Version 1.0.0.0
    """
    if not isinstance(n, int):
        raise UT_TypeError(n, int, SkipFrames = 2)
    if not isinstance(k, int):
        raise UT_TypeError(k, int, SkipFrames = 2)
    if n < 0:
        raise UT_ValueError(n, '>= 0, number of objects', SkipFrames = 2)
    if k < 0:
        raise UT_ValueError(k, '>= 0, number of trials', SkipFrames = 2)
    if k > n:
        raise UT_ValueError(k,
                    '<= {}, number of trials <= number of objects'.format(n),
                                                                SkipFrames = 2)

def _checkSanity2(x: TReal, y: TReal) -> None:
    """
    Performs the input data sanity check - the both arguments must be positive
    real numbers.
    
    Signature:
        int > 0 OR float > 0, int > 0 OR float > 0 -> None
    
    Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: either of the arguments is zero or negative
    
    Version 1.0.0.0
    """
    if not isinstance(x, (int, float)):
        raise UT_TypeError(x, (int, float), SkipFrames = 2)
    if not isinstance(y, (int, float)):
        raise UT_TypeError(y, (int, float), SkipFrames = 2)
    if x <= 0:
        raise UT_ValueError(x, '> 0, x argument', SkipFrames = 2)
    if y <= 0:
        raise UT_ValueError(y, '> 0, y argument', SkipFrames = 2)

def _checkSanity3(x: TReal, y: TReal) -> None:
    """
    Performs the input data sanity check - the first argument must be positive
    real number, and the second - non-negative real number.
    
    Signature:
        int > 0 OR float > 0, int >= 0 OR float > 0 -> None
    
    Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: either of the arguments is zero or negative
    
    Version 1.0.0.0
    """
    if not isinstance(x, (int, float)):
        raise UT_TypeError(x, (int, float), SkipFrames = 2)
    if not isinstance(y, (int, float)):
        raise UT_TypeError(y, (int, float), SkipFrames = 2)
    if x <= 0:
        raise UT_ValueError(x, '> 0, x argument', SkipFrames = 2)
    if y < 0:
        raise UT_ValueError(y, '>= 0, y argument', SkipFrames = 2)

def _checkSanity4(z: TReal, x: TReal, y: TReal) -> None:
    """
    Performs the input data sanity check - the first argument must be a real
    number in the closed range [0, 1], the other two arguments must be positive
    real numbers.
    
    Signature:
        0 <= int <= 1 OR 0 <= float <= 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> None
    
    Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: the first argument is not in the range [0, 1], OR either
            of the other arguments is zero or negative
    
    Version 1.0.0.0
    """
    if not isinstance(z, (int, float)):
        raise UT_TypeError(z, (int, float), SkipFrames = 2)
    if not isinstance(x, (int, float)):
        raise UT_TypeError(x, (int, float), SkipFrames = 2)
    if not isinstance(y, (int, float)):
        raise UT_TypeError(y, (int, float), SkipFrames = 2)
    if z < 0 or z > 1:
        raise UT_ValueError(z, 'in range [0, 1], z argument', SkipFrames = 2)
    if x <= 0:
        raise UT_ValueError(x, '> 0, x argument', SkipFrames = 2)
    if y <= 0:
        raise UT_ValueError(y, '> 0, y argument', SkipFrames = 2)

#+ main set of functions

def permutation(n: int, k: int) -> int:
    """
    Calculates 'n permute k' value, i.e. n! / (n-k)!

    Signature:
        int >= 0 , int >= 0 -> int > 0
    
    Args:
        n: int >= 0; the total number of objects available
        k: int >= 0; the number of objects taken
    
    Raises:
        UT_TypeError: either of the arguments is not integer
        UT_ValueError: either of the arguments is negative, or k > n
    
    Version 1.0.0.0
    """
    _checkSanity1(n, k)
    if IS_V3_8_PLUS:
        Result = math.perm(n, k)
    else:
        if k > 0:
            Result = n
            for i in range(1, k):
                Result *= (n - i)
        else:
            Result = 1
    return Result

def combination(n: int, k: int) -> int:
    """
    Calculates 'n chose k' value, i.e. n! / ((n-k)! k!)

    Signature:
        int >= 0 , int >= 0 -> int > 0
    
    Args:
        n: int >= 0; the total number of objects available
        k: int >= 0; the number of objects taken
    
    Raises:
        UT_TypeError: either of the arguments is not integer
        UT_ValueError: either of the arguments is negative, or k > n
    
    Version 1.0.0.0
    """
    _checkSanity1(n, k)
    if IS_V3_8_PLUS:
        Result = math.comb(n, k)
    else:
        if k > n - k:
            Result = permutation(n, n - k) // math.factorial(n - k)
        else:
            Result = permutation(n, k) // math.factorial(k)
    return Result

def log_beta(x: TReal, y: TReal) -> float:
    """
    The value of the natural logarithm of beta function ln(B(x, y)).

    Signature:
        int > 0 OR float > 0, int > 0 OR float > 0 -> float
    
    Args:
        x: int >0 OR float > 0; any real number first argument
        y: int >0 OR float > 0; any real number second argument
    
    Raises:
        UT_TypeError: either of the arguments is not integer or float
        UT_ValueError: either of the arguments is not positive
    
    Version 1.0.0.0
    """
    _checkSanity2(x, y)
    Result = math.lgamma(x) + math.lgamma(y) - math.lgamma(x + y)
    return Result

def beta(x: TReal, y: TReal) -> float:
    """
    The value of beta function B(x, y).

    Signature:
        int > 0 OR float > 0, int > 0 OR float > 0 -> float > 0
    
    Args:
        x: int >0 OR float > 0; any real number first argument
        y: int >0 OR float > 0; any real number second argument
    
    Raises:
        UT_TypeError: either of the arguments is not integer or float
        UT_ValueError: either of the arguments is not positive
    
    Version 1.0.0.0
    """
    _checkSanity2(x, y)
    Result = math.lgamma(x) + math.lgamma(y) - math.lgamma(x + y)
    return math.exp(Result)

def inv_erf(x: TReal) -> float:
    """
    Calculates the value of the inverse error function of the given argument.
    
    Based on the algorithm given in:
    
    Michael J. Wichura. Algorithm AS241: The Percentage Points of the Normal
    Distribution. Journal of Royal Statistical Society. Series C (Applied
    Statistics), Vol. 37, No. 3 (1988), pp. 477-484
    
    which is 3 ranges rational function approximation with double precision
    (7th power polynomials).
    
    Signature:
        -1 < int < 1 OR -1 < float < 1 -> float
    
    Args:
        x: -1 < int < 1 OR -1 < float < 1; the function argument
    
    Raises:
        UT_TypeError: the argument is not integer or float
        UT_ValueError: the argument is not in the range (-1, 1)
    
    Version 1.0.0.0
    """
    Split1 = 0.425E0
    Const1 = 0.180625E0
    Split2 = 5.0E0
    Const2 = 1.6E0
    if not isinstance(x, (int, float)):
        raise UT_TypeError(x, (int, float), SkipFrames = 1)
    if (x >= 1) or (x <= -1):
        raise UT_ValueError(x, 'in range (-1, 1)', SkipFrames = 1)
    q = 0.5 * x
    if abs(q) <= Split1:
        r = Const1 - q*q
        Result = q * _InvErfRat0(r)
    else:
        if x < 0:
            r = math.sqrt(- math.log(0.5 * (x + 1.0)))
        else:
            r = math.sqrt(- math.log(0.5 * (1.0 - x)))
        if r <= Split2:
            r -= Const2
            Result = _InvErfRat1(r)
        else:
            r -= Split2
            Result = _InvErfRat2(r)
        if x < 0:
            Result = - Result
    return Result / math.sqrt(2)

def lower_gamma(x: TReal, y : TReal) -> float:
    """
    Calculates the lower incomplete gamma function.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 216-219. ISBN: 0-521-43108-5
    
    Signature:
        int > 0 OR float > 0, int >= 0 OR float > 0 -> float >= 0
    
    Args:
        x: int > 0 OR float > 0; power parameter of the function
        y: int >= 0 OR float > 0; the integeral boundary parameter of the
            function
    
    Raises:
        Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: either of the arguments is zero or negative
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    _checkSanity3(x, y)
    if y == 0:
        Result = 0.0
    elif (y < x + 1.0):
        Sum = _gammaSeries(x, y)
        Result = math.exp(-y + x * math.log(y)) * Sum
    else:
        Sum = _gammaContFraction(x, y)
        GammaLn = math.lgamma(x)
        Factor = math.exp(-y + x * math.log(y) - GammaLn)
        Result = math.exp(GammaLn + math.log(1 - Factor * Sum))
    return Result

def log_lower_gamma(x: TReal, y : TReal) -> float:
    """
    Calculates the natural logarithm of the lower incomplete gamma function.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 216-219. ISBN: 0-521-43108-5
    
    Signature:
        int > 0 OR float > 0, int > 0 OR float > 0 -> float
    
    Args:
        x: int > 0 OR float > 0; power parameter of the function
        y: int > 0 OR float > 0; the integeral boundary parameter of the
            function
    
    Raises:
        Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: either of the arguments is zero or negative
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    _checkSanity2(x, y)
    if (y < x + 1.0):
        Sum = _gammaSeries(x, y)
        Result = -y + x * math.log(y) + math.log(Sum)
    else:
        Sum = _gammaContFraction(x, y)
        GammaLn = math.lgamma(x)
        Factor = math.exp(-y + x * math.log(y) - GammaLn)
        Result = GammaLn + math.log(1 - Factor * Sum)
    return Result

def lower_gamma_reg(x: TReal, y : TReal) -> float:
    """
    Calculates the regularized lower incomplete gamma function.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 216-219. ISBN: 0-521-43108-5
    
    Signature:
        int > 0 OR float > 0, int >= 0 OR float > 0 -> 0 <= float < 1
    
    Args:
        x: int > 0 OR float > 0; power parameter of the function
        y: int >= 0 OR float > 0; the integeral boundary parameter of the
            function
    
    Raises:
        Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: either of the arguments is zero or negative
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    _checkSanity3(x, y)
    if y == 0:
        Result = 0.0
    else:
        GammaLn = math.lgamma(x)
        Factor = math.exp(-y + x * math.log(y) - GammaLn)
        if (y < x + 1.0):
            Sum = _gammaSeries(x, y)
            Result = Factor * Sum
        else:
            Sum = _gammaContFraction(x, y)
            Result = 1 - Factor * Sum
    return Result

def upper_gamma(x: TReal, y : TReal) -> float:
    """
    Calculates the upper incomplete gamma function.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 216-219. ISBN: 0-521-43108-5
    
    Signature:
        int > 0 OR float > 0, int >= 0 OR float > 0 -> float > 0
    
    Args:
        x: int > 0 OR float > 0; power parameter of the function
        y: int >= 0 OR float > 0; the integeral boundary parameter of the
            function
    
    Raises:
        Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: either of the arguments is zero or negative
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    _checkSanity3(x, y)
    if y == 0:
        Result = math.gamma(x) 
    elif (y > x + 1.0):
        Sum = _gammaContFraction(x, y)
        Result = math.exp(-y + x * math.log(y)) * Sum
    else:
        Sum = _gammaSeries(x, y)
        GammaLn = math.lgamma(x)
        Factor = math.exp(-y + x * math.log(y) - GammaLn)
        Result = math.exp(GammaLn + math.log(1 - Factor * Sum))
    return Result

def log_upper_gamma(x: TReal, y : TReal) -> float:
    """
    Calculates the natural logarithm of the upper incomplete gamma function.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 216-219. ISBN: 0-521-43108-5
    
    Signature:
        int > 0 OR float > 0, int >= 0 OR float > 0 -> float
    
    Args:
        x: int > 0 OR float > 0; power parameter of the function
        y: int >= 0 OR float > 0; the integeral boundary parameter of the
            function
    
    Raises:
        Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: either of the arguments is zero or negative
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    _checkSanity3(x, y)
    if y == 0:
        Result = math.lgamma(x) 
    elif (y > x + 1.0):
        Sum = _gammaContFraction(x, y)
        Result = -y + x * math.log(y) + math.log(Sum)
    else:
        Sum = _gammaSeries(x, y)
        GammaLn = math.lgamma(x)
        Factor = math.exp(-y + x * math.log(y) - GammaLn)
        Result = GammaLn + math.log(1 - Factor * Sum)
    return Result

def upper_gamma_reg(x: TReal, y : TReal) -> float:
    """
    Calculates the regularized upper incomplete gamma function.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 216-219. ISBN: 0-521-43108-5
    
    Signature:
        int > 0 OR float > 0, int >= 0 OR float > 0 -> 0 < float <= 1
    
    Args:
        x: int > 0 OR float > 0; power parameter of the function
        y: int >= 0 OR float > 0; the integeral boundary parameter of the
            function
    
    Raises:
        Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: either of the arguments is zero or negative
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    _checkSanity3(x, y)
    GammaLn = math.lgamma(x)
    if y == 0:
        Result = GammaLn
    else:
        Factor = math.exp(-y + x * math.log(y) - GammaLn)
        if (y > x + 1.0):
            Sum = _gammaContFraction(x, y)
            Result = Factor * Sum
        else:
            Sum = _gammaSeries(x, y)
            Result = 1 - Factor * Sum
    return Result

def beta_incomplete(z: TReal, x: TReal, y : TReal) -> float:
    """
    Calculates the incomplete beta function.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 226-228. ISBN: 0-521-43108-5
    
    Signature:
        0 <= int <= 1 OR 0 <= float <= 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> float >= 0
    
    Args:
        z: 0 <= int <= 1 OR 0 <= float <= 1; the integeral boundary parameter of
            the function
        x: int > 0 OR float > 0; the first power parameter of the function
        y: int > 0 OR float > 0; the second power parameter of the function
    
    Raises:
        Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: the first argument is not in the range [0, 1], OR either
            of the other arguments is zero or negative
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    _checkSanity4(z, x, y)
    if z == 0:
        Result = 0
    elif z == 1:
        Result = beta(x, y)
    else:
        Factor = math.exp(x * math.log(z) + y * math.log(1 - z))
        if z < (x + 1.0) / (x + y + 2.0):
            Sum = _betaContFraction(z, x, y)
            Factor /=  x
            Result = Factor * Sum
        else:
            Sum = _betaContFraction(1 - z, y, x)
            Beta = beta(x, y)
            Factor /= y
            Result = Beta - Factor * Sum
    return Result

def log_beta_incomplete(z: TReal, x: TReal, y : TReal) -> float:
    """
    Calculates the natural logarithm of the incomplete beta function.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 226-228. ISBN: 0-521-43108-5
    
    Signature:
        int = 1 OR 0 < float <= 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> float >= 0
    
    Args:
        z: int = 1 OR 0 < float <= 1; the integeral boundary parameter of
            the function
        x: int > 0 OR float > 0; the first power parameter of the function
        y: int > 0 OR float > 0; the second power parameter of the function
    
    Raises:
        Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: the first argument is not in the range [0, 1], OR either
            of the other arguments is zero or negative
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    _checkSanity4(z, x, y)
    if z == 0:
        raise UT_ValueError(z, '> 0, z argument', SkipFrames = 1)
    elif z == 1:
        Result = log_beta(x, y)
    else:
        pass

def beta_incomplete_reg(z: TReal, x: TReal, y : TReal) -> float:
    """
    Calculates the regularized incomplete beta function.
    
    Based on the algorithm given in:
    
    William H. Press, Saul A. Teukolsky, William T. Vetterling and
    Brian P. Flannery. Numerical Recipes in C: The Art of Scientific Computing.
    2nd Ed. Cambridge University Press (1992), pp. 226-228. ISBN: 0-521-43108-5
    
    Signature:
        0 <= int <= 1 OR 0 <= float <= 1, int > 0 OR float > 0,
            int > 0 OR float > 0 -> 0<= float <= 1
    
    Args:
        z: 0 <= int <= 1 OR 0 <= float <= 1; the integeral boundary parameter of
            the function
        x: int > 0 OR float > 0; the first power parameter of the function
        y: int > 0 OR float > 0; the second power parameter of the function
    
    Raises:
        Raises:
        UT_TypeError: either of the arguments is neither integer nor float
        UT_ValueError: the first argument is not in the range [0, 1], OR either
            of the other arguments is zero or negative
        Exception: maximum number of iteration is reached
    
    Version 1.0.0.0
    """
    _checkSanity4(z, x, y)
    if z == 0:
        Result = 0
    elif z == 1:
        Result = 1
    else:
        Factor = math.exp(x * math.log(z) + y * math.log(1 - z) - log_beta(x,y))
        if z < (x + 1.0) / (x + y + 2.0):
            Sum = _betaContFraction(z, x, y)
            Factor /=  x
            Result = Factor * Sum
        else:
            Sum = _betaContFraction(1 - z, y, x)
            Factor /= y
            Result = 1 - Factor * Sum
    return Result