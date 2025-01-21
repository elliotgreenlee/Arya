import os.path
from .KrogerCredentials import KrogerCredentials
from API_Helpers.Kroger.KrogerFlow import InstalledAppFlow


class KrogerAPI:
    def __init__(self, user_credentials_path, api_credentials_path, scope):
        self.user_credentials_path = user_credentials_path
        self.api_credentials_path = api_credentials_path
        self.scope = scope
        self.credentials = self.load_credentials()

    def load_credentials(self):
        # Check if there are stored user credentials
        if os.path.exists(self.user_credentials_path):
            creds = KrogerCredentials.from_authorized_user_file(self.user_credentials_path, self.scope)

            if creds and creds.expired and creds.refresh_token:
                creds.refresh()
                # Save the credentials for the next run
                with open(self.user_credentials_path, 'w') as token:
                    token.write(creds.to_json())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(self.api_credentials_path, self.scope)
            creds = flow.run_local_server()
            # Save the credentials for the next run
            with open(self.user_credentials_path, 'w') as token:
                token.write(creds.to_json())

        return creds


def example():
    scope = "profile.compact product.compact cart.basic:write"

    user_kroger_credentials_path = '../../Credentials/kroger_user_token.json'
    kroger_credentials_path = '../../Credentials/kroger_client.json'

    kroger_api = KrogerAPI(user_kroger_credentials_path, kroger_credentials_path, scope)
    print(kroger_api.credentials)


if __name__ == '__main__':
    example()
