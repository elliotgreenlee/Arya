from kroger_utils import Kroger
from Utils.utils import load_json
import requests
import base64


def get_customer_profile(kroger):
    api_url = "https://api.kroger.com/v1/connect/profile"
    headers = {
        "Authorization": f"Bearer {kroger.token}",
        "Accept": "application/json",
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        profile = response.json()
        print("Profile API Response:", profile)
        return profile
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def example():
    kroger_credentials_path = '../Credentials/kroger_client.json'
    credentials = load_json(kroger_credentials_path)

    '''
    kroger = Kroger(credentials['client_id'], credentials['client_secret'], credentials['profile_scope'])
    profile = get_customer_profile(kroger)
    if profile:
        customer_id = profile.get("data", {}).get("id", None)
        print(f"Customer ID: {customer_id}")
    '''

    redirect_uri = 'www.google.com'
    authorization_code = 'your_authorization_code'

    # Encode client credentials
    credentials = f"{credentials['client_id']}:{credentials['client_secret']}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # Step 2: Obtain an OAuth2 access token
    token_url = 'https://api.kroger.com/v1/connect/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_credentials}',
    }
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
    }
    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f"Error obtaining access token: {response.text}")

    access_token = response.json().get('access_token')

    # Step 3: Fetch the customer's profile ID
    profile_url = 'https://api.kroger.com/v1/identity/profile'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(profile_url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching profile: {response.text}")

    profile_data = response.json()
    profile_id = profile_data.get('data', {}).get('id')

    print(f"Customer Profile ID: {profile_id}")


if __name__ == '__main__':
    example()
