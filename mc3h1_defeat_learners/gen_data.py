"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""

import numpy as np
import math


# this function should return a dataset (X and Y) that will work
# better for linear regresstion than random trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    X = np.random.choice(1000, (800, 3))
    ones = np.ones(800).reshape(800, 1)
    Y = np.dot(np.concatenate((X, ones), axis=1),
               np.array([1, 3, 5, 7])) + np.random.choice(1000, 800) / 200
    return X, Y


def best4RT(seed=1489683273):
    np.random.seed(seed)
    X = np.random.choice(1000, (800, 2))
    cut = [200, 500]
    Y = (((X[:, 0] < cut[0]) + (X[:, 0] > cut[1])) +
         ((X[:, 1] < cut[0]) + (X[:, 1] > cut[1]))).astype('int')
    return X, Y


if __name__ == "__main__":
    print "they call me Tim."
