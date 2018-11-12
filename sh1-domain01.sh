#!/bin/sh

# ------------------------------- Created by Gessei Matsumoto at April 13, 2018.
# This script costs about 6m35s in this iMac.
#
FC=gfortran
DOPT="-fbacktrace"
COPT="-fconvert=big-endian -frecord-marker=4"
NOPT="-I/usr/local/netcdf4/include -L/usr/local/netcdf4/lib -lnetcdff"

#
# Create 
#
mkdir -p Output
cd Domain01
exe=step1d01readGeog_em
fort_src=${exe}.f95
$FC ${fort_src} $COPT $NOPT $DOPT -o $exe
./$exe
rm -fv $exe *.o

#
# Create grouped shape file clipped in 5km
#
python3 step2d01gsiTo5kmShp.py

#
# Create files, LU_INDEX & LANDUSEF deduced in domaon01
#
python3 step3d01toCategory.py


#
# Over write
#
exe=step4d01overWrite
fort_src=${exe}.f95
$FC ${fort_src} $COPT $NOPT $DOPT -o $exe
./$exe
rm -fv $exe *.o
