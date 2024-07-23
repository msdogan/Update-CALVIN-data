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
            if loc.lower() == director:
                filepath = os.path.join(subdirs, director)
                break
            
    return filepath

def save_ts_data(df,path_ending,start_date='1921-09-30',end_date='2003-10-31'):
    save_data = pd.DataFrame()
    save_data.index = df.index
    save_data.index.names = ['date']
    for c in df.columns:
        col = c.lower()
        print('Updating: '+col)
        # sinks and inflows do not follow general rule and they have a specific representation
        if '-sink' in col:
            col = col.replace("-sink", "")
            file_loc = loc_finder(col,directory)+os.sep+'sinks'+os.sep+'default'+path_ending
        elif 'inflow-' in col:
            col = col.replace("inflow-", "")
            file_loc = loc_finder(col,directory)+os.sep+'inflows'+os.sep+'default.csv'
        else:
            file_loc = loc_finder(col,directory) + path_ending
        # save matched time-series data
        save_data['kaf'] = df[c].values
        save_data = save_data[(save_data.index > start_date) & (save_data.index < end_date)]
        save_data.to_csv(file_loc, index=True)
    return



"""
RIM INFLOWS
"""
# print('Updating Reservoir Inflow')
# # read rim inflow locations (nodes) and time-series data
# rim_inflows = pd.read_csv('data/rim_inflow_data.csv', header=0, index_col = 0)
# # convert index to date time index
# rim_inflows.index = pd.to_datetime(rim_inflows.index)

# # this will match and update calvin-network-data
# save_ts_data(rim_inflows,os.sep+'inflows'+os.sep+'default.csv')
# print('*********************   *********************')


"""
RESERVOIR EVAPORATION
"""
# print('Updating Reservoir Evaporation')
# # read reservoir evaporation locations (nodes) and time-series data
# res_evaps = pd.read_csv('data/reservoir_evaporation_data.csv', header=0, index_col = 0)
# # convert index to date time index
# res_evaps.index = pd.to_datetime(res_evaps.index)

# # this will match and update calvin-network-data
# save_ts_data(res_evaps,os.sep+'evaporation.csv')
# print('*********************   *********************')


"""
GROUNDWATER INFLOWS
"""
# print('Updating Groundwater Inflow')
# # read groundwater inflow locations (nodes) and time-series data
# gw_inflows = pd.read_csv('data/gw_inflow_data.csv', header=0, index_col = 0)
# # convert index to date time index
# gw_inflows.index = pd.to_datetime(gw_inflows.index)

# # this will match and update calvin-network-data
# save_ts_data(gw_inflows,os.sep+'inflows'+os.sep+'default.csv')
# print('*********************   *********************')


"""
MINIMUM INSTREAM FLOW REQUIREMENTS
"""
# print('Updating MIF Requirements')
# # read minimum instream flow locations (nodes) and time-series data
# mif_reqs = pd.read_csv('data/mif_req_lbt_data.csv', header=0, index_col = 0)
# # convert index to date time index
# mif_reqs.index = pd.to_datetime(mif_reqs.index)

# # this will match and update calvin-network-data
# save_ts_data(mif_reqs,os.sep+'LBT.csv')
# print('*********************   *********************')

"""
CONSTRAINED FLOW TIME-SERIES
"""
# print('Updating Constrained Flows')
# # read constrained flow locations (nodes) and time-series data
# # (mostly refuge deliveries and fixed urban demands)
# constrained_flow = pd.read_csv('data/constrained_eqt_data.csv', header=0, index_col = 0)
# # convert index to date time index
# constrained_flow.index = pd.to_datetime(constrained_flow.index)

# # this will match and update calvin-network-data
# save_ts_data(constrained_flow,os.sep+'EQT.csv')
# print('*********************   *********************')


"""
TARGET AND CAPACITY TIME-SERIES
(excluding ag target deliveries)
"""
# print('Updating Infrastructure Capacities')
# # read target capacity locations (nodes) and time-series data
# target_cap = pd.read_csv('data/ubt_infrastructure_cap_data.csv', header=0, index_col = 0)
# # convert index to date time index
# target_cap.index = pd.to_datetime(target_cap.index)

# # this will match and update calvin-network-data
# save_ts_data(target_cap,os.sep+'UBT.csv')

# print('Updating Urban Target Capacities')
# # read target capacity locations (nodes) and time-series data
# target_cap = pd.read_csv('data/ubt_urban_target_data.csv', header=0, index_col = 0)
# # convert index to date time index
# target_cap.index = pd.to_datetime(target_cap.index)

