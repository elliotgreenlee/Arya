import requests
from API_Helpers.Kroger.kroger_utils import KrogerAPI
import json


class KrogerLocationsAPI(KrogerAPI):
    def __init__(self, user_credentials_path, api_credentials_path, scope):
        super().__init__(user_credentials_path, api_credentials_path, scope)

    def search_locations(self, zip_code, limit=5):
        locations_url = "https://api.kroger.com/v1/locations"
        headers = {
            "Authorization": f"Bearer {self.credentials.token}",
            "Accept": "application/json",
        }
        params = {
            "filter.zipCode.near": zip_code,
            "filter.limit": limit,
        }
        try:
            response = requests.get(locations_url, headers=headers, params=params)
            response.raise_for_status()
            locations = response.json()
            return locations.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


def example():
    scope = "profile.compact product.compact cart.basic:write"
    user_kroger_credentials_path = '../../Credentials/kroger_user_token.json'
    kroger_credentials_path = '../../Credentials/kroger_client.json'
    kroger_locations_api = KrogerLocationsAPI(user_kroger_credentials_path, kroger_credentials_path, scope)

    user_zip_code = "97215"
    locations = kroger_locations_api.search_locations(user_zip_code)
    for location in locations:
        print(json.dumps(location, indent=4))


if __name__ == '__main__':
    example()
