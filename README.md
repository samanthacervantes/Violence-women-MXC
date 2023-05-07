# Violence Against Women in Mexico City

## Description and Results

In Mexico City, women are perceived to be disproportionately at risk of crime victimization in the areas near public transit stations, particularly for kidnapping, sexual assault, and robbery. This repository seeks to explore the relationship and assess if claims are founded using georeferenced victim crime data from the Attorney General Office and of the BRT system from the Mobility Secretariat of Mexico CIty for the period ranging from January 2019 to August 2022. The project does the following:

**Section I** describes how several types of crimes perpetrated towards women and men evolve through time, showing that 1) All crime and kidnappings are at least as perpetrated towards women relative to men, if not more, 2) that certain types of crime are gendered and of high incidence against women (such as domestic violence and sexual assault), 3) that violent crime against women has increased in the city for the period of study. Violent crime in this measure encompasses homicide, injuries, and feminicide (homicide involving sexual assault or by an intimate partner). 

**Section II** creates chloropleths of the Social Exclusion Index (by CONEVAL, the Mexican Agency of poverty measurement) and crime over Mexico City at the census tract level, as well as heatmaps of domestic violence and property theft in the City. The BRT sytem is overlayed in all maps, in order to be able to see the correlation between proximity to the public transit system (as the BRT and the subway systems overlap, composing the "fast" public modes of transport) and the aforementioned variables. Maps show that the center of the city is where most of crime is concentrated, as well as where most public transit points are. Furthermore, census tract that have high concentrations of crime seem to be also those that have richer households (measured as low values of Social Exclusion).

**Section III** conducts a "distance to nearest station analysis". In it, the distance of each crime to its nearest BRT station is computed using QGIS, and then exported to Python to create overlay density maps that compare the distance relative to the nearest station distribution of women and men, for different categories of crime. All types of crime are concentrated relatively near stations, but distributions peak at a 1-km radius from the station. When crimes are aggregated, crimes against men seem to be more clustered around stations than females'; however, other types of crime have more incidence near stations for women than for men, such as kidnapping. 

**Section IV** creates exclusive 1-km and 2-km buffers around the BRT system lines, counts how many crimes of different categories happen within each buffer, by sex of the victim, and then compares the ratio of female to male crime incidence of each type through the period of study. The ratio of female/male incidence of domestic violence, violent crime, and kidnapping of women increases over time and has a higher level in the 1-km area around stations relative to the 2-km one, suggesting that the neighborhoods around stations might indeed be more dangerous, and are in the trend of becoming more, towards women.  

## Documentation

There are four scripts in the repository. To what section of the analysis they are associated with, the data sources they use, how to obtain them and produce them, and the outputs of each script are described below. The order in which they appear is the order in which they should be ran. 

### Section I and III

The first one is "victim_crime_files.py". The link to obtain the victim crime data is directly used in the script. This file produces the time series plots and the distance to nearest station analysis, as well as "vict2.csv" the crime point file that will be used to conduct the nearest station analysis. The instructions to conduct this analysis are the following.

In QGIS, I imported the "df_ageb_urb.shp" shapefile of the urban census tracts of Mexico City obtained from "https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=702825292812". Then, I plotted over it the "Metrobus_estaciones_utm14n.shp" obtained from "https://datos.cdmx.gob.mx/dataset/geolocalizacion-metrobus" and the victim point files produced by "victim_crime_files.py", "vict2.csv". All files are in the repo. I reprojected the victim point files to the same CRS than the BRT stations, which is 32614 with UTN-18. I then duplicated the layer and in one duplicated filtered Sexo=="Femenino" (gender of victims being equal to females), and for the other one Sexo=="Masculino". Subsequently, I used "Join attributes by nearest", using as the Input layer the point layer (one for female, one for male) and over it the BRT stations layer. Then, I exported the two attribute tables as "nearest_fem.csv.zip" and "masc_nearest.csv.zip", for men and women, respectively. 

The heatmaps were created in QGIS first importing the "df_ageb_urb.shp" and "Metrobus_estaciones_utm14n.shp" as described earlier, then importing over it the "vict2.csv" data, and creating a duplicate layer of it. The first copy should filter the variable "property==1", and the second one "DV==0" (-1 denotes that the crime is _not_ domestic violence). Then, for each, go to the Layer Styling Panel, and choose "Heatmap" instead of "Single symbol", and then change the color ramp to red and the opacity to 70%. Finally, order station layer on top of the crime one. 

### Section II

The chloropleths are constructed with Mexico City's urban census tract as described in the previous paragraph and the 2010 Social Exclusion Index at the Census Tract level in Mexico City. As the document that contains all 2,435 census tracts cannot be found anymore, I provided the database that was saved before it was altered. This is called "exclusionindex.csv", and the script to create a unique identifier for each census tract that can be matched with the census tract shapefile is in "exclusion.py". For the crime chloropleth, the input is "vict2.csv" as described above. The script that produces the chloropleths is called "maps.py".

### Section IV

The input files for this section are "Metrobus_lineas_utm14n.shp", "df_ageb_urb.shp", and "vict_gdf.gpkg" The latter is an intermediate geopackage layer that contains the victim crime point file. 















