# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 13:35:37 2020

@author: Sjoerd Gnodde
"""

import pandas as pd
import datetime as dt
from statsmodels.distributions.empirical_distribution import ECDF

import knmi

from ev_distributions import gumbel_cdf, weibull_cdf

rtdf = pd.DataFrame(columns=['Station_', 'RT', 'RTH'])


for station in knmi.stations.keys():
    
    if station>199:
        try:
            data = knmi.get_day_data_dataframe(stations = [station], start = dt.datetime(1963,1,1))
        
            data['FHX'] = data['FHX']*0.1
            data['FXX'] = data['FXX']*0.1

            
            ecdfw = ECDF(data['FXX'][data['FXX']>=0])
            ecdfh = ECDF(data['FHX'][data['FHX']>=0])
            
            lastmax = data['FXX'][dt.datetime(2020, 2,9)]
            lastmaxh = data['FHX'][dt.datetime(2020, 2,9)]
            
            chance = 1 - ecdfw.__call__(lastmax)
            chanceh = 1 - ecdfh.__call__(lastmaxh)
            
            returntime = round(1/chance)
            returntimeh = round(1/chanceh)
            
            print(station,returntime, returntimeh)
            
            if returntime > 0 and returntime<100000 and len(data['FXX'][data['FXX']>=0])>10*365:
                if returntimeh > 0 and returntimeh<100000 and len(data['FHX'][data['FHX']>=0])>10*365:
               
                    rtdf = rtdf.append({'Station_':int(station), 'RT':returntime, 'RTH':returntimeh},ignore_index=True)
        except:
            pass


    
    

rtdf['Station_'] = rtdf['Station_'].astype(int)
rtdf['RT'] = rtdf['RT'].astype(int)
rtdf['RTH'] = rtdf['RTH'].astype(int)
#rtdf.to_csv(save_path, index=False)


