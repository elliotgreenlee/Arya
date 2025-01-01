import datetime
import os.path
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
                start_dt = datetime.datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.datetime.fromisoformat(end.replace('Z', '+00:00'))
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
    now = datetime.datetime.utcnow()
    time_min = (now - datetime.timedelta(weeks=1)).isoformat() + 'Z'
    time_max = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    calendar_events(calendar_service, time_min, time_max)


def next_two_weeks_calendar(calendar_service):
    print(f"In the next two weeks you will have these events:")
    now = datetime.datetime.utcnow()
    time_min = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    time_max = (now + datetime.timedelta(weeks=2)).isoformat() + 'Z'
    calendar_events(calendar_service, time_min, time_max)


def main():
    creds = None
    # Check if Credentials/token.json exists for stored credentials
    token_path = 'Credentials/token.json'
    credentials_path = 'Credentials/client_secret.apps.googleusercontent.com.json'

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
    service = build('calendar', 'v3', credentials=creds)

    last_week_calendar(service)
    next_two_weeks_calendar(service)


if __name__ == '__main__':
    main()

