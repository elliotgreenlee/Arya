import requests
from Utils.utils import load_json


class Kroger:
    def __init__(self, client_id, client_secret, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.token = None
        self.get_access_token()

    def get_access_token(self):
        auth_url = "https://api.kroger.com/v1/connect/oauth2/token"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
            "scope": self.scope,
        }
        try:
            response = requests.post(auth_url, headers=headers, data=data, auth=(self.client_id, self.client_secret))
            response.raise_for_status()
            self.token = response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


def example():
    kroger_credentials_path = '../Credentials/kroger_client.json'
    credentials = load_json(kroger_credentials_path)
    empty_scope = ""

    kroger = Kroger(credentials['client_id'], credentials['client_secret'], empty_scope)
    print(kroger.token)

    # TODO: test each scope individually to confirm they work
    # TODO: test combining scopes into a single oauth request. chatgpt and the kroger documentation suggest
    #  I can combine them as space separated items in a string, but it doesnt seem to work


if __name__ == '__main__':
    example()
