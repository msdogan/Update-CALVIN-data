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
    

"""
RIM INFLOWS
"""
# print('Updating Reservoir Inflow')
# # read rim inflow locations (nodes) and time-series data
# rim_inflows = pd.read_csv('data/rim_inflow_taf_data.csv', header=0, index_col = 0)
# # convert index to date time index
# rim_inflows.index = pd.to_datetime(rim_inflows.index)

# # this will match and update calvin-network-data rim inflows
# save_data = pd.DataFrame()
# save_data.index = rim_inflows.index
# save_data.index.names = ['date']
# for rim_inflow in rim_inflows.columns:
#     print('Updating reservoir inflow: '+rim_inflow)
#     rim_file_loc = loc_finder(rim_inflow,directory) + os.sep + 'inflows' + os.sep + 'default.csv'
#     # save matched time-series data
#     save_data['kaf'] = rim_inflows[rim_inflow].values
#     save_data.to_csv(rim_file_loc, index=True)


"""
RESERVOIR EVAPORATION
"""
print('Updating Reservoir Evaporation')
# read reservoir evaporation locations (nodes) and time-series data
res_evaps = pd.read_csv('data/reservoir_evaporation_data.csv', header=0, index_col = 0)
# convert index to date time index
res_evaps.index = pd.to_datetime(res_evaps.index)

# this will match and update calvin-network-data reservoir evaporation
save_data = pd.DataFrame()
save_data.index = res_evaps.index
save_data.index.names = ['date']
for res_evap in res_evaps.columns:
    print('Updating reservoir evap: '+res_evap)
    res_evap_file_loc = loc_finder(res_evap,directory) + os.sep + 'evaporation.csv'
    # save matched time-series data
    save_data['kaf'] = res_evaps[res_evap].values
    save_data.to_csv(res_evap_file_loc, index=True)



# for subdirs, dirs, files in os.walk(directory):
#     for file in files:
#         # print(os.path.join(subdirs, file))
#         filepath = subdirs + os.sep + file
#         if filepath.endswith("LBT.csv"):
#             print(filepath)