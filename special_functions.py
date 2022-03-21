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
"""

__version__= '1.0.0.0'
__date__ = '21-03-2022'
__status__ = 'Development'

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
    if not isinstance(n, int):
        raise UT_TypeError(n, int, SkipFrames = 1)
    if not isinstance(k, int):
        raise UT_TypeError(k, int, SkipFrames = 1)
    if n < 0:
        raise UT_ValueError(n, '>= 0, number of objects', SkipFrames = 1)
    if k < 0:
        raise UT_ValueError(k, '>= 0, number of trials', SkipFrames = 1)
    if k > n:
        raise UT_ValueError(k,
                    '<= {}, number of trials <= number of objects'.format(n),
                                                                SkipFrames = 1)
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
    if not isinstance(n, int):
        raise UT_TypeError(n, int, SkipFrames = 1)
    if not isinstance(k, int):
        raise UT_TypeError(k, int, SkipFrames = 1)
    if n < 0:
        raise UT_ValueError(n, '>= 0, number of objects', SkipFrames = 1)
    if k < 0:
        raise UT_ValueError(k, '>= 0, number of trials', SkipFrames = 1)
    if k > n:
        raise UT_ValueError(k,
                    '<= {}, number of trials <= number of objects'.format(n),
                                                                SkipFrames = 1)
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
    if not isinstance(x, (int, float)):
        raise UT_TypeError(x, (int, float), SkipFrames = 1)
    if not isinstance(y, (int, float)):
        raise UT_TypeError(y, (int, float), SkipFrames = 1)
    if x <= 0:
        raise UT_ValueError(x, '> 0, x argument', SkipFrames = 1)
    if y <= 0:
        raise UT_ValueError(y, '> 0, y argument', SkipFrames = 1)
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
    if not isinstance(x, (int, float)):
        raise UT_TypeError(x, (int, float), SkipFrames = 1)
    if not isinstance(y, (int, float)):
        raise UT_TypeError(y, (int, float), SkipFrames = 1)
    if x <= 0:
        raise UT_ValueError(x, '> 0, x argument', SkipFrames = 1)
    if y <= 0:
        raise UT_ValueError(y, '> 0, y argument', SkipFrames = 1)
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
