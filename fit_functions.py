# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:19:44 2020

@author: sgnodde
"""

from ev_distributions import gumbel_cdf, weibull_cdf
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit

def _test_gumbel(x, *params):
    return gumbel_cdf(x,params[0], params[1])

def _test_weibull(x, *params):
    return weibull_cdf(x,params[0], params[1])

def optimal_function(x, y, goal):
    """Find the optimal function and parameters
    

    Parameters
    ----------
    x : list or numpy.array
        x-values.
    y : list or numpy.array
        y-values.

    Returns
    -------
    Intersect of the goal.

    """
    
    # gumbel
    best_params_gumbel, _ = curve_fit(_test_gumbel, x, y, p0 = [6,2.5])
    mse_gumbel = mean_squared_error(y, _test_gumbel(x, *tuple(best_params_gumbel)))
    
    # weibull
    best_params_weibull, _ = curve_fit(_test_weibull, x, y, p0 = [8,3])
    mse_weibull = mean_squared_error(y, _test_weibull(x, *tuple(best_params_weibull)))
    
    
    return _test_gumbel(goal, *tuple(best_params_gumbel))
    # if mse_gumbel < mse_weibull:
    #     return _test_gumbel(goal, *tuple(best_params_gumbel))
    
    # else:
    #     return _test_weibull(goal, *tuple(best_params_weibull))
