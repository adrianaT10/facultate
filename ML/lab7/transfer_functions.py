# Tudor Berariu, 2016

import numpy as np
import math

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# -- Transfer functions
#
# Useful numpy functions and constants:
#  - np.e : the "e" constant (Euler's number)

def identity(x, derivate = False):
    return x if not derivate else np.ones(x.shape)

def logistic(x, derivate = False):
    if not derivate:
        # return np.array(map(lambda a: 1 / (1 + math.exp(-a)), x))
        return 1 / (1 + np.exp(-x))
    return x * (1 - x)
    # TODO (1.a)

def hyperbolic_tangent(x, derivate = False):
    if not derivate:
        return (np.exp(2 * x) - 1) / (np.exp(2 * x) + 1)
    return 1 - x * x
    # TODO (1.b)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# -- Testing transfer functions

from util import close_enough

def test_transfer_functions():
    X = np.array([
        -100.0, -10.0, -1.0, -.1, -.01, .0, .1, .01, .1, 1.0, 10.0, 100.0
    ])
    logX = np.array([
        3.7200759760208555e-44, 4.539786870243442e-05, 0.2689414213699951,
        0.47502081252106, 0.49750002083312506, 0.5, 0.52497918747894,
        0.5024999791668749, 0.52497918747894, 0.7310585786300049,
        0.9999546021312976, 1.0
    ])
    dlogX = np.array(
        [3.7200759760208555e-44, 4.53958077359517e-05, 0.19661193324148185,
         0.24937604019289197, 0.2499937501041652,  0.25, 0.24937604019289197,
         0.2499937501041652, 0.24937604019289197, 0.19661193324148185,
         4.5395807735907655e-05, 0.0]
    )
    tanhX = np.array([
        -1.0, -0.99999999587769273, -0.76159415595576485, -0.099667994624955819,
        -0.0099996666799994603, 0.0, 0.099667994624955819,
        0.0099996666799994603, 0.099667994624955819, 0.76159415595576485,
        0.99999999587769273, 1.0
    ])
    dtanhX = np.array([
        0.0, 8.2446145466263943e-09, 0.41997434161402614,
        0.9900662908474398, 0.99990000666628887, 1.0, 0.9900662908474398,
        0.99990000666628887, 0.9900662908474398, 0.41997434161402614,
        8.2446145466263943e-09, 0.0
    ])


    # Test the identity transfer function
    print("Testing the identity transfer function ...")
    assert close_enough(identity(X), X), \
        "Identity function not good!"
    assert close_enough(identity(X, True), np.ones(X.shape)), \
        "Identity derivative not good"
    print("Identity transfer function implemented ok!")

    # Test the sigmoid transfer function
    print("Testing the logistic transfer function ...")
    assert close_enough(logistic(X), logX), \
        "Logistic function not good"
    assert close_enough(logistic(logX, True), dlogX), \
        "Logistic function not good"
    print("Logistic transfer function implemented ok!")

    # Test the sigmoid transfer function
    print("Testing the hyperbolic tangent transfer function ...")
    assert close_enough(hyperbolic_tangent(X), tanhX), \
        "Hyperbolic tangent function not good"
    assert close_enough(hyperbolic_tangent(tanhX, True), dtanhX), \
        "Hyperbolic tangent function not good"
    print("Hyperbolic tangent transfer function implemented ok!")

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    test_transfer_functions()
