import os
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MBTA_API_KEY")



def get_routes():
    url = 'https://api-v3.mbta.com/routes'
    headers = {"x-api-key" : api_key}
    params = {"filter[type]" : "1"}
    r = requests.get(url,headers=headers,params=params)
    data = r.json()
    info = []
    r.raise_for_status()
    for i in data['data']:
        route_id = i['id']
        long_name = i['attributes']['long_name']
        direction_name = i['attributes']['direction_names']
        j = {"route_id" : route_id, "long_name" : long_name, "direction_names" : direction_name}
        info.append(j)
    return info
# if i wanna get scheduled times instead of predicitions use /schedules
def get_predictions(route_id):
    url ='https://api-v3.mbta.com/predictions'
    headers = {"x-api-key" : api_key}
    params = {"filter[route]" : route_id}
    r = requests.get(url,headers=headers,params=params)
    r.raise_for_status()
    data = r.json()
    info = []
    for i in data['data']:
        prediction_id = i['id']
        stop_id = i['relationships']['stop']['data']['id']
        trip_id = i['relationships']['trip']['data']['id']
        direction_id = i['attributes']['direction_id']
        arrival_time = i['attributes']['arrival_time']
        departure_time = i['attributes']['departure_time']
        status = i['attributes']['status']
        j = {'prediction_id' : prediction_id, 'route_id' : route_id, 'stop_id': stop_id, 'trip_id' : trip_id, 'direction_id' : direction_id, 'arrival_time' : arrival_time, 'departure_time' : departure_time, 'status' : status}
        info.append(j)
    return info