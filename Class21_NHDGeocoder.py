import urllib2 
import json
from pprint import pprint

#input by user
Name = "Ivy Creek"
State = "VA"

#build URL
url = "http://ofmpub.epa.gov/waters10/Name.Service?" \
    + "pFullText=" + Name.replace(' ', '+') \
    + "&pFullTextRegex=" \
    + "&pBasename=" \
    + "&pBasenameRegex=" \
    + "&pHydrography=" \
    + "&pHydrographyRegex=" \
    + "&pDirectional=" \
    + "&pDirectionalRegex=" \
    + "&pOperator=EQ" \
    + "&pQueryLimit=" \
    + "&pJWThreshold=90" \
    + "&pResolution=3" \
    + "&pSourceTable=" \
    + "&pState=" + State \
    + "&pStateMod=%2C" \
    + "&pCountyFips5=" \
    + "&pCountyFips5Mod=%2C" \
    + "&pSubbasin=" \
    + "&pSubbasinMod=%2C" \
    + "&pGnisClass=" \
    + "&pGnisClassMod=%2C" \
    + "&pFtype=" \
    + "&pBreakBySubbasin=false" \
    + "&pBreakByFcode=false" \
    + "&optNHDPlusDataset=2.1" \
    + "&optCache=1415283785917" \
    + "&optJSONPCallback=" \

#load response into JSON object
response = json.loads(urllib2.urlopen(url).read())

#uncomment to see structure of response
#pprint(response)

#get lat and lon coordinates of centroid
print "%s result(s) found"%(len(response['output']['results']))

#there may be multiple responses if it is a common stream/river/waterbody name
for i in range(0, len(response['output']['results'])):
    coords = response['output']['results'][i]['gnis_centroid_geom']['coordinates']
    lon = coords[0]
    lat = coords[1]
    print "Pt %s: The centroid point is %s, %s"%(i, lat,lon)