import requests
from kroger_utils import Kroger
from Utils.utils import load_json


def search_locations(kroger, zip_code, limit=5):
    locations_url = "https://api.kroger.com/v1/locations"
    headers = {
        "Authorization": f"Bearer {kroger.token}",
        "Accept": "application/json",
    }
    params = {
        "filter.zipCode.near": zip_code,
        "filter.limit": limit,
    }
    try:
        response = requests.get(locations_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def example():
    user_zip_code = "97215"

    kroger_credentials_path = '../Credentials/kroger_client.json'
    credentials = load_json(kroger_credentials_path)

    kroger = Kroger(credentials['client_id'], credentials['client_secret'], credentials['locations_scope'])

    locations = search_locations(kroger, user_zip_code)

    for location in locations.get("data", []):
        print(f"Store Name: {location['name']}")
        print(f"Location ID: {location['locationId']}")
        print(
            f"Address: {location['address']['addressLine1']}, {location['address']['city']}, {location['address']['state']}")
        print()


if __name__ == '__main__':
    example()
