from google.oauth2.credentials import Credentials as GoogleCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path


class GoogleAPI:
    def __init__(self, credentials):
        self.credentials = credentials


def load_google_credentials(user_credentials_path, api_credentials_path, scope):
    # Check if there are stored user credentials
    if os.path.exists(user_credentials_path):
        creds = GoogleCredentials.from_authorized_user_file(user_credentials_path, scope)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save the credentials for the next run
            with open(user_credentials_path, 'w') as token:
                token.write(creds.to_json())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(api_credentials_path, scope)
        creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(user_credentials_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def example():
    scopes = ['https://www.googleapis.com/auth/calendar.readonly',
              'https://www.googleapis.com/auth/spreadsheets.readonly']
    user_google_credentials_path = '../Credentials/google_user_token.json'
    google_credentials_path = '../Credentials/google_client.json'
    credentials = load_google_credentials(user_google_credentials_path, google_credentials_path, scopes)

    google_api = GoogleAPI(credentials)
    print(google_api.credentials)


if __name__ == '__main__':
    example()
