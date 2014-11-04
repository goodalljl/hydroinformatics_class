# -*- coding: utf-8 -*-
from suds.client import Client

#Create a new object named NWIS for calling the web service methods (https://fedorahosted.org/suds/wiki/Documentation)
NWIS = Client("http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?WSDL").service

#Call the GetSiteInfoObject method (http://river.sdsc.edu/wateroneflow/NWIS/UnitValues.asmx?op=GetSiteInfo)
response = NWIS.GetSiteInfoObject("USGS:10109000")

#print the site’s name to the console
print response.site[0].siteInfo.siteName
#(this should produce the following output)
#LOGAN RIVER ABOVE STATE DAM, NEAR LOGAN, UT
