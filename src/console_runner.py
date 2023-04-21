import urllib

import requests
from geopy.geocoders import Nominatim

TFL_STOP_POINT_URL = "https://api.tfl.gov.uk/StopPoint?"
TFL_STOP_POINT_STATIC_PARAMS = {
    'stopTypes': 'NaptanPublicBusCoachTram',
    'radius': '1000',
    'app_id': '',
    'app_key': ''
}


def _prompt_for_postcode():
    postcode = input('\nEnter your postcode: ')
    return postcode


def _display_stop_points(stop_points):
    for point in stop_points:
        print(point['commonName'])


def _get_nearest_stop_points(parameters):
    request_url = (
            TFL_STOP_POINT_URL +
            urllib.parse.urlencode(
                TFL_STOP_POINT_STATIC_PARAMS | parameters
            )
    )
    response = requests.get(request_url)
    if response.status_code != 200:
        raise Exception(f'Request failed with status code {response.status_code}')
    return response.json()


def _get_location_for_postcode(postcode):
    geolocator = Nominatim(user_agent='console-runner')
    location = geolocator.geocode(postcode)
    if not location:
        raise Exception('Could not retrieve location')
    return {
        'lat': location.latitude,
        'lon': location.longitude,
    }


def _parse_nearest_stop_response(response_json, count):
    stop_points = response_json['stopPoints']
    return [{'naptanId': point['naptanId'], 'commonName': point['commonName']} for point in stop_points[:count]]


def run():
    nearest_stops = []
    try:
        user_inputted_postcode = _prompt_for_postcode()
        location = _get_location_for_postcode(user_inputted_postcode)
        nearest_stops = _parse_nearest_stop_response(
            _get_nearest_stop_points(location),
            count=5,
        )
    except Exception as e:
        print(f"Error while parsing response: {e}")
    _display_stop_points(nearest_stops)
