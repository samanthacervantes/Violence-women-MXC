#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 14:01:51 2023

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

# We download straight from the source the victims' files

vict=pd.read_csv("https://archivo.datos.cdmx.gob.mx/fiscalia-general-de-justicia/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico/apache_da_victimas_completa_agosto_2022.csv")

# To clean the data we remove those that are outside MXC and that are before 2019

# Convert year and age to numeric
vict["year"]=vict["Año_hecho"].astype(float)
vict["age"]=vict["Edad"].astype(float)

# Drop if less than 2018
vict=vict.query("year>2018")

# Drop if "out of MXC"
vict=vict.query("alcaldia_hechos!='FUERA DE CDMX'")


# False are denoted as -1 and True as 0


### Variable for underage

vict["minor"]=np.where((vict['age']<18) ,"minor","adult")


# Now an interactin term between both that indicates with 1 if both cases are true 

vict['DV_fem']=np.where((vict['DV']==0) & (vict['female']==0),1,0)

# We transform date to date format
vict["ymd"]=pd.to_datetime(vict["FechaHecho"],format="%Y-%m-%d")



# Delito, Sexo, Edad, Año_hecho, Mes_hecho, FechaHecho, HoraHecho, latitud, longitud

###### We create a variable for domestic violence  and another for female using string find
sub_dv ='VIOLENCIA FAMILIAR'

vict['DV']=vict["Delito"].str.find(sub_dv)
vict['female']=vict["Sexo"].str.find("Femenino")

## Descriptives
# Weekday
# Percentage men and women, and age

### Create other variables using np where and string find

vict["sexual"]=np.where((vict['Delito']=="ABUSO SEXUAL")|(vict['Delito']=="ABUSO SEXUAL")|(vict["Delito"].str.find("Feminicidio"))|
                        (vict['Delito']=="VIOLACION"),1,0)

### No jala 

vict["public"]=np.where((vict['Delito']=="DESAPARICION FORZADA DE PERSONAS")| (vict["Delito"].str.find("HOMICIDIO"))| (vict["Delito"].str.find("LESIONES"))| (vict["Delito"].str.find("PERSONAS EXTRA"))| (vict["Delito"].str.find("PRIV. ILE"))|(vict["Delito"].str.find("PRIVACION DE LA"))|(vict["Delito"].str.find("ROBO A TRANSEUNTE")) |(vict["Delito"].str.find("SECUESTRO"))|(vict["Delito"].str.find("TENTATIVA DE HOMICIDIO")),1,0)

print(vict["public"].unique())





####### Census data

## Census data for census tracts in Mexico City, 2010 and 2020

cen10=pd.read_csv('resultados_ageb_urbana_09_cpv2010.csv')
cen20=pd.read_csv('RESAGEBURB_09CSV20.csv')

#cen10['prim']=13*"0"
# df['cvegeo'] = df['zeros'].str.slice(1, 13-length)
#cen10=cen10.drop(['cvegeo'],axis=1)

# We format CT identifier to be the same way as shapefile for both years

# For 2010

cen10['ent'] = cen10['entidad'].astype(str)
cen10['ent'] = cen10['ent'].str.zfill(2)

cen10['muni'] = cen10['mun'].astype(str)
cen10['muni'] = cen10['muni'].str.zfill(3)

cen10['loca'] = cen10['loc'].astype(str)
cen10['loca'] = cen10['loca'].str.zfill(4)

cen10['CVEGEO']=cen10['ent']+cen10['muni']+cen10['loca']+cen10['ageb']

# For 2020

cen20['ent'] = cen20['ENTIDAD'].astype(str)
cen20['ent'] = cen20['ent'].str.zfill(2)

cen20['muni'] = cen20['MUN'].astype(str)
cen20['muni'] = cen20['muni'].str.zfill(3)

cen20['loca'] = cen20['LOC'].astype(str)
cen20['loca'] = cen20['loca'].str.zfill(4)

cen20['CVEGEO']=cen20['ent']+cen20['muni']+cen20['loca']+cen20['AGEB']


# We collapse the census 2020 data from blocks to census tracts

cen10 = cen10.query("nom_loc=='Total AGEB urbana'")
cen20 = cen20.query("NOM_LOC=='Total AGEB urbana'")

## We create relevant variables as percentages of population/households by CT ... To make PCA?

### Exclusion index
# Here is a variable called new_code. which is the relevant to merge

excl=pd.read_csv('exclusionindex.csv')

excl.drop(['CVEGEO'], axis=1)


excl['ent'] = excl['CVE_ENT'].astype(str)
excl['ent'] = excl['ent'].str.zfill(2)

excl['muni'] = excl['CVE_MUN'].astype(str)
excl['muni'] = excl['muni'].str.zfill(3)

excl['loca'] = excl['CVE_LOC'].astype(str)
excl['loca'] = excl['loca'].str.zfill(4)

# CVE ageb also needs four

excl['ageb'] = excl['CVE_AGEB'].astype(str)
excl['ageb'] = excl['ageb'].str.zfill(4)

excl['CVEGEO']=excl['ent']+excl['muni']+excl['loca']+excl['ageb']


########## Spatial files 

## Read spatial files (urban CT of MXC)

urb_ct=gpd.read_file("df_ageb_urb.shp")
urb_ct.plot()




## BRT lines (shapefile)

brt_lines=gpd.read_file("Metrobus_lineas_utm14n.shp",color='green')

#hola=brt_lines.plot(ax=urb_ct,color='green')

## CT and BRT line join

urb_ct2=urb_ct.to_crs("EPSG:32614")

ct_brt_join= pd.concat([urb_ct2.geometry,brt_lines.geometry])
ct_brt_join.plot()



# Merge exclusion index and CT

ct_excl  = urb_ct2.merge(excl, on='CVEGEO', how='left')

# Chloropleth of Social Exclusion Index. Cool! why cant I see lines?

fig, ax = plt.subplots(figsize=(20, 8))
ct_excl.plot(ax=ax, alpha=0.5, markersize=2, column="IMU2010", legend=False)
plt.title("Social Exclusion Index", fontsize=20)


ct_excl.plot(column='IMU2010', cmap='Reds', legend=True)

## Intento hacer victimas  ??? has geometry column
vict_gdf = gpd.GeoDataFrame( vict, crs="EPSG:32614",  geometry=points_from_xy(  vict["longitud"], vict["latitud"]),)

vict_ct  = urb_ct2.merge(vict_gdf)


vict_gdf.plot(markersize=1)


## Merge  victims with CT





## 
#joined = gpd.sjoin( taxi_gdf, urb_ct2, how='left', predicate="within")

#joined.plot()
#fig, ax = plt.subplots(figsize=(20, 8))
#joined.plot(ax=ax, alpha=0.5, markersize=2, column="pickup_ngbhood_name", legend=False)
#plt.title("Pickups Colored by Neighborhood", fontsize=20)




















