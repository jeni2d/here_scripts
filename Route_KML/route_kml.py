# this script can extract geometry and save it as KML file from the route built on https://refclient.ext.here.com/
# the only input is copied api call

import requests
import re
import simplekml

kml=simplekml.Kml()

api_url = "https://route.api.here.com/routing/7.2/calculateroute.json"
params = {
	'mode': 'fastest;car;traffic:disabled',
	'app_id': '', #get app_id and app_code on https://developer.here.com/
        'app_code': '',
	'departure': 'now',
	'routeattributes': ['sm', 'sh'],
	'linkattributes': ['sh', 'le'],
	'legattributes': 'li'
}
input_link = input()
points = [i.replace('!', '').replace('%2C', ',') for i in re.findall('!\d\d\.\d+%\w+\.\d+', input_link )]

coords = []

for index, i in enumerate(points):
	if 0 < index < len(points)-1:
		params['waypoint'+str(index)] = 'geo!passThrough!'+i
	else:
		params['waypoint'+str(index)] = i

res = requests.get(api_url, params=params)
length = res.json()['response']['route'][0]['summary']['distance']
links = []
for i in res.json()['response']['route'][0]['shape']:
	q = i.split(',')
	q1 = (q[1], q[0])
	coords.append(q1)	

name_file = '' 
kml.newlinestring(name=str(length), coords=coords)
kml.save('path_to_output_file/{}.kml'.format(name_file))
