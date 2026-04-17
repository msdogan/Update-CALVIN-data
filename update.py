#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 09:36:22 2023

@author: msdogan

Updating CALVIN database (HOBBES)
"""

import pandas as pd
import os
import json

# data directory
directory = '/Users/Workstation/Documents/github/calvin-network-data/data'

print("**************** exporting network matrix ****************")
 
# following command line command will export network matrix
os.system(f'cnf matrix --data={directory}  --verbose --format=csv --start=1921-10 --stop=2015-10 --ts=. --fs=, --to=network_historical_with_overdraft_feb --max-ub=10000000000')
 
print("network successfully exported")

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
# save_ts_data(rim_inflows,os.sep+'inflows'+os.sep+'default.csv',start_date='1921-09-30',end_date='2015-10-31')
# # print('*********************   *********************')


"""
RESERVOIR EVAPORATION
"""
# print('Updating Reservoir Evaporation')
# # read reservoir evaporation locations (nodes) and time-series data
# res_evaps = pd.read_csv('data/reservoir_evaporation_data.csv', header=0, index_col = 0)
# # convert index to date time index
# res_evaps.index = pd.to_datetime(res_evaps.index)

# # this will match and update calvin-network-data
# save_ts_data(res_evaps,os.sep+'evaporation.csv',start_date='1921-09-30',end_date='2015-10-31')
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
# save_ts_data(gw_inflows,os.sep+'inflows'+os.sep+'default.csv',start_date='1921-09-30',end_date='2015-10-31')
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
# save_ts_data(mif_reqs,os.sep+'LBT.csv',start_date='1921-09-30',end_date='2015-10-31')
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
# save_ts_data(constrained_flow,os.sep+'EQT.csv',start_date='1921-09-30',end_date='2015-10-31')
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
# save_ts_data(target_cap,os.sep+'UBT.csv',start_date='1921-09-30',end_date='2015-10-31')

# print('Updating Urban Target Capacities')
# # read target capacity locations (nodes) and time-series data
# target_cap = pd.read_csv('data/ubt_urban_target_data.csv', header=0, index_col = 0)
# # convert index to date time index
# target_cap.index = pd.to_datetime(target_cap.index)

# # this will match and update calvin-network-data
# save_ts_data(target_cap,os.sep+'UBT.csv',start_date='1921-09-30',end_date='2015-10-31')

# # !!!important!!!
# # If you are updating ag penalties, this will affect ag targets. So, use penalty and target updater below
# print('Updating Ag Target Capacities')
# # read target capacity locations (nodes) and time-series data
# target_cap = pd.read_csv('data/ubt_ag_target_data.csv', header=0, index_col = 0)
# # convert index to date time index
# target_cap.index = pd.to_datetime(target_cap.index)

# # this will match and update calvin-network-data
# save_ts_data(target_cap,os.sep+'UBT.csv',start_date='1921-09-30',end_date='2015-10-31')
# print('*********************   *********************')


"""
LOCAL INFLOWS AND LOSSES
"""
# print('Updating Local Inflows')
# # read local inflow and loss locations (nodes) and time-series data
# local_flow = pd.read_csv('data/local_inflow_and_loss_data.csv', header=0, index_col = 0)
# # convert index to date time index
# local_flow.index = pd.to_datetime(local_flow.index)

# # this will match and update calvin-network-data
# save_ts_data(local_flow,os.sep+'EQT.csv',start_date='1921-09-30',end_date='2015-10-31')
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
# flow_outputs = pd.read_csv('CALVIN_output/flow_extended_with_zeros.csv', header=0, index_col = 0)
# # convert index to date time index
# flow_outputs.index = pd.to_datetime(flow_outputs.index)

# # walk through CALVIN directory (CALVIN-network-data) to update storage on reservoir nodes
# save_ts_data(flow_outputs,os.sep + 'flow.csv',start_date='1921-09-30',end_date='2015-10-31')
# print('*********************   *********************')


# print('Updating Reservoir Storage')
# # read node names and time-series data
# storage_outputs = pd.read_csv('CALVIN_output/storage_extended_with_zeros.csv', header=0, index_col = 0)
# # convert index to date time index
# storage_outputs.index = pd.to_datetime(storage_outputs.index)

# # walk through CALVIN directory (CALVIN-network-data) to update storage on reservoir nodes
# save_ts_data(storage_outputs,os.sep + 'storage.csv',start_date='1921-09-30',end_date='2015-10-31')
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
# save_ts_data(target_cap_ag,os.sep+'UBT.csv',start_date='1921-09-30',end_date='2015-10-31')
# print('*********************   *********************')

# # method 2:
# # demand areas to be updated
# demand_area = {
#     "hu101":"cvpm01",
#     "hu102":"cvpm02",
#     "hu103a":"cvpm03a",
#     "hu103b":"cvpm03b",
#     "hu104":"cvpm04",
#     "hu202":"cvpm05",
#     "hu203":"cvpm06",
#     "hu204":"cvpm07",
#     "hu207":"cvpm08",
#     "hu206":"cvpm09",
#     "hu303":"cvpm10",
#     "hu302":"cvpm11",
#     "hu305":"cvpm12",
#     "hu306":"cvpm13",
#     "hu402a":"cvpm14a",
#     "hu402b":"cvpm14b",
#     "hu404a":"cvpm15a",
#     "hu404b":"cvpm15b",
#     "hu401":"cvpm16",
#     "hu403":"cvpm17",
#     "hu405":"cvpm18",
#     "hu408a":"cvpm19a",
#     "hu408b":"cvpm19b",
#     "hu407":"cvpm20",
#     "hu409a":"cvpm21a",
#     "hu409b":"cvpm21b",
#     "hu409c":"cvpm21c"
#     }

# return_type = {"GW":"g","SW":"s"}

# months = {'January':"JAN",'February':"FEB",'March':"MAR",'April':"APR",'May':"MAY",'June':"JUN",'July':"JUL",'August':"AUG",'September':"SEP",'October':"OCT",'November':"NOV",'December':"DEC"}

# start_date='1921-10-31'
# end_date='2015-09-30'
# date_range = pd.date_range(start=start_date,end=end_date,freq='M')
# target_delivery=pd.DataFrame(index=date_range)
# target_delivery.index.name = 'date'

# # read penalties - raw data
# # Read data
# df = pd.read_csv("data/ag_penalty/penalties_lambdawaters_monthly_feb.csv")

# unique_hu = df["hu"].unique()
# unique_month = df["month_name"].unique()
# unique_water_type = df["water_type"].unique()

# for hu in unique_hu:
#     df_region = df[df["hu"] == hu]
#     for wt in unique_water_type:
#         subregion = demand_area[hu]
#         link = hu + '-' + subregion + return_type[wt]
#         penalty_loc = loc_finder(link, directory)+os.sep+'costs'+os.sep
#         print(penalty_loc)
#         df_wt = df_region[df_region["water_type"] == wt]
#         monthly_target = {}
#         for month in unique_month:
#             df_save = pd.DataFrame()
#             print(f'{hu}, {wt}, {month}')
#             df_month = df_wt[df_wt["month_name"] == month]
#             delivery = df_month["xwatersc_monthly_TAF"]
#             penalty = df_month["penalty"]
            
#             if sum(delivery) == 0: # these are months/regions with zero target capacity
#                 delivery = [0.000001,0] # if you don't update this, problems can arise when calcualting slopes (unit cost c)
#                 penalty = [0,0]
            
#             df_save["capacity"] = delivery
#             df_save["cost"] = penalty
            
#             # save and update penalties
#             df_save.to_csv(penalty_loc+os.sep+months[month]+'.csv', index=False)
            
#             monthly_target[month]=df_save['capacity'].iloc[-1]
#         targets=[]
#         for j in target_delivery.index:
#             targets.append(monthly_target[j.strftime("%B")])
#         target_delivery[link]=targets

# # save target capacities    
# target_delivery.to_csv('data/ubt_ag_target_CV_feb.csv')

# print('Updating ag target deliveries (UBT)')
# # read target capacity locations (nodes) and time-series data
# target_cap_ag = pd.read_csv('data/ubt_ag_target_05_CV_feb.csv', header=0, index_col = 0)
# # convert index to date time index
# target_cap_ag.index = pd.to_datetime(target_cap_ag.index)

# # this will match and update calvin-network-data
# save_ts_data(target_cap_ag,os.sep+'UBT.csv',start_date='1921-09-30',end_date='2015-10-31')
# print('*********************   *********************')


"""
   PERTURBED HYDROLOGY FOR CLIMATE CHANGE
