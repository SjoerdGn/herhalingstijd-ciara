# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:36:36 2020

@author: sgnodde
"""
import numpy as np

def gumbel_cdf(x, mu, beta):
    """Gumbel CDF. 
    
        
    Parameters
    ----------
    x : list or numpy.array (1d)
        x-values.
    mu : float
        mu parameter of Gumbel function.
    beta : float
        beta parameter of Gumbel function.

    Returns
    -------
    F : similar to x
        CDF of x-values of Gumbel function

    """
    F = np.exp(-np.exp((mu-x)/beta))
    return F


def weibull_cdf(x, lambda_, k):
    """Weibull CDF. 
    
        
    Parameters
    ----------
    x : list or numpy.array (1d)
        x-values.
    lambda_ : float
        lambda parameter of Weibull function.
    k : float
        k parameter of Weibull function.

    Returns
    -------
    F : similar to x
        CDF of x-values of Weibull function

    """
    F = 1 - np.exp(-(x/lambda_)**k)
    return F