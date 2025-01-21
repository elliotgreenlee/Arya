# Manages cooking planning

import json
from API_Helpers.spoonacular_utils import SpoonacularAPI
from Utils.utils import load_json
from API_Helpers.Kroger.kroger_products_utils import KrogerProductsAPI
from API_Helpers.Kroger.kroger_cart_utils import KrogerCartAPI


def example():
    spoonacular_credentials_path = '../Credentials/api_keys.json'
    api_keys = load_json(spoonacular_credentials_path)

    scope = "profile.compact product.compact cart.basic:write"
    user_kroger_credentials_path = '../Credentials/kroger_user_token.json'
    kroger_credentials_path = '../Credentials/kroger_client.json'
    kroger_products_api = KrogerProductsAPI(user_kroger_credentials_path, kroger_credentials_path, scope)

    scope = "profile.compact product.compact cart.basic:write"
    user_kroger_credentials_path = '../Credentials/kroger_user_token.json'
    kroger_credentials_path = '../Credentials/kroger_client.json'
    kroger_cart_api = KrogerCartAPI(user_kroger_credentials_path, kroger_credentials_path, scope)

    spoonacular = SpoonacularAPI(api_keys['spoonacular_api_key'])
    recipe_count = 1
    recipes = spoonacular.random_recipes(recipe_count)

    print(f"Your random recipe is:")
    for recipe in recipes:
        print(f"Title: {recipe['title']}")
        print(f"Servings: {recipe['servings']}")
        print(f"Instructions: {recipe['instructions']}")
        print(f"Source URL: {recipe['spoonacularSourceUrl']}")
        print(f"Ingredients:")
        for ingredient in recipe['extendedIngredients']:
            print(f"    {ingredient['amount']} {ingredient['unit']} {ingredient['nameClean']}")
            # Store Name: Fred Meyer - Hawthorne
            # Address: 3805 Se Hawthorne Blvd, Portland, OR
            user_location_id = "70100135"
            search = f"{ingredient['nameClean']}"
            limit = 1
            products = kroger_products_api.search_products(user_location_id, search, limit)
            for product in products:
                quantity = 1
                modality = "DELIVERY"
                cart_response = kroger_cart_api.add_to_cart(product['upc'], quantity, modality)
                print(f"{cart_response}")


if __name__ == "__main__":
    example()
