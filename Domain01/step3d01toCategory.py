#! /Library/Frameworks/Python.framework/Versions/3.6/bin
# -*- coding: utf-8 -*-

# ----- 10 ------ 20 ------ 30 ------ 40 ------ 50 ------ 60 ------ 70 ------ 80
# 
# 
# ----- 10 ------ 20 ------ 30 ------ 40 ------ 50 ------ 60 ------ 70 ------ 80

# ------------------------------------------------------------- Sectin of Import
import os,sys,shutil                    # os,sys,shutil
import numpy as np                      # numpy
import pandas as pd
import shapely.geometry as sg
import geopandas as gpd

# Category numbers of landuse used in this study
catNum = 33

# file names for output, which indicate GSI landuse
outFile1 = "../Output/gsid01_luindex.txt"                   # Domain01
outFile2 = "../Output/gsid01_landusef.txt"  
fw1 = open(outFile1, 'w')
fw2 = open(outFile2, 'w')

# read lon, lat,  used by Pandas
llFile = "../Output/lu_lmd01.txt"                          # Domain01
pdData  = pd.read_csv(llFile, delim_whitespace=True, header=None,
                      names=('i','j','lon','lat','landuse','landmask') )

# shapefile
shpfile = "../Output/土地利用d01_5km区分.shp"       # Domain01
df = gpd.read_file(shpfile, encoding='utf-8')
g = gpd.GeoSeries(df.geometry)

# One by One
'''latLon = (130.33041, 33.59555)          # Around Odo
#latLon = (130.2315, 33.7656)              # North of Genkai Island
pt    = sg.Point(latLon)

A = g.contains(pt) idx = np.where(A == True) if (len(idx[0]) == 1):
print (latLon, idx[0][0],df.landCatego[idx[0][0]]) else: print
(latLon, " isn't contained")
'''

# Loop
for i in np.arange(len(pdData)):
#for i in np.arange(2):
    latLon = pdData.loc[i,['lon','lat']]
    pt    = sg.Point(latLon)

    A = g.contains(pt)
    idx = np.where(A == True)
    if (len(idx[0]) == 1):
       # lu_index section
       formatted_num \
          = "%f\t%f\t%i" %(latLon['lon'],latLon['lat'],df.landCatego[idx[0][0]])
       fw1.write(formatted_num)

       # landusef section
       temp = df.landCatego[idx[0][0]]
       vec = np.zeros(33)
       vec[4]  = df.modis05[idx[0][0]]
       vec[9]  = df.modis10[idx[0][0]]
       vec[11] = df.modis12[idx[0][0]]
       vec[12] = df.modis13[idx[0][0]]
       vec[13] = df.modis14[idx[0][0]]
       vec[16] = df.modis17[idx[0][0]]
       form1 = "%f\t%f" %(latLon['lon'],latLon['lat'])
       fw2.write(form1)
       for i in np.arange(catNum):
          form2 = "\t%4.2f" %(vec[i])
          fw2.write(form2)
       
    else:
       # lu_index section
       formatted_num = "%f\t%f\t17" %(latLon['lon'],latLon['lat'])
       fw1.write(formatted_num)
       
       # landusef section
       vec = np.zeros(33)
       vec[16] = 1.0
       form1 = "%f\t%f" %(latLon['lon'],latLon['lat'])
       fw2.write(form1)
       for i in np.arange(catNum):
          form2 = "\t%4.2f" %(vec[i])
          fw2.write(form2)
       
    fw1.write('\n')
    fw2.write('\n')
    
fw1.close()
fw2.close()
# -------------------------------------------------------------------- Clean up
#shutil.rmtree("./__pycache__")