"""

# # climate scenario
# scenarios = [
#             # 'ACCESS-CM2', # ssp370 does not exist
#             # 'EC-Earth3-Veg',
#             # 'FGOALS-g3',
#             # 'GFDL-ESM4',
#             # 'INM-CM5-0',
#             # 'IPSL-CM6A-LR',
#             # 'KACE-1-0-G',
#             # 'MIROC6',
#             'MPI-ESM1-2-HR',
#             # 'MRI-ESM2-0',
#             # 'TaiESM1' # ssp585 does not exist
#             ]
# # ssp scenario
# ssps = [
#         # 'ssp245',
#         # 'ssp370',
#         'ssp585'
#         ]

# # following scenarios do not exist in the database
# skip_pairs = {
#     ('ACCESS-CM2', 'ssp370'),
#     ('TaiESM1', 'ssp585')
# }

# # organize projected runoff
# for scenario in scenarios:
#     for ssp in ssps:
#         if (scenario, ssp) in skip_pairs:
#             continue
#         print(f'scenario: {scenario}, ssp: {ssp}')
#         """
#         RIM INFLOWS
#         """
#         print('Perturbing Reservoir Inflow')
#         # read rim inflow locations (nodes) and time-series data
#         rim_inflows = pd.read_csv(f'data/perturbed_hydrology/rim_inflow/{scenario}_{ssp}_rim_inflow_perturbed.csv', header=0, index_col = 0)
#         # convert index to date time index
#         rim_inflows.index = pd.to_datetime(rim_inflows.index)
        
