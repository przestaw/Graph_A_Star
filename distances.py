import math
import requests
import json

def haversine(start, stop):
	r = 6371
	lat0, lon0 = start
	lat1, lon1 = stop

	dlon = math.radians(lon1-lon0)
	dlat = math.radians(lat1-lat0)
	x = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat0)) * math.cos(math.radians(lat1)) * math.sin(dlon/2) * math.sin(dlon/2)
	y = 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))
	z = r * y
	return z

def road_distance(start, stop):
	lat0, lon0 = start
	lat1, lon1 = stop
	
	route_url ='https://fleet.api.here.com/2/calculateroute.json?mapMatchRadius=2000&ignoreWaypointVehicleRestriction=1000&waypoint0='+str(lat0)+'%2C'+str(lon0)+'&waypoint1='+str(lat1)+'%2C'+str(lon1)+'&mode=fastest%3Bcar%3Btraffic%3Adisabled&app_id=mCHjQRZFnmZcxTtunxeQ&app_code=QGzrNESMJOVlccW3gRrM2g&departure=now&routeattributes=sm'
	req = requests.get(route_url)
	#jesli fleet api skiśnie
	try:
		ret = req.json()['response']['route'][0]['summary']['distance']/1000
	except TypeError:
		ret = haversine(start, stop)
	return ret;





