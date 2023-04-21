import requests
from geopy.geocoders import Nominatim

class ConsoleRunner:
    def prompt_for_postcode(self):
        print('here')
        postcode = input('\nEnter your postcode: ')
        return postcode

    def display_stop_points(self, stop_points):
        for point in stop_points:
            print(point['commonName'])

    def make_get_request(self, parameters):
        response = requests.get(f"https://api.tfl.gov.uk/StopPoint?stopTypes=NaptanPublicBusCoachTram&lat={parameters[0]}&lon={parameters[1]}&radius=1000&app_id=&app_key=")
        if response.status_code != 200:
            raise Exception(f'Request failed with status code {response.status_code}')
        return response.json()

    def get_location_for_postcode(self, postcode):
        geolocator = Nominatim(user_agent='console-runner')
        location = geolocator.geocode(postcode)
        if not location:
            raise Exception('Could not retrieve location')
        return {
            'latitude': location.latitude,
            'longitude': location.longitude,
        }

    def get_nearest_stop_points(self, latitude, longitude):
        parameters = [latitude, longitude]
        return self.make_get_request( parameters)

    def parse_nearest_stop_response(self, response_json, count):
        stop_points = response_json['stopPoints']
        return [{'naptanId': point['naptanId'], 'commonName': point['commonName']} for point in stop_points[:count]]

    def run(self):
        nearest_stops = []
        try:
            user_inputted_postcode = self.prompt_for_postcode()
            location = self.get_location_for_postcode(user_inputted_postcode)
            nearest_stops = self.parse_nearest_stop_response(
                self.get_nearest_stop_points(location['latitude'], location['longitude']),
                count=5,
            )
        except Exception as e:
            print(f"Error while parsing response: {e}")
        self.display_stop_points(nearest_stops)

def main():
    console_runner = ConsoleRunner()
    console_runner.run()