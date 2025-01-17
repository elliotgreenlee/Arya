from Utils.utils import load_json
import requests
import json


class OpenweatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def next_eight_days(self, lat, lon):
        endpoint = f"https://api.openweathermap.org/data/3.0/onecall"
        params = {
            'lat': lat,
            'lon': lon,
            'exclude': 'minutely,hourly',  # Focus on daily data
            'units': 'imperial',  # temperature in Fahrenheit and wind speed in miles/hour
            'appid': self.api_key
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('daily', [])


def example():
    openweather_credentials_path = '../Credentials/api_keys.json'
    api_keys = load_json(openweather_credentials_path)

    user_latitude = 45.5152
    user_longitude = -122.6784
    openweather = OpenweatherAPI(api_keys['openweather_api_key'])
    daily_data = openweather.next_eight_days(user_latitude, user_longitude)

    for day in daily_data:
        print(json.dumps(day, indent=4))


if __name__ == '__main__':
    example()