# # this will match and update calvin-network-data
# save_ts_data(target_cap,os.sep+'UBT.csv')

# !!!important!!!
# If you are updating ag penalties, this will affect ag targets. So, use penalty and target updater below
print('Updating Ag Target Capacities')
# read target capacity locations (nodes) and time-series data
target_cap = pd.read_csv('data/ubt_ag_target_data.csv', header=0, index_col = 0)
# convert index to date time index
target_cap.index = pd.to_datetime(target_cap.index)

# this will match and update calvin-network-data
save_ts_data(target_cap,os.sep+'UBT.csv')
print('*********************   *********************')


"""
LOCAL INFLOWS AND LOSSES
"""
# print('Updating Local Inflows')
# # read local inflow and loss locations (nodes) and time-series data
# local_flow = pd.read_csv('data/local_inflow_and_loss_data.csv', header=0, index_col = 0)
# # convert index to date time index
# local_flow.index = pd.to_datetime(local_flow.index)

# # this will match and update calvin-network-data
# save_ts_data(local_flow,os.sep+'EQT.csv')
# print('*********************   *********************')


"""
*********************   *********************
THIS MODULE WILL UPDATE EXISTING OUTPUTS (BASECASE - MASTER) WITH DESIRED OUTPUTS
*********************   *********************


Required files:
    flow.csv (This file has flows for all links in CALVIN)
    storage.csv (This file has storage values for all surface and groundwater reservoirs)
"""

# print('Updating Link Flow')
# # read link names and time-series data
# flow_outputs = pd.read_csv('CALVIN_output/flow.csv', header=0, index_col = 0)
# # convert index to date time index
# flow_outputs.index = pd.to_datetime(flow_outputs.index)

# # walk through CALVIN directory (CALVIN-network-data) to update storage on reservoir nodes
# save_ts_data(flow_outputs,os.sep + 'flow.csv')
# print('*********************   *********************')


# print('Updating Reservoir Storage')
# # read node names and time-series data
# storage_outputs = pd.read_csv('CALVIN_output/storage.csv', header=0, index_col = 0)
# # convert index to date time index
# storage_outputs.index = pd.to_datetime(storage_outputs.index)

# # walk through CALVIN directory (CALVIN-network-data) to update storage on reservoir nodes
# save_ts_data(storage_outputs,os.sep + 'storage.csv')
# print('*********************   *********************')

'''
*********************   *********************
THIS MODULE WILL UPDATE AG PENALTIES AND AG TARGET DELIVERIES 
*********************   *********************
'''

# # read ag link information from ag_regions.csv and identify links where penalties are applied
# ag_region_names = pd.read_csv('data/ag_penalty/ag_regions.csv',header=0)
# ag_links = ag_region_names['penalty_link']

# start_date='1921-10-31'
# end_date='2003-09-30'
# date_range = pd.date_range(start=start_date,end=end_date,freq='M')
# target_delivery=pd.DataFrame(index=date_range)
# target_delivery.index.name = 'date'

# print('Updating ag penalties')
# for r in ag_links:
#     print('region: '+r)
#     penalty = pd.read_csv('data/ag_penalty/'+r+'.csv')
#     monthly_penalty_dict={}
#     for i in range(12):
#         dfsave = pd.DataFrame()
#         col1 = penalty.columns[2*i]
#         col2 = penalty.columns[2*i+1]
#         dfsave['capacity'] = penalty[col1].dropna()
#         dfsave['cost'] = penalty[col2].dropna()
#         penalty_loc = loc_finder(r, directory)+os.sep+'costs'+os.sep
#         dfsave.to_csv(penalty_loc+col2+'.csv', index=False)
#         # construct times-series for ag target deliveries
#         monthly_penalty_dict[i+1]=dfsave['capacity'].iloc[-1]
#     # construct annual time-series from monthly targets
#     targets=[]
#     for j in target_delivery.index:
#         targets.append(monthly_penalty_dict[j.month])
#     target_delivery[r]=targets
# target_delivery.to_csv('data/ubt_ag_target.csv')

# print('Updating ag target deliveries (UBT)')
# # read target capacity locations (nodes) and time-series data
# target_cap_ag = pd.read_csv('data/ubt_ag_target.csv', header=0, index_col = 0)
# # convert index to date time index
# target_cap_ag.index = pd.to_datetime(target_cap_ag.index)

# # this will match and update calvin-network-data
# save_ts_data(target_cap_ag,os.sep+'UBT.csv')
# print('*********************   *********************')
