# -*- coding: utf-8 -*-
import json
import urllib2

"""
This code will find the distance between two points on the NHD network.
It uses the EPA WATERS Web Services, in particular the Point Indexing service
and the Navigation service. 

These services are described here:
    http://water.epa.gov/scitech/datait/tools/waters/services/index.cfm

The tool requires an Internet connection to work.

Users should input the lat/lon for the two points below. One way to get these
coordinates is using this website http://itouchmap.com/latlong.html or 
simply clicking on a location in Google Maps.

Author: Jon Goodall (goodall@virignia.edu)
Last modified: November 12, 2014.
"""

#-------------------------------------------------------------------------------
#USER INPUT: 

#downstream point
lonPt1 = -78.623751
latPt1 = 38.479505

#upstream point
lonPt2 = -78.635252
latPt2 = 38.409105

#-------------------------------------------------------------------------------

def pointIndexing(lon, lat):
    """
    Uses the EPA WATERS Web Services to identify the comid and measure along
    an NHD feature for a given lat/lon
    
    Parameters:
            lat: the latitude in decimal degrees of the point
            lon: the longitude in decimal degrees of the point
    
    Returns:
            comID, measure where measure is the fmeasure attribute returned 
            by the PointIndexing service. 
    """
    
    #build the point indexing URL
    PtServiceUrl = "http://ofmpub.epa.gov/waters10/PointIndexing.Service?" \
        + "pGeometry=POINT(%s+%s)"%(lon, lat) \
        + "&pGeometryMod=WKT%2CSRID%3D8265" \
        + "&pResolution=3" \
        + "&pPointIndexingMethod=DISTANCE" \
        + "&pPointIndexingMaxDist=25" \
        + "&pOutputPathFlag=FALSE" \
        + "&pReturnFlowlineGeomFlag=FALSE" \
        + "&optNHDPlusDataset=2.1" \
        + "&optCache=1415731048364" \
        + "&optJSONPCallback="

    #load response into JSON object
    response = json.loads(urllib2.urlopen(PtServiceUrl).read()) 
    
    #check the status message from the response to see if it worked
    status_message = response['status']['status_message']
    if status_message == "No Results Returned.":
        raise Exception('Point service did not find an NHD feature for ' + \
            'lat=%s, lon=%s. Please double check your coordinates.'%(lat, lon))
    
    #extract comids and measures
    comid = response['output']['ary_flowlines'][0]['comid']
    measure = response['output']['ary_flowlines'][0]['fmeasure']
    
    return comid, measure

#get the comid and measure for the two points
comid1, measure1 = pointIndexing(lonPt1, latPt1)
comid2, measure2 = pointIndexing(lonPt2, latPt2)

#build the URL to call the navigation service
NavigationServiceUrl = "http://ofmpub.epa.gov/waters10/Navigation.Service?" \
    + "pNavigationType=PP" \
    + "&pStartPermanentIdentifier=%s"%(comid2) \
    + "&pStartMeasure=%s"%(measure2) \
    + "&pStopPermanentIdentifier=%s"%(comid1) \
    + "&pStopMeasure=%s"%(measure1) \
    + "&pReturnFlowlineAttr=TRUE" \
    + "&optNHDPlusDataset=2.1" \
    + "&optCache=1415731050350" \
    + "&pReturnFlowlineAttr=False" \
    + "&optJSONPCallback="

#load response into JSON object
response = json.loads(urllib2.urlopen(NavigationServiceUrl).read())

#check the status message from the response to see if it worked
status_message = str(response['status']['status_message'])
if status_message != "None": 
    raise Exception("Error: " + status_message)

#extract and print the distance between the two points
totalDist = response['output']['ntNavResultsStandard'][-1]['totaldist']
print "The flowline distance between the (%s, %s) and (%s, %s) is %0.2f km." \
    %(latPt1, lonPt1, latPt2, lonPt2, totalDist)