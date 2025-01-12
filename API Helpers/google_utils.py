from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path


class GoogleAPI:
    def __init__(self, credentials):
        self.credentials = credentials


def load_google_credentials(user_credentials_path, api_credentials_path, scope):
    creds = None
    # Check if there are stored user credentials
    if os.path.exists(user_credentials_path):
        creds = Credentials.from_authorized_user_file(user_credentials_path, scope)

    # If there are no valid credentials, prompt for login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(api_credentials_path, scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(user_credentials_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def example():
    scope = ['https://www.googleapis.com/auth/calendar.readonly',
             'https://www.googleapis.com/auth/spreadsheets.readonly']
    user_google_credentials_path = '../Credentials/google_user_token.json'
    google_credentials_path = '../Credentials/google_client.json'
    credentials = load_google_credentials(user_google_credentials_path, google_credentials_path, scope)

    google_api = GoogleAPI(credentials)
    print(google_api.credentials)


if __name__ == '__main__':
    example()
