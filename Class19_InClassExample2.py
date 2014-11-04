# -*- coding: utf-8 -*-
from suds.client import Client
from pandas import Series

#Create a new object named NWIS for calling the web service methods (https://fedorahosted.org/suds/wiki/Documentation)
NWIS = Client("http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL").service

#Call the GetValuesObject method (http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?op=GetValuesObject)
response = NWIS.GetValuesObject("USGS:10109000", "USGS:00060", "2014-10-31", "2014-11-4")
#(If you get an error message saying ‘Error connecting to USGS’, double check your Internet connection and the input parameters above.)

#create a Pandas Series object from the response
a = []
b = []
values = response.timeSeries.values.value
for v in values: a.append(v.value)
for v in values: b.append(v._dateTime)
ts = Series(a, index=b)


#print the site’s minimum value and datetime of occurrence to the console
print "Minimum streamflow was %s cfs on %s"%(ts.min(), ts.idxmin())
#(this should produce the following output: Min streamflow was 101 cfs on 2014-11-01 10:30:00.)

