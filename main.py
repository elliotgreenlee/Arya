
import os.path
import requests
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes define the level of access your application requires
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def calendar_events(calendar_service, time_min, time_max):
    print(f"Getting events from {time_min} to {time_max}")
    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    else:
        for event in events:
            # Extract details
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            location = event.get('location', 'No location specified')
            description = event.get('description', 'No description available')
            summary = event.get('summary', 'No title')

            # Calculate event length (if start and end are dateTime)
            if 'dateTime' in event['start'] and 'dateTime' in event['end']:
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
                duration = end_dt - start_dt
            else:
                duration = 'All day event'

            # Print details
            print(f"Title: {summary}")
            print(f"Start: {start}")
            print(f"Duration: {duration}")
            print(f"Location: {location}")
            print(f"Description: {description}")
            print("-" * 40)


def last_week_calendar(calendar_service):
    print(f"Last week you had these events:")
    now = datetime.utcnow()
    time_min = (now - timedelta(weeks=1)).isoformat() + 'Z'
    time_max = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    calendar_events(calendar_service, time_min, time_max)


def next_two_weeks_calendar(calendar_service):
    print(f"In the next two weeks you will have these events:")
    now = datetime.utcnow()
    time_min = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    time_max = (now + timedelta(weeks=2)).isoformat() + 'Z'
    calendar_events(calendar_service, time_min, time_max)


def connect_to_google_calendar():
    token_path = 'Credentials/token.json'
    credentials_path = 'Credentials/client_secret.apps.googleusercontent.com.json'

    # Check if Credentials/token.json exists for stored credentials
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no valid credentials, prompt for login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Initialize the Calendar API
    google_calendar = build('calendar', 'v3', credentials=creds)
    return google_calendar


def load_api_key(file_path):
    """
    Loads the OpenWeather API key from a JSON file.

    Parameters:
    - file_path (str): Path to the JSON file containing the API key.

    Returns:
    - str: The API key.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['api_key']


def next_eight_days_weather(api_key, lat, lon):
    """
    Fetches daily weather forecasts from OpenWeather for a given time range.

    Parameters:
    - api_key (str): Your OpenWeather API key.
    - lat (float): Latitude of the location.
    - lon (float): Longitude of the location.

    Returns:
    - List of dictionaries containing weather data for each day
    """
    # OpenWeather One Call API endpoint
    url = f"https://api.openweathermap.org/data/3.0/onecall"

    # Fetch weather data
    response = requests.get(url, params={
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,hourly',  # Focus on daily data
        'units': 'imperial',  # temperature in Fahrenheit and wind speed in miles/hour
        'appid': api_key
    })
    response.raise_for_status()  # Raise an error if the request fails
    data = response.json()

    # Filter daily data for the specified time range
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


def main():
    calendar_service = connect_to_google_calendar()
    last_week_calendar(calendar_service)
    next_two_weeks_calendar(calendar_service)

    # Example: Portland, OR
    portland_latitude = 45.5152
    portland_longitude = -122.6784
    openweather_api_key = load_api_key('Credentials/openweather_api_key.json')
    # Commented out so I don't use up 1000 call quota
    # next_eight_days_weather(openweather_api_key, portland_latitude, portland_longitude)


if __name__ == '__main__':
    main()
