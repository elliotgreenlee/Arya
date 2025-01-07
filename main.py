
import os.path
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from openai import OpenAI

# Scopes define the level of access your application requires
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/spreadsheets.readonly']

API_KEYS_PATH = 'Credentials/api_keys.json'

ELLIOT_GOOGLE_CREDENTIALS_PATH = 'Credentials/elliot_google_user_token.json'
CLIENT_GOOGLE_CREDENTIALS_PATH = 'Credentials/google_client.json'

# Portland, OR
USER_LATITUDE = 45.5152
USER_LONGITUDE = -122.6784


def load_google_credentials(user_credentials_path, api_credentials_path):
    # Check if there are stored user credentials
    creds = None
    if os.path.exists(user_credentials_path):
        creds = Credentials.from_authorized_user_file(user_credentials_path, SCOPES)

    # If there are no valid credentials, prompt for login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(api_credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(user_credentials_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def connect_to_google_calendar(credentials):
    # Initialize the Calendar API
    google_calendar = build('calendar', 'v3', credentials=credentials)
    return google_calendar


def connect_to_google_sheets(credentials):
    # Initialize the Sheets API
    google_sheets = build('sheets', 'v4', credentials=credentials)
    return google_sheets


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


def load_api_keys(file_path):
    with open(file_path, 'r') as file:
        api_keys = json.load(file)
        return api_keys


def next_eight_days_weather(api_key, lat, lon):
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


def load_google_sheet_to_dataframe(sheets_service, spreadsheet_id, spreadsheet_range, column_types=None):
    sheet = sheets_service.spreadsheets()

    # Read data from the specified range
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=spreadsheet_range).execute()
    values = result.get('values', [])

    # If no data, return an empty DataFrame
    if not values:
        return pd.DataFrame()

    # Create a DataFrame
    df = pd.DataFrame(values[1:], columns=values[0])  # Use the first row as column names

    # Apply column types if specified
    if column_types:
        for column, dtype in column_types.items():
            if column in df.columns:
                df[column] = df[column].astype(dtype)

    return df


def last_week_workout(sheets_service):
    # https://docs.google.com/spreadsheets/d/<spreadsheet_id>/edit
    training_spreadsheet_id = '1JFpTX7CfaQ-GYvUSiq6dA397tgVxM1v3x_s2vA_UIeQ'
    training_spreadsheet_range = 'Weekly Training!A1:X25'
    training_column_types = {
        'Week': str,
        'Week Start': str,
        'Day 1': str,
        'Day 1 Data': str,
        'Day 2': str,
        'Day 2 Data': str,
        'Day 3': str,
        'Day 3 Data': str,
        'Day 4': str,
        'Day 4 Data': str,
        'Day 5': str,
        'Day 5 Data': str,
        'Day 6': str,
        'Day 6 Data': str,
        'Day 7': str,
        'Day 7 Data': str,
        'Run Distance': str,
        'Bike Distance': str,
        'Swim Distance': str,
        'Total Distance': str,
        'Total Time': str,
        'Running Goal': str,
        'Biking Goal': str,
        'Swimming Goal': str
    }

    # Load data into a Pandas DataFrame
    df = load_google_sheet_to_dataframe(sheets_service, training_spreadsheet_id,
                                        training_spreadsheet_range,
                                        column_types=training_column_types)

    df['Week Start'] = pd.to_datetime(df['Week Start'], format="%Y/%m/%d")

    # Get today's date in PST
    today_pst = pd.Timestamp(datetime.now())
    start_date = today_pst - timedelta(days=13)
    end_date = today_pst - timedelta(days=6)

    last_week = df[(df['Week Start'] >= start_date) &
                   (df['Week Start'] <= end_date)]

    pd.set_option('display.max_columns', None)  # Show all columns
    display_columns = ['Week', 'Week Start', 'Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']

    if not last_week.empty:
        print(last_week[display_columns])
    else:
        print("No exercise plan for last week.")


def next_week_workout(sheets_service):
    # https://docs.google.com/spreadsheets/d/<spreadsheet_id>/edit
    training_spreadsheet_id = '1JFpTX7CfaQ-GYvUSiq6dA397tgVxM1v3x_s2vA_UIeQ'
    training_spreadsheet_range = 'Weekly Training!A1:X25'
    training_column_types = {
        'Week': str,
        'Week Start': str,
        'Day 1': str,
        'Day 1 Data': str,
        'Day 2': str,
        'Day 2 Data': str,
        'Day 3': str,
        'Day 3 Data': str,
        'Day 4': str,
        'Day 4 Data': str,
        'Day 5': str,
        'Day 5 Data': str,
        'Day 6': str,
        'Day 6 Data': str,
        'Day 7': str,
        'Day 7 Data': str,
        'Run Distance': str,
        'Bike Distance': str,
        'Swim Distance': str,
        'Total Distance': str,
        'Total Time': str,
        'Running Goal': str,
        'Biking Goal': str,
        'Swimming Goal': str
    }

    # Load data into a Pandas DataFrame
    df = load_google_sheet_to_dataframe(sheets_service, training_spreadsheet_id,
                                        training_spreadsheet_range,
                                        column_types=training_column_types)

    df['Week Start'] = pd.to_datetime(df['Week Start'], format="%Y/%m/%d")

    # Get today's date in PST
    today_pst = pd.Timestamp(datetime.now())

    next_week = df[(df['Week Start'] >= today_pst - timedelta(days=6))
                   & (df['Week Start'] <= today_pst + timedelta(days=1))]

    pd.set_option('display.max_columns', None)  # Show all columns
    display_columns = ['Week', 'Week Start', 'Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
    if not next_week.empty:
        print(next_week[display_columns])
    else:
        print("No exercise plan for next week.")


def main():
    api_keys = load_api_keys(API_KEYS_PATH)

    google_credentials = load_google_credentials(
        ELLIOT_GOOGLE_CREDENTIALS_PATH,
        CLIENT_GOOGLE_CREDENTIALS_PATH)

    '''
    # Calendar data
    calendar_service = connect_to_google_calendar(google_credentials)
    last_week_calendar(calendar_service)
    next_two_weeks_calendar(calendar_service)

    # Weather data
    next_eight_days_weather(api_keys['openweather_api_key'], USER_LATITUDE, USER_LONGITUDE)

    # Sheets data
    sheets_service = connect_to_google_sheets(google_credentials)
    last_week_workout(sheets_service)
    next_week_workout(sheets_service)
    '''

    # OpenAI

    client = OpenAI(api_key=api_keys['openai_api_key'])
    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ]
    )

    print(completion)


if __name__ == '__main__':
    main()
