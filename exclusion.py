#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:40:33 2023

@author: samcerv
"""


# Set up

import re
import requests
import pandas as pd
import geopandas as gpd
import seaborn as sns
import geopandas as gpd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from geopandas import points_from_xy
plt.rcParams['figure.dpi'] = 300




### Exclusion index at Census Tract level in Mexico City, 2010
# We create for the exclusion index the CT identifier as before.
# I use a Social Exclusion Index for 2010 because edits were made to an "updated" version in which
#now there are only 1/5 of original observations and the CT identifier is different. The one I have
# is more reliable and can be match with CT data.

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

excl.to_csv("excl.csv")


## If we were using both 2010 and 2020 censuses and wanted to create an ID for the variables:

# Add suffix to identify variables 
#cen10=cen10.add_suffix('_c10')
#cen20=cen10.add_suffix('_c20')



