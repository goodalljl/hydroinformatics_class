# -*- coding: utf-8 -*-
"""
Simple example of using Pydap for accessing data from a OPeNDAP/DODS server.
Code plots precipitation data used as forcing for NLDAS.

Author: Jon Goodall (goodall@virigina.edu)
Last Modified: November 20, 2014
"""

# -*- coding: utf-8 -*-
from pydap.client import open_url
from netCDF4 import num2date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#URL is OPeNDAP/DODS Data URL provided at the top of the GDS page 
# (e.g., http://hydro1.sci.gsfc.nasa.gov/dods/NLDAS_FOR0125_H.001.info)
url = 'http://hydro1.sci.gsfc.nasa.gov:80/dods/NLDAS_FOR0125_H.001'

#variables are defined on the GDS page as well
variable = 'prdarsfc' #this is precipitation hourly total from stageii [kg/m^2] 
                      #   according to info on the URL provided above

dataset = open_url(url)
prdarsfc = dataset[variable]

# get precip for Charlottesvile Airport (38.1386° N, 78.4528° W)
#get the first element in the time dimension
print "getting data from http://hydro1.sci.gsfc.nasa.gov ..."
grid = prdarsfc[100000:100080, (38.1875 == prdarsfc.lat), (-78.4375 == prdarsfc.lon)] 
print " -- success!"

print "creating plot ..."
dt = num2date(grid.time[:], dataset.time.units)
values = [v[0][0] if v != -9999.00 else None for v in grid.prdarsfc[:]]

ts = pd.Series(values, index=dt)
ax = ts.plot()
ax.set_ylabel(prdarsfc.long_name)

plt.show()
print " -- success!"
print "FINISHED"
