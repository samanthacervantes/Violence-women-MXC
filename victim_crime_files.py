#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:22:53 2023

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
import zipfile
import numpy as np
import matplotlib.pyplot as plt
from geopandas import points_from_xy
plt.rcParams['figure.dpi'] = 300
plt.style.use('seaborn-white')
import plotly.express as px
import plotly.figure_factory as ff
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.io import show, output_notebook
from bokeh.io import curdoc
curdoc().theme = 'light_minimal'
import warnings
warnings.filterwarnings("ignore")

# We download the victims' files from the Attorney files

vict=pd.read_csv("https://archivo.datos.cdmx.gob.mx/fiscalia-general-de-justicia/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico/apache_da_victimas_completa_agosto_2022.csv")

# To clean the data we remove those that are outside MXC and that are before 2019, first by
# making year (and age) numeric variables

# Convert year and age to numeric
vict["year"]=vict["Año_hecho"].astype(float)
vict["age"]=vict["Edad"].astype(float)

# Drop if less than 2019
vict=vict.query("year>2018")

# Drop if "out of MXC"
vict=vict.query("alcaldia_hechos!='FUERA DE CDMX'")


### Variable for underage and sex

vict["minor"]=np.where((vict['age']<18) ,"minor","adult")
vict['female']=vict["Sexo"].str.find("Femenino")
vict['male']=vict["Sexo"].str.find("Masculino")

# Where False are denoted as -1 and True as 0


# We transform date to date format
vict["ymd"]=pd.to_datetime(vict["FechaHecho"],format="%Y-%m-%d")

############## CREATE CRIME VARIABLES 

###### We create a variable for domestic violence  
sub_dv ='VIOLENCIA FAMILIAR'
vict['DV']=vict["Delito"].str.find(sub_dv)

# Now creat DV where victims are female and male based on previous definitions of variables 

vict['DV_fem']=np.where((vict['DV']==0) & (vict['female']==0),1,0)
vict['DV_masc']=np.where((vict['DV']==0) & (vict['female']==-1),1,0)


### Create other variables using np.where and string contains

# Sexual crimes: abuse, harassment, and rape

vict["sexual"]=np.where(((vict['Delito']=="ABUSO SEXUAL")|(vict["Delito"].str.contains("ACOSO"))|(vict['Delito']=="VIOLACION")),1,0)
vict['Sexual_fem']=np.where((vict['sexual']==1) & (vict['female']==0),1,0)
vict['Sexual_masc']=np.where((vict['sexual']==1) & (vict['female']==-1),1,0)

### Violent: homicide, injuries, attempted murder

vict["violent"]=np.where(((vict["Delito"].str.contains("HOMICIDIO"))| (vict["Delito"].str.contains("LESIONES"))|(vict["Delito"].str.contains("TENTATIVA DE HOMICIDIO"))| (vict["Delito"].str.contains("FEMINICIDIO"))),1,0)
vict['Violent_fem']=np.where((vict['violent']==1) & (vict['female']==0),1,0)
vict['Violent_masc']=np.where((vict['violent']==1) & (vict['female']==-1),1,0)

### Freedom: kidnapping, "forzed abduction", missing people, child abduction

vict["freedom"]=np.where(((vict['Delito']=="DESAPARICION FORZADA DE PERSONAS")| (vict["Delito"].str.contains("PERSONAS EXTRA"))|  (vict["Delito"].str.contains("SECUESTRO"))| (vict["Delito"].str.contains("SUSTRACCIÓN DE MENORES"))),1,0)
vict['Freedom_fem']=np.where((vict['freedom']==1) & (vict['female']==0),1,0)
vict['Freedom_masc']=np.where((vict['freedom']==1) & (vict['female']==-1),1,0)


### Property
robo=vict["Delito"].str.contains("ROBO")
vict["property"]=robo.astype(int)
vict['Prop_fem']=np.where((vict['property']==1) & (vict['female']==0),1,0)
vict['Prop_masc']=np.where((vict['property']==1) & (vict['female']==-1),1,0)


### Feminicide

vict["Feminicide"]=np.where((vict["Delito"].str.contains("FEMINICIDIO")),1,0)



# verify that values have 0s and 1
print(vict["property"].unique())

## As female are coded as 0 and male as -1, we create new variables that make them 0 and 1 

vict["Women"]=vict["female"]+1
vict["Men"]=vict["male"]+1


#### We create a new df without Nan for male or female

vict2=vict.dropna(subset=['female', 'male'])

# Create a month and year variable
vict2['Month_Year'] = vict["ymd"].dt.to_period('M')

# And collapse by month-year to sum crime by each category monthly

vict3=vict2.groupby('Month_Year')
crimes_month=vict3.sum()

### Time series plots

# Total Crime
vict4=crimes_month[['Women','Men']]
vict4.plot().set(title='Total Crime, by Gender, 2019-22')


# Domestic Violence

vict5=crimes_month[['DV_fem','DV_masc']]
vict5.plot().set(title='Domestic Violence, by Gender, 2019-22')

# Sexual crimes

vict6=crimes_month[['Sexual_fem','Sexual_masc']]
vict6.rename(columns={'Sexual_fem': 'Women', 'Sexual_masc': 'Men'}, inplace=True)
vict6.plot().set(title='Sexual Assault, by Gender, 2019-22')

