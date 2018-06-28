import numpy as np
np.set_printoptions(threshold=np.nan)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# -- Transfer functions


def identity(x, derivate = False):
    return x if not derivate else np.ones(x.shape)

def logistic(x, derivate = False):
    return 1 / (1 + np.e ** (-x)) if not derivate else x * (1 - x)

def hyperbolic_tangent(x, derivate = False):
    return (np.exp(2 * x) - 1) / (np.exp(2 * x) + 1) if not derivate else 1 - x ** 2

def relu(x, derivate = False):
    maxe = lambda y: y if y > 0 else 0.0
    f = np.vectorize(maxe)
    deriv = lambda y: 1 if y > 0 else 0.0
    derivf = np.vectorize(deriv)
    return f(x) if not derivate else derivf(x)
