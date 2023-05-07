#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:40:57 2023

@author: samcerv
"""


# Set up

import re
import requests
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from geopandas import points_from_xy
plt.rcParams['figure.dpi'] = 300


########## Spatial files 

## Read spatial files (urban census tracts of MExico City)

urb_ct=gpd.read_file("df_ageb_urb.shp")
urb_ct.plot()

## BRT lines (shapefile)

brt_lines=gpd.read_file("Metrobus_lineas_utm14n.shp",color='green')

## Join of census tracts and BRT lines. 

urb_ct2=urb_ct.to_crs("EPSG:32614")
ct_brt_join= pd.concat([urb_ct2.geometry,brt_lines.geometry])

# Merge exclusion index and census tracts

excl=pd.read_csv("excl.csv")
ct_excl  = urb_ct2.merge(excl, on='CVEGEO', how='left')

# Chloropleth of Social Exclusion Index. 

fig, ax = plt.subplots(figsize=(20, 8))
ct_excl.plot(ax=ax, alpha=1.0, markersize=2, column="IMU2010", scheme="natural_breaks", legend=True)
plt.title("Social Exclusion Index", fontsize=20)
brt_lines.plot(ax=ax, alpha=1, markersize=3, legend=False,color='orange')
fig.savefig("social_exclusion.png")


# Another way of seeing the chloropleth
ct_excl.plot(column='IMU2010', cmap='Reds', legend=True)


## We use victim data set where there are no missing values for coordinates and for gender of the victim

vict_crs=pd.read_csv("vict2.csv")

### Create a geodatagrame and reproject it to the same CRS as the census tract shapefiles
vict_gdf = gpd.GeoDataFrame( vict_crs, crs="EPSG:4326",  geometry=points_from_xy(  vict_crs["longitud"], vict_crs["latitud"]),)
vict_gdf=vict_gdf.to_crs(urb_ct2.crs)

vict_gdf.to_file("vict_gdf.gpkg",layer="victim")


######## Verify that the victim data is projected correctly

fig,ax=plt.subplots(figsize=(20, 8))
urb_ct2.plot(ax=ax, alpha=0.5, legend=False)
vict_gdf.plot(ax=ax, alpha=0.5, markersize=2, legend=False)

# Spatial join of census tracts and victim point file

sjoin = gpd.sjoin(vict_gdf,urb_ct2, how='left', op='intersects')


# Set up to create chloropleth of crime and census tracts
polygon_id_field = 'CVEGEO'
count = sjoin.groupby(polygon_id_field)[polygon_id_field].count()
count.name='pointcount'
polygons = pd.merge(left=urb_ct2, right=count, left_on=polygon_id_field, right_index=True)

## Create chloropleth
fig, ax = plt.subplots(figsize=(20, 8))
polygons.plot(ax=ax, alpha=1.0, markersize=2, column="pointcount", scheme='natural_breaks',legend=True)
brt_lines.plot(ax=ax, alpha=1, markersize=3, legend=False,color='orange')
#plt.title("Total Crime by Census Tract, 2019-22", fontsize=20)
fig.savefig("crime_chloropleth.png")



##### Hexaplot using different measures of crime 

count_excl  = polygons.merge(excl, on='CVEGEO', how='left')

jg=sns.jointplot(data=count_excl,x="IMU2010",y="pointcount",kind="hex")
jg.set_axis_labels("Crime","Marginality")
jg.fig.suptitle("Hexaplot Crime and Marginality")
jg.fig.tight_layout()
jg.fig.savefig("hexa_count_crime_marginality.png")


## Vamos a hacer dos cosas: log y condicionar a que valroes sean positivos

count_excl['ln_crime']= np.log(count_excl.pointcount)
jg=sns.jointplot(data=count_excl,x="IMU2010",y="ln_crime",kind="hex")
jg.set_axis_labels("Crime","Marginality")
jg.fig.suptitle("Hexaplot Crime and Marginality")
jg.fig.tight_layout()
jg.fig.savefig("hexa_log_crime_marginality.png")






