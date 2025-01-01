import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes define the level of access your application requires
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    creds = None
    # Check if token.json exists for stored credentials
    if os.path.exists('Credentials/token.json'):
        creds = Credentials.from_authorized_user_file('Credentials/token.json', SCOPES)

    # If there are no valid credentials, prompt for login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Credentials/client_secret.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('Credentials/token.json', 'w') as token:
            token.write(creds.to_json())

    # Initialize the Calendar API
    service = build('calendar', 'v3', credentials=creds)

    # Get the next 10 events from the user's calendar
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
