from kroger_utils import KrogerAPI
import requests
import json


class KrogerProductsAPI(KrogerAPI):
    def __init__(self, user_credentials_path, api_credentials_path, scope):
        super().__init__(user_credentials_path, api_credentials_path, scope)

    def search_products(self, location_id, search_term, limit=5):
        print("Searching Products")
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
            products = response.json()
            return products.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


def example():
    scope = "profile.compact product.compact cart.basic:write"
    user_kroger_credentials_path = '../Credentials/kroger_user_token.json'
    kroger_credentials_path = '../Credentials/kroger_client.json'
    kroger_products_api = KrogerProductsAPI(user_kroger_credentials_path, kroger_credentials_path, scope)

    # Store Name: Fred Meyer - Hawthorne
    # Address: 3805 Se Hawthorne Blvd, Portland, OR
    user_location_id = "70100135"
    search = "milk"
    products = kroger_products_api.search_products(user_location_id, search)

    for product in products:
        print(json.dumps(product, indent=4))


if __name__ == '__main__':
    example()
