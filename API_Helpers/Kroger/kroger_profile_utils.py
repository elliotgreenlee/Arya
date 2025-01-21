from API_Helpers.Kroger.kroger_utils import KrogerAPI
import requests
import json


class KrogerProfileAPI(KrogerAPI):
    def __init__(self, user_credentials_path, api_credentials_path, scope):
        super().__init__(user_credentials_path, api_credentials_path, scope)

    def get_customer_profile(self):
        api_url = "https://api.kroger.com/v1/identity/profile"
        headers = {
            "Authorization": f"Bearer {self.credentials.token}",
            "Accept": "application/json",
        }

        try:
            response = requests.get(api_url, headers=headers)
            profile = response.json()
            return profile.get('data', {})
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


def example():
    scope = "profile.compact product.compact cart.basic:write"
    user_kroger_credentials_path = '../../Credentials/kroger_user_token.json'
    kroger_credentials_path = '../../Credentials/kroger_client.json'
    kroger_profile_api = KrogerProfileAPI(user_kroger_credentials_path, kroger_credentials_path, scope)

    profile = kroger_profile_api.get_customer_profile()
    print(json.dumps(profile, indent=4))


if __name__ == '__main__':
    example()
