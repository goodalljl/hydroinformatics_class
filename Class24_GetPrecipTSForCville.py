"""
Creates a precipitation time series for Charlottesville Airport using the NWS 
AHPS precipitation data available here: 
http://water.weather.gov/precip/download.php

Code will automtically download required files if files are not available within
the current working directory.

To change the location, find the hrapx and hrapy coordianates for the location
using this shapefile: http://water.weather.gov/precip/p_download_new/
nws_precip_allpoint_conversion.tar.gz
Then update the hrapx and hrapy variables to the new location.

Author: Jon Goodall (goodall@virginia.edu)
Last updated: November 19, 2014
"""


import urllib
import netCDF4
from datetime import datetime, timedelta
import os

# --- USER INPUT ----
start = "11-10-2014"
end = "11-17-2014"
hrapy = 514 #these are coordinates for the Charlottesville, VA airport
hrapx = 943
# -------------------

#convert start and end to datetime objects
startTime = datetime.strptime(start, "%m-%d-%Y")
endTime = datetime.strptime(end, "%m-%d-%Y")

currentTime = startTime

#open file for writing output
f = open("precip.csv", "w")
f.write("DateTime, Precip_in\n")

while currentTime <= endTime:
    
    print "working on %s"%(currentTime.strftime("%m-%d-%Y"))
    
    #get the file if it doesn't alreay exist in the working direcotry
    if os.path.exists('nws_precip_conus_%s.nc' \
            %(currentTime.strftime("%Y%m%d"))) == False:
        print " --- getting netCDF file from water.weather.gov"
        urllib.urlretrieve("http://water.weather.gov/precip/p_download_new/" \
            + "%s/%s/%s/nws_precip_conus_%s.nc" \
            %(currentTime.strftime("%Y"), currentTime.strftime("%m"), \
            currentTime.strftime("%d"), currentTime.strftime("%Y%m%d")), \
            "nws_precip_conus_%s.nc"%(currentTime.strftime("%Y%m%d")))
        print " --- got netCDF file from water.weather.gov"
    
    print " --- reading precipitation out of netCDF file."
    #Open netCDF file for reading
    ds = netCDF4.Dataset("nws_precip_conus_%s.nc"\
        %(currentTime.strftime("%Y%m%d")), "r")
    
    #Create variable for amountofprecip
    amountOfPrecip = ds.variables['amountofprecip']
    
    #extract metadata for variable
    name = amountOfPrecip.long_name
    units = amountOfPrecip.units
    dateOfData = amountOfPrecip.dateofdata
    
    #create datetime 
    dateOfDataObj = datetime.strptime(dateOfData, '%Y%m%d%HZ')
    
    #get precip for Charlottesville, VA Airport (hrapy = 514, hrapx = 943) 
    precip = amountOfPrecip[hrapy, hrapx]
    
    #perform unit conversion to get precip in inches
    precip_in = precip * 0.01 / 25.4

    print " --- writing precipitation to the output file"
    
    #print out precip
    f.write("%s, %0.5f\n"%(currentTime.strftime("%b %d, %Y"), precip_in)) 
    
    #increment the current time by 1 day
    currentTime = currentTime + timedelta(days=1)
    
    print " --- success!"

print "closing output file."
f.close()
print "FINISHED!"