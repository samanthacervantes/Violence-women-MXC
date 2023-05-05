# Violence Against Women in Mexico City

## Description and Results

In Mexico City, women are perceived to be disproportionately at risk of crime victimization in the areas near public transit stations, particularly for kidnapping, sexual assault, and robbery. This repository seeks to explore the relationship and assess if claims are founded using georeferenced victim crime data from the Attorney General Office and of the BRT system from the Mobility Secretariat of Mexico CIty for the period ranging from January 2019 to August 2022. The project does the following:

The Section I describes how several types of crimes perpetrated towards women and men evolve through time, showing that 1) All crime and kidnappings are at least as perpetrated towards women relative to men, if not more, 2) that certain types of crime are gendered and of high incidence against women (such as domestic violence and sexual assault), 3) that violent crime against women has increased in the city for the period of study. Violent crime in this measure encompasses homicide, injuries, and feminicide (homicide involving sexual assault or by an intimate partner). 

Section II creates chloropleths of the Social Exclusion Index (by CONEVAL, the Mexican Agency of poverty measurement) and crime over Mexico City at the census tract level, as well as heatmaps of domestic violence and property theft in the City. The BRT sytem is overlayed in all maps, in order to be able to see the correlation between proximity to the public transit system (as the BRT and the subway systems overlap, composing the "fast" public modes of transport) and the aforementioned variables. Maps show that the center of the city is where most of crime is concentrated, as well as where most public transit points are. Furthermore, census tract that have high concentrations of crime seem to be also those that have richer households (measured as low values of Social Exclusion).

Section III conducts a "distance to nearest station analysis". In it, the distance of each crime to its nearest BRT station is computed using QGIS, and then exported to Python to create overlay density maps that compare the distance relative to the nearest station distribution of women and men, for different categories of crime. All types of crime are concentrated relatively near stations, but distributions peak at a 1-km radius from the station. When crimes are aggregated, crimes against men seem to be more clustered around stations than females'; however, other types of crime have more incidence near stations for women than for men, such as kidnapping. 

Section IV creates exclusive 1-km and 2-km buffers around the BRT system lines, counts how many crimes of different categories happen within each buffer, by sex of the victim, and then compares the ratio of female to male crime incidence of each type through the period of study. The pattern for crimes is for the ratio of female/male incidence to increase over time in the 1-km area around stations relative to the 2-km one, suggesting that the neighborhoods around stations might indeed may be becoming more dangerous towards women.  

## Documentation

There are four scripts in the repository. To what section of the analysis they are associated with, the data sources they use, as well as how to obtain them and produce them, and the outputs of each script are described below. 

### Section I and III

The first one is "victim_crime_files.py". The link to obtain the victim crime data is directly used in the script. This file produces the time series plots and the distance to nearest station analysis, as well as "vict2.csv" the crime point file that will be used to conduct the nearest station analysis. The instructions to conduct this analysis are the following.

In QGIS, I imported the "df_ageb_urb.shp" shapefile of the urban census tracts of Mexico City obtained from "https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=702825292812". Then, I plotted over it the "Metrobus_estaciones_utm14n.shp" obtained from "https://datos.cdmx.gob.mx/dataset/geolocalizacion-metrobus" and the victim point files produced by "victim_crime_files.py", "vict2.csv". I then duplicated the layer and in one duplicated filtered Sexo=="Femenino" (gender of victims being equal to females), and for the other one Sexo=="Masculino". Subsequently, I used "Join attributes by nearest", using as the Input layer the point layer (one for female, one for male) and over it the BRT stations layer. Then, I exported the two attribute tables as "nearest_fem.csv.zip" and "masc_nearest.csv.zip", for men and women, respectively. 


(2) include instructions on how to obtain the original input data, such as where it can be downloaded or it should provide a script to download the data via an API; (3) explain what each script does and the order in which they should be run; (4) explain any additional files provided in the repository

















