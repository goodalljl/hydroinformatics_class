import urllib
import netCDF4
from datetime import datetime
import os

#get the file if it doesn't alreay exist in the working direcotry
if os.path.exists('nws_precip_conus_20141117.nc') == False:
    print "getting file ..."
    urllib.urlretrieve("http://water.weather.gov/precip/p_download_new/" +\
        "2014/11/17/nws_precip_conus_20141117.nc", \
        "nws_precip_conus_20141117.nc")

#Open netCDF file for reading
ds = netCDF4.Dataset("nws_precip_conus_20141117.nc", "r")

#Create variable for amountofprecip
amountOfPrecip = ds.variables['amountofprecip']

#extract metadata for variable
name = amountOfPrecip.long_name
units = amountOfPrecip.units
dt = amountOfPrecip.dateofdata

#create datetime 
dt = datetime.strptime(dt, '%Y%m%d%HZ')

#get precip for Charlottesville, VA Airport (hrapy = 514, hrapx = 943)
# - note: I optained the HRAP coordinates from this file:
#   http://water.weather.gov/precip/p_download_new/nws_precip_allpoint.tar.gz 
precip = amountOfPrecip[514, 943]

#perform unit conversion to get precip in inches
precip_in = precip * 0.01 / 25.4

#print out precip
print "Charlottesville airport received %0.2f inches of precipitation on %s." \
    %(precip_in, dt.strftime("%b %d, %Y")) 