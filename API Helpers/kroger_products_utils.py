from kroger_utils import KrogerAPI
import requests
from kroger_utils import load_kroger_credentials


class KrogerProductsAPI(KrogerAPI):
    def __init__(self, credentials):
        super().__init__(credentials)

    def search_products(self, location_id, search_term, limit=5):
        api_url = "https://api.kroger.com/v1/products"
        headers = {
            "Authorization": f"Bearer {self.credentials.token}",
            "Accept": "application/json",
        }
        params = {
            "filter.term": search_term,
            "filter.locationId": location_id,
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

    scopes = {
        "cart_scope": "",
        "locations_scope": "",
        "products_scope": "product.compact",
        "profile_scope": "",
    }
    user_kroger_credentials_path = '../Credentials/kroger_user_token.json'
    kroger_credentials_path = '../Credentials/kroger_client.json'
    credentials = load_kroger_credentials(user_kroger_credentials_path, kroger_credentials_path, scopes)

    kroger_products_api = KrogerProductsAPI(credentials)
    # Store Name: Fred Meyer - Hawthorne
    # Address: 3805 Se Hawthorne Blvd, Portland, OR
    user_location_id = "70100135"
    search = "milk"
    kroger_products_api.search_products(user_location_id, search)


if __name__ == '__main__':
    example()
