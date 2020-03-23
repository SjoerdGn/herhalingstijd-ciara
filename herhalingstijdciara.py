# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:35:37 2020

@author: Sjoerd Gnodde
"""

import pandas as pd
import datetime as dt
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.optimize import curve_fit
import knmi
import matplotlib.pyplot as plt
from ev_distributions import gumbel_cdf, weibull_cdf
from sklearn.metrics import mean_squared_error
from fit_functions import optimal_function
import numpy as np


def get_repetition_times_knmi(dates, pref = None):
    """Get repetition times from KNMI data.
    
    Calculates the repetition times for maximum peak wind and 
    highest hourly wind peak. 
    

    Parameters
    ----------
    dates : list of dt.DateTime objects
        Dates of the storm
    pref : str or None (optional)
        Preference for a certain function.
        If None, returns optimal fit function.
        If 'gumbel', returns only the Gumbel one.
        If 'weibull', returns only the Weibull result.

    Returns
    -------
    rtdf : pandas.DataFrame
        DataFrame with location and both types of return times.

    """
    rtdf = pd.DataFrame(columns=['Station_', 'longitude', 'latitude', 'RT', 'RTH'])
    for station in knmi.stations.keys():
        
        if station>199:
            data = knmi.get_day_data_dataframe(stations = [station], start = dt.datetime(1963,1,1))
            if len(data['FHX']) < 100:
                continue
            
            data['FHX'] = data['FHX']*0.1
            data['FXX'] = data['FXX']*0.1
            try:        
                ecdfw = ECDF(data['FXX'][data['FXX']>=0])
                ecdfh = ECDF(data['FHX'][data['FHX']>=0])
                lastmax = np.nanmax([data['FXX'][date] for date in dates])
                lastmaxh = np.nanmax([data['FHX'][date] for date in dates])
                chance = optimal_function(ecdfw.x[1:], ecdfw.y[1:], lastmax, pref = pref)
                chanceh = optimal_function(ecdfh.x[1:], ecdfh.y[1:], lastmaxh, pref = pref)
            except:
                continue
    
            returntime = round(1/(1-chance))
            returntimeh = round(1/(1-chanceh))
            
            if returntime > 0 and returntime<1000000 and len(data['FXX'][data['FXX']>=0])>10*365:
                if returntimeh > 0 and returntimeh<1000000 and len(data['FHX'][data['FHX']>=0])>10*365:
               
                    rtdf = rtdf.append({'Station_':int(station), 'longitude':knmi.stations[station].longitude,
                                        'latitude':knmi.stations[station].latitude,'RT':returntime, 'RTH':returntimeh},ignore_index=True)
    
    rtdf['Station_'] = rtdf['Station_'].astype(int)
    rtdf['RT'] = rtdf['RT'].astype(int)
    rtdf['RTH'] = rtdf['RTH'].astype(int)
    return rtdf


if __name__ == "__main__":
    dates = [dt.datetime(2020, 2,9), dt.datetime(2020, 2,10)]
    rtdf = get_repetition_times_knmi(dates, pref = 'gumbel')
    rtdf.to_csv("../data/herhalingstijd-ciara.csv", index=False)

