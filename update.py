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


def loc_finder(loc, directory):
    for subdirs, dirs, files in os.walk(directory):
        for director in dirs:
            if director == loc:
                # print (os.path.join(subdirs, director))
                filepath = subdirs + os.sep + director
                # print(filepath)
                break
    return filepath


# rim inflow locations (nodes)
rim_inflows = pd.read_csv('rim_inflow_loc.csv', header=0)

for rim_inflow in rim_inflows['Node']:
    rim_file = loc_finder(rim_inflow,directory) + os.sep + 'inflows' + os.sep + 'default.csv'





# for subdirs, dirs, files in os.walk(directory):
#     for file in files:
#         # print(os.path.join(subdirs, file))
#         filepath = subdirs + os.sep + file
#         if filepath.endswith("LBT.csv"):
#             print(filepath)