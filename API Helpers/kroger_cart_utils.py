import requests
from kroger_utils import KrogerAPI
import json


class KrogerCartAPI(KrogerAPI):
    def __init__(self, user_credentials_path, api_credentials_path, scope):
        super().__init__(user_credentials_path, api_credentials_path, scope)

    def add_to_cart(self, product_upc, quantity, modality):
        api_url = f"https://api.kroger.com/v1/cart/add"
        headers = {
            "Authorization": f"Bearer {self.credentials.token}",
            "Accept": "application/json",
        }

        payload = {
            "items": [
                {
                    "quantity": quantity,
                    "upc": product_upc,
                    "modality": modality
                }
            ]
        }

        # Make the PUT request
        response = requests.put(api_url, json=payload, headers=headers)
        if response.status_code == 204:
            cart_response = "Success"
        else:
            cart_response = response.json()
        return cart_response


def example():
    scope = "profile.compact product.compact cart.basic:write"
    user_kroger_credentials_path = '../Credentials/kroger_user_token.json'
    kroger_credentials_path = '../Credentials/kroger_client.json'
    kroger_cart_api = KrogerCartAPI(user_kroger_credentials_path, kroger_credentials_path, scope)

    # Fred Meyer 2% Reduced Fat Milk Gallon
    product_upc = "0001111041550"
    quantity = 1
    modality = "DELIVERY"
    cart_response = kroger_cart_api.add_to_cart(product_upc, quantity, modality)
    print(json.dumps(cart_response, indent=4))


if __name__ == '__main__':
    example()
