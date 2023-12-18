#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 09:36:22 2023

@author: msdogan

Updating CALVIN database (HOBBES)
"""

import pandas as pd
import os

# data directory
directory = '/Users/msdogan/Documents/github/calvin-network-data/data'

# this function finds data path for desired nodes or links
def loc_finder(loc, directory):
    for subdirs, dirs, files in os.walk(directory):
        for director in dirs:
            if director == loc:
                # print (os.path.join(subdirs, director))
                filepath = subdirs + os.sep + director
                break
    return filepath

def save_ts_data(df,path_ending):
    save_data = pd.DataFrame()
    save_data.index = df.index
    save_data.index.names = ['date']
    for c in df.columns:
        print('Updating reservoir evap: '+c)
        file_loc = loc_finder(c,directory) + path_ending
        # save matched time-series data
        save_data['kaf'] = df[c].values
        save_data.to_csv(file_loc, index=True)
    return



"""
RIM INFLOWS
"""
print('Updating Reservoir Inflow')
# read rim inflow locations (nodes) and time-series data
rim_inflows = pd.read_csv('data/rim_inflow_taf_data.csv', header=0, index_col = 0)
# convert index to date time index
rim_inflows.index = pd.to_datetime(rim_inflows.index)

# this will match and update calvin-network-data rim inflows
save_ts_data(rim_inflows,os.sep + 'inflows' + os.sep + 'default.csv')
print('*********************   *********************')


"""
RESERVOIR EVAPORATION
"""
print('Updating Reservoir Evaporation')
# read reservoir evaporation locations (nodes) and time-series data
res_evaps = pd.read_csv('data/reservoir_evaporation_data.csv', header=0, index_col = 0)
# convert index to date time index
res_evaps.index = pd.to_datetime(res_evaps.index)

# this will match and update calvin-network-data reservoir evaporation
save_ts_data(res_evaps,os.sep + 'evaporation.csv')
print('*********************   *********************')

