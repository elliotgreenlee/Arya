from google.oauth2.credentials import Credentials as GoogleCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path


class GoogleAPI:
    def __init__(self, user_credentials_path, api_credentials_path, scope):
        self.user_credentials_path = user_credentials_path
        self.api_credentials_path = api_credentials_path
        self.scope = scope
        self.credentials = self.load_credentials()

    def load_credentials(self):
        # Check if there are stored user credentials
        if os.path.exists(self.user_credentials_path):
            creds = GoogleCredentials.from_authorized_user_file(self.user_credentials_path, self.scope)

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                # Save the credentials for the next run
                with open(self.user_credentials_path, 'w') as token:
                    token.write(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(self.api_credentials_path, self.scope)
            creds = flow.run_local_server(port=8082)
            # Save the credentials for the next run
            with open(self.user_credentials_path, 'w') as token:
                token.write(creds.to_json())

        return creds


def example():
    scope = ['https://www.googleapis.com/auth/calendar.readonly',
             'https://www.googleapis.com/auth/spreadsheets.readonly']
    user_google_credentials_path = '../../Credentials/google_user_token.json'
    google_credentials_path = '../../Credentials/google_client.json'

    google_api = GoogleAPI(user_google_credentials_path, google_credentials_path, scope)
    print(google_api.credentials)


if __name__ == '__main__':
    example()
