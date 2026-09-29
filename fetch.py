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
    pulled_at = datetime.now(timezone.utc).isoformat()
    r.raise_for_status()
    for i in data['data']:
        route_id = i['id']
        long_name = i['attributes']['long_name']
        direction_name = i['attributes']['direction_names']
        j = {"route_id" : route_id, "long_name" : long_name, "direction_names" : direction_name, "pulled_at" : pulled_at}
        info.append(j)
    return info

def get_schedules(route_id):
    url = 'https://api-v3.mbta.com/schedules'
    headers = {'x-api-key' : api_key}
    params = {'filter[route]' : route_id}
    r = requests.get(url,headers=headers,params=params)
    r.raise_for_status()
    data = r.json()
    info = []
    for i in data['data']:
        arrival_time = i['attributes']['arrival_time']
        departure_time = i['attributes']['departure_time']
        direction_id = i['attributes']['direction_id']
        stop_id = i['relationships']['stop']['data']['id']
        trip_id = i['relationships']['trip']['data']['id']
        schedule_id = i['id']
        stop_sequence = i['attributes']['stop_sequence']
        j = {'route_id' : route_id, 'arrival_time' : arrival_time, 'departure_time' : departure_time, 'direction_id' : direction_id, 'stop_id' : stop_id, 'trip_id' : trip_id, 'schedule_id' : schedule_id, 'stop_sequence' : stop_sequence}
        info.append(j)
    return info
    

def get_predictions(route_id):
    url ='https://api-v3.mbta.com/predictions'
    headers = {"x-api-key" : api_key}
    params = {"filter[route]" : route_id}
    r = requests.get(url,headers=headers,params=params)
    r.raise_for_status()
    data = r.json()
    info = []
    pulled_at = datetime.now(timezone.utc).isoformat()
    for i in data['data']:
        prediction_id = i['id']
        stop_id = i['relationships']['stop']['data']['id']
        trip_id = i['relationships']['trip']['data']['id']
        direction_id = i['attributes']['direction_id']
        arrival_time = i['attributes']['arrival_time']
        departure_time = i['attributes']['departure_time']
        status = i['attributes']['status']
        j = {'prediction_id' : prediction_id, 'route_id' : route_id, 'stop_id': stop_id, 'trip_id' : trip_id, 'direction_id' : direction_id, 'arrival_time' : arrival_time, 'departure_time' : departure_time, 'status' : status, 'pulled_at' : pulled_at}
        info.append(j)
    return info