#         # this will match and update calvin-network-data
#         save_ts_data(rim_inflows,os.sep+'inflows'+os.sep+'default.csv',start_date='1921-09-30',end_date='2015-10-31')
#         # print('*********************   *********************')
        
        
#         """
#         GROUNDWATER INFLOWS
#         """
#         print('Perturbing Groundwater Inflow')
#         # read groundwater inflow locations (nodes) and time-series data
#         gw_inflows = pd.read_csv(f'data/perturbed_hydrology/gw_inflow/{scenario}_{ssp}_gw_inflow_perturbed.csv', header=0, index_col = 0)
#         # convert index to date time index
#         gw_inflows.index = pd.to_datetime(gw_inflows.index)
        
#         # this will match and update calvin-network-data
#         save_ts_data(gw_inflows,os.sep+'inflows'+os.sep+'default.csv',start_date='1921-09-30',end_date='2015-10-31')
#         print('*********************   *********************')
        
        
#         """
#         LOCAL INFLOWS AND LOSSES
#         """
#         print('Perturbing Local Inflows')
#         # read local inflow and loss locations (nodes) and time-series data
#         local_flow = pd.read_csv(f'data/perturbed_hydrology/local_inflow/{scenario}_{ssp}_local_inflow_perturbed.csv', header=0, index_col = 0)
#         # convert index to date time index
#         local_flow.index = pd.to_datetime(local_flow.index)
        
#         # this will match and update calvin-network-data
#         save_ts_data(local_flow,os.sep+'EQT.csv',start_date='1921-09-30',end_date='2015-10-31')
#         print('*********************   *********************')
        
#         print("**************** exporting network matrix ****************")
        
#         # following command line command will export network matrix
#         os.system(f'cnf matrix --data={directory}  --verbose --format=csv --start=1921-10 --stop=2015-10 --ts=. --fs=, --to=network_{scenario}_{ssp}_no_overdraft_debug --max-ub=10000000000 --debug=All')
        
#         print("network successfully exported")



'''
*********************   *********************
NOT WORKING YET - THIS MODULE WILL MODIFY NODE.GEOJSON files - NOT WORKING YET
*********************   *********************
'''
# for subdirs, dirs, files in os.walk(directory):
#     for file in files:
#         if file == "node.geojson":
#             filepath = subdirs+os.sep+"node.geojson"
#             # with open(filepath, 'r') as filex:
#             #     # read lines from the file
#             #     lines = filex.readlines()
#             # if lines[-1] != '"'+'flow'+'"'+':'+'null'+'}'+'}':
#             #     print(filepath)
#             # Opening JSON file
#             with open(filepath, 'r') as openfile:
#                 # Reading from json file
#                 json_object = json.load(openfile)
#             json_object["properties"]["flow"]=None
#             with open(filepath, "w") as outfile:
#                 json.dump(json_object, outfile)

print('%%%%%%%%  FINISHED  %%%%%%%%')