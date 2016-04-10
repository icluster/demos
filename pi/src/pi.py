#!/usr/bin/env python
''' Evaluate pi using Monte Carlo '''

import numpy as np
import random as rd
import sys
import matplotlib.pyplot as pl


def calc_pi(nsamples, bin_width):
    '''Simple (parallel) implementation of Monte Carlo evaluation of pi

Parameters
----------
nsamples : int
    Number of independent samples to make.
bin_width : int
    Zero quantities every bin_width iterations.

Returns
-------
pi : float
    Estimate of pi
std_err : float
    Estimate of standard error in estimate for pi.
configs : list of lists
    [x, y] pairs of points which are randomly generated.
'''

    hit = 0.0
    cycle = 0
    it = 0
    nmeasure = nsamples / bin_width
    estimators = np.zeros(shape=(nmeasure,2))
    configs = []

    for n in range(1, nsamples+1):
        # Generate random x and y cordinate uniformly in interval [-1,1].
        (x, y) = (rd.uniform(-1,1), rd.uniform(-1,1))

        # Does point lie within unit circle?
        if (x**2.0 + y**2.0)**0.5 <= 1.0:
            hit += 1

        # Update average every bin_width attempts.
        if n % bin_width == 0:
            est = 4.0*hit / bin_width
            estimators[cycle] = est
            configs.append([x,y])
            hit = 0
            cycle += 1

    return (np.mean(estimators), (np.var(estimators)/nmeasure)**0.5, configs)


if __name__ == "__main__":

    if len(sys.argv[1:]) < 2:
        print ("Usage: pi.py nsamples bin_width")
    else:
        print (calc_pi(int(sys.argv[1]), int(sys.argv[2])))