## Violent 
vict7=crimes_month[['Violent_fem','Violent_masc']]
vict7.rename(columns={'Violent_fem': 'Women', 'Violent_masc': 'Men'}, inplace=True)
vict7.plot().set(title='Violent Crime, by Gender, 2019-22')

# Freedom/kidnapping

vict8=crimes_month[['Freedom_fem','Freedom_masc']]
vict8.rename(columns={'Freedom_fem': 'Women', 'Freedom_masc': 'Men'}, inplace=True)
vict8.plot().set(title='Kidnapping, by Gender, 2019-22')


# Feminicide
vict9=crimes_month[['Feminicide']]
#vict8.rename(columns={'Freedom_fem': 'Women', 'Freedom_masc': 'Men'}, inplace=True)
vict9.plot()
#vict9.plot().set(title='Kidnapping, by Gender, 2019-22')

# Violent female 
vict10=crimes_month[['Violent_fem']]
#vict8.rename(columns={'Freedom_fem': 'Women', 'Freedom_masc': 'Men'}, inplace=True)
vict10.plot()

# Drop observations where latitude or longitude information is missing 

vict = vict[vict.latitud != 0]
vict = vict[vict.longitud != 0]

vict.to_csv("vict.csv")

vict2 = vict2[vict2.latitud != 0]
vict2= vict2[vict2.longitud != 0]

vict2.to_csv("vict2.csv")

#####################################################
########## NEAREST STATION ANALYSIS
#####################################################

# For this section, I import from QGIS the attribute layers where:
# 1 BRT stations were projected in the Mexico City map
# 2. Female and male victim point files were projected in the map
# 3. Reprojected them to have the same crs as the station
# 4. joined the victim data with the stations using the "Join attributes by nearest"
# 5. exported the joint layers as "nearest_fem.csv" and "masc_nearest.csv"

fem_nearest=pd.read_csv("nearest_fem.csv.zip")
fem_nearest=fem_nearest[['CVE_EST','feature_x', 'Sexo','Delito','Edad']]
masc_nearest=pd.read_csv("masc_nearest.csv.zip")
masc_nearest=masc_nearest[['CVE_EST','feature_x', 'Sexo','Delito','Edad']]

nearest=pd.concat([fem_nearest,masc_nearest])

## Creamos indicadores de sexo y edad

nearest['female']=nearest["Sexo"].str.find("Femenino")
nearest['young']=np.where((nearest['Edad']<35),1,0)


## Sexual

nearest["sexual"]=np.where(((nearest['Delito']=="ABUSO SEXUAL")|(nearest["Delito"].str.find("ACOSO"))|(nearest['Delito']=="VIOLACION")),1,0)
nearest['Sexual_fem']=np.where((nearest['sexual']==1) & (nearest['female']==0),1,0)
nearest['Sexual_masc']=np.where((nearest['sexual']==1) & (nearest['female']==-1),1,0)
near_sex=nearest.query("sexual==1")

## Kidnapping

nearest["freedom"]=np.where(((nearest['Delito']=="DESAPARICION FORZADA DE PERSONAS")| (nearest["Delito"].str.contains("PERSONAS EXTRA"))|  (nearest["Delito"].str.contains("SECUESTRO"))| (nearest["Delito"].str.contains("SUSTRACCIÓN DE MENORES"))),1,0)
nearest['Freedom_fem']=np.where((nearest['freedom']==1) & (nearest['female']==0),1,0)
nearest['Freedom_masc']=np.where((nearest['freedom']==1) & (nearest['female']==-1),1,0)
near_kidn=nearest.query("freedom==1")


##### Overlay density estimates

## Kidnapping using the whole distribution of distance to nearest station
near_kidn=near_kidn.reset_index()
fig,ax1=plt.subplots(dpi=300)
sns.kdeplot(data=near_kidn,x="feature_x",palette="rocket",hue="Sexo",fill=True,ax=ax1)
ax1.set_xlabel("Distance to Nearest Station")
ax1.set_xlim(0, 25000)
fig.tight_layout()

## Kidnapping up to 5km from nearest station
fig,ax1=plt.subplots(dpi=300)
sns.kdeplot(data=near_kidn,x="feature_x",palette="rocket",hue="Sexo",fill=True,ax=ax1)
ax1.set_xlabel("Distance to Nearest Station")
ax1.set_xlim(0, 5000)
fig.tight_layout()

## All crime using the whole distribution of distance to nearest station
nearest=nearest.reset_index()
fig,ax1=plt.subplots(dpi=300)
sns.kdeplot(data=nearest,x="feature_x",palette="mako",hue="Sexo",fill=True,ax=ax1)
ax1.set_xlabel("Distance to Nearest Station")
ax1.set_xlim(0, 25000)
fig.tight_layout()

fig,ax1=plt.subplots(dpi=300)
sns.kdeplot(data=nearest,x="feature_x",palette="mako",hue="Sexo",fill=True,ax=ax1)
ax1.set_xlabel("Distance to Nearest Station")
ax1.set_xlim(0, 5000)
fig.tight_layout()








