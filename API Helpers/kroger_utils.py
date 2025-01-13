import requests
import os.path
from KrogerCredentials import KrogerCredentials
from KrogerFlow import InstalledAppFlow


class KrogerAPI:
    def __init__(self, credentials):
        self.credentials = credentials


def load_kroger_credentials(user_credentials_path, api_credentials_path, scopes):
    # Check if there are stored user credentials
    if os.path.exists(user_credentials_path):
        creds = KrogerCredentials.from_authorized_user_file(user_credentials_path, scopes)

        if creds and creds.expired and creds.refresh_token:
            # TODO: pass something in here and implement
            creds.refresh(Request())
            # Save the credentials for the next run
            with open(user_credentials_path, 'w') as token:
                token.write(creds.to_json())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(api_credentials_path, scopes)
        creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(user_credentials_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def example():
    # TODO: show how to put multiple scopes together instead of dict once figured out
    scopes = {
        "cart_scope": '',
        "locations_scope": '',
        "products_scope": '',
        "profile_scope": ''
    }
    user_kroger_credentials_path = '../Credentials/kroger_user_token.json'
    kroger_credentials_path = '../Credentials/kroger_client.json'
    credentials = load_kroger_credentials(user_kroger_credentials_path, kroger_credentials_path, scopes)

    kroger_api = KrogerAPI(credentials)
    print(kroger_api.credentials)


if __name__ == '__main__':
    example()
