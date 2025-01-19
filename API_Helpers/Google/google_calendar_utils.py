from googleapiclient.discovery import build
from .google_utils import GoogleAPI
from datetime import datetime, timedelta


class GoogleCalendarAPI(GoogleAPI):
    def __init__(self, user_credentials_path, client_credentials_path, scope):
        super().__init__(user_credentials_path, client_credentials_path, scope)

        self.calendar = build('calendar', 'v3', credentials=self.credentials)

    def calendar_events(self, time_min, time_max):
        events_result = self.calendar.events().list(
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

    def upcoming_days(self, days):
        print(f"In the next {days} day(s) you will have these events:")
        now = datetime.utcnow()
        time_min = now.isoformat() + 'Z'  # 'Z' indicates UTC time
        time_max = (now + timedelta(days=days)).isoformat() + 'Z'
        self.calendar_events(time_min, time_max)

    def past_days(self, days):
        print(f"In the last {days} day(s) you had these events:")
        now = datetime.utcnow()
        time_min = (now - timedelta(days=days)).isoformat() + 'Z'
        time_max = now.isoformat() + 'Z'  # 'Z' indicates UTC time
        self.calendar_events(time_min, time_max)


def example():
    scope = ['https://www.googleapis.com/auth/calendar.readonly']
    user_google_calendar_credentials_path = '../../Credentials/google_calendar_user_token.json'
    google_credentials_path = '../../Credentials/google_client.json'
    google_calendar_api = GoogleCalendarAPI(user_google_calendar_credentials_path, google_credentials_path, scope)

    google_calendar_api.past_days(7)
    google_calendar_api.upcoming_days(7)


if __name__ == '__main__':
    example()
