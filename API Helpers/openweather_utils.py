from Utils.utils import load_json
import requests
from datetime import datetime


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

        daily_data = []
        for day in data.get('daily', []):
            date = datetime.fromtimestamp(day['dt'])
            daily_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'morning_temp': day['temp']['morn'],
                'daytime_temp': day['temp']['day'],
                'evening_temp': day['temp']['eve'],
                'night_temp': day['temp']['night'],
                'morning_human_temp': day['feels_like']['morn'],
                'daytime_human_temp': day['feels_like']['day'],
                'evening_human_temp': day['feels_like']['eve'],
                'night_human_temp': day['feels_like']['night'],
                'weather': day['weather'][0]['description'],  # Weather description
                'summary': day['summary'],  # Weather description, kinda bad
                'humidity': day['humidity'],  # Humidity percentage
                'dew_point': day['dew_point'],  # Dew point temperature
                'uv_index': day['uvi'],  # UV index
                'precipitation_prob': day['pop'],  # chance of precipitation 0-1
                'wind_speed': day['wind_speed'],  # Wind speed
                'wind_gust': day['wind_gust'],  # Wind gust
                'sunrise': day['sunrise'],  # Sunrise unix timestamp in UTC
                'sunset': day['sunset'],  # Sunset unix timestamp in UTC
            })

        for day in daily_data:
            print(f"Day: {day}")
            print("-------------")


def example():
    openweather_credentials_path = '../Credentials/api_keys.json'
    api_keys = load_json(openweather_credentials_path)

    user_latitude = 45.5152
    user_longitude = -122.6784
    openweather = OpenweatherAPI(api_keys['openweather_api_key'])
    openweather.next_eight_days(user_latitude, user_longitude)


if __name__ == '__main__':
    example()
