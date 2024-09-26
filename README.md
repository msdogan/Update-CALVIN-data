# Update-CALVIN-data
 This repo can be used to update CALVIN database. For each CALVIN component (Rim inflow, gw inflow, evaporation etc.), `update.py` code takes time-series from defined files and updates existing database with a defined path.

# CALVIN database repository:
https://github.com/ucd-cws/calvin-network-data

# Update Memo
The [update memo](https://github.com/msdogan/Update-CALVIN-data/blob/main/data_sources_documentation/CALVIN_Input_Hydrology_Update_2024_Memo.docx) describes surface and groundwater hydrology update process and data sources:

# Data Sources
Mainly CALSIM III and C2VSim models are used to update CALVIN's surface water and groundwater hydrology, respectively.

# CALVIN's Updated Hydrology
Files in the following directory describes update process for each time-series
https://github.com/msdogan/Update-CALVIN-data/tree/main/data_sources_documentation/CALVIN_Updated_Hydrology

# Output Comparison
Following figures compare CALVIN results with old (1921-2003) and updated (1921-2015) hydrology

+ Ag and Urban Delivery - Duration
  
<img src="https://github.com/msdogan/Update-CALVIN-data/blob/main/plots/ag_delivery_duration.png" width="400"> <img src="https://github.com/msdogan/Update-CALVIN-data/blob/main/plots/urban_delivery_duration.png" width="400">

+ Surface Storage and Duration

<img src="https://github.com/msdogan/Update-CALVIN-data/blob/main/plots/surface_storage.png" width="400"> <img src="https://github.com/msdogan/Update-CALVIN-data/blob/main/plots/surface_storage_duration.png" width="400">

+ Surface Release and Duration

<img src="https://github.com/msdogan/Update-CALVIN-data/blob/main/plots/surface_reservoir_release.png" width="400"> <img src="https://github.com/msdogan/Update-CALVIN-data/blob/main/plots/surface_reservoir_release_duration.png" width="400">

+ Delta Exports and Duration

<img src="https://github.com/msdogan/Update-CALVIN-data/blob/main/plots/delta_exports.png" width="400"> <img src="https://github.com/msdogan/Update-CALVIN-data/blob/main/plots/delta_exports_duration.png" width="400">  
