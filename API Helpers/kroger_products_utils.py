from kroger_utils import Kroger
import requests
from Utils.utils import load_json


def search_products(kroger, search_term, limit=5):
    api_url = "https://api.kroger.com/v1/products"
    headers = {
        "Authorization": f"Bearer {kroger.token}",
        "Accept": "application/json",
    }
    params = {
        "filter.term": search_term,
        "filter.limit": limit,
    }

    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        products = response.json()
        print("Products API Response:", products)
        return products
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def example():
    kroger_credentials_path = '../Credentials/kroger_client.json'
    credentials = load_json(kroger_credentials_path)

    kroger = Kroger(credentials['client_id'], credentials['client_secret'], credentials['products_scope'])
    search_products(kroger, 'milk')


if __name__ == '__main__':
    example()
