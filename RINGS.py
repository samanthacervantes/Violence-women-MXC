#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 21:28:12 2023

@author: samcerv
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os 
from geopandas import points_from_xy

### This is a document to create exclusive 1 and 2 km buffers around BRT lines to then 
## compare counts of crime through time in the inner vs outer layer

brt_lines=gpd.read_file("Metrobus_lineas_utm14n.shp",color='green')

## dissolve

# List of radii

radius=[1000,2000]

# Create empty geodataframe

ring_layer=gpd.GeoDataFrame()

ring_layer['radius'] = radius


#Build the geometries of the rings. Empty list:

geo_list=[]

# create the buffers moving outward from the interstate.variable will be used to make the buffers into rings by allowing us 
#to subtract out the previous buffer when building the next one.

last_buf=None

# Loop 

for r in radius:
    this_buf=brt_lines.buffer(r)
    if len(geo_list)==0:
        geo_list.append(this_buf[0])
    else:
        change=this_buf.difference(last_buf)
        geo_list.append(change[0])
    last_buf=this_buf

ring_layer['geometry']=geo_list

# Set the CRS of the ring layer to the CRS of the BRT lines layer

ring_layer=ring_layer.set_crs(brt_lines.crs)


# Read census tract shapefiles. 
urb_ct=gpd.read_file("df_ageb_urb.shp")

#Reproject urb_ct so that it matches the projection used with the rings 
urb_ct=urb_ct.to_crs(ring_layer.crs)
brt_lines=brt_lines.to_crs(ring_layer.crs)

## Dissolve lines are there are seven of them 

brt_lines2 = brt_lines.dissolve()

# Overlay the ring layers to the brt lines

slices=gpd.overlay(brt_lines2,ring_layer,how='union',keep_geom_type=True)

# Drop the areas that are outside the buffers

slices=slices.dropna(subset=['radius'])


# We read the victim spatial data frame created before 
#vict_gdf=gpd.read_file("vict_gdf.gpkg",layer="victim")

urb_ct2=urb_ct.to_crs("EPSG:32614")
vict_crs=pd.read_csv("vict2.csv")

### Create a geodatagrame and reproject it to the same CRS as the census tract shapefiles
vict_gdf = gpd.GeoDataFrame( vict_crs, crs="EPSG:4326",  geometry=points_from_xy(  vict_crs["longitud"], vict_crs["latitud"]),)
vict_gdf=vict_gdf.to_crs(urb_ct2.crs)


# Overlay of the radius and the victim points

vict_buff=gpd.overlay(vict_gdf,ring_layer,how='union',keep_geom_type=True)

vict_buff2=vict_buff.dropna(subset=['radius'])


# Collapse crime counts by month and radius...

vict_buff2["n"]=1

buff_mon = vict_buff2.groupby(["Month_Year","radius"]).sum()

#### We create ratio variables 

buff_mon["ratio_DV"]=buff_mon["DV_fem"]/buff_mon["DV_masc"]
buff_mon["ratio_tot"]=buff_mon["Women"]/buff_mon["Men"]
buff_mon["ratio_viol"]=buff_mon["Violent_fem"]/buff_mon["Violent_masc"]
buff_mon["ratio_freedom"]=buff_mon["Freedom_fem"]/buff_mon["Freedom_masc"]
buff_mon["ratio_prop"]=buff_mon["Prop_fem"]/buff_mon["Prop_masc"]


# Unstack the data to create separate columns for the primary and general elections 

radius_wide=buff_mon.unstack("radius")


### Quick analysis of several variables

# List of elements for tuple

cols=radius_wide.columns.get_level_values(0)
cols=cols.drop_duplicates()


plot_info=["ratio_DV", "ratio_tot", "ratio_viol", "ratio_freedom", "ratio_prop"]
# Create variable equal to one

nfig=1

# Loop to make graphs

for var in plot_info:
    fig,ax=plt.subplots()
    fig.suptitle(f"Figure {nfig}: Female/Male ratio, Inner vs Outer ring")
    df=radius_wide[var]
    df.plot(ax=ax)
    ax.set_ylabel(var)
    ax.set_xlabel("Date")
    fig.tight_layout()
    nfig=nfig+1
    fig.savefig(f"fig{nfig}.png")


## We do the same plot but onyl showing the inner and outer ring trend for DV against women.

x=radius_wide["DV_fem"]

# Begin new figure

fig1,ax1=plt.subplots(dpi=300)
fig1.suptitle("Ratio of DV against women in Inner vs Outer rings")
# Plot all crime 
x.plot(ax=ax1)
ax1.set_xlabel("Date")
ax1.set_ylabel("DV")
fig1.tight_layout()
fig1.savefig("inner_vs_outer_DV_fem.png")















