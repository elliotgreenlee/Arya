import requests

def add_to_cart(access_token, customer_id, product_id, quantity):
    api_url = f"https://api.kroger.com/v1/cart/add"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "customerId": customer_id,  # Replace with the customer's unique identifier
        "items": [
            {
                "upc": product_id,  # Universal Product Code of the item
                "quantity": quantity
            }
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        print("Cart API Response:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example Usage
access_token = "your_access_token_here"  # Replace with your valid access token
customer_id = "customer_id_here"  # Replace with the actual customer ID
product_id = "0001111041702"  # Replace with a valid UPC of a product
quantity = 1  # Quantity of the product to add

response = add_to_cart(access_token, customer_id, product_id, quantity)
