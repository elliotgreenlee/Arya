from Utils.utils import load_json
import requests
import json


class SpoonacularAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def random_recipes(self, recipe_count):
        endpoint = f"https://api.spoonacular.com/recipes/random"
        params = {
            "apiKey": self.api_key,
            "number": recipe_count  # Number of random recipes to retrieve
        }

        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('recipes', [])


def example():
    spoonacular_credentials_path = '../Credentials/api_keys.json'
    api_keys = load_json(spoonacular_credentials_path)

    spoonacular = SpoonacularAPI(api_keys['spoonacular_api_key'])
    recipe_count = 2
    recipes = spoonacular.random_recipes(recipe_count)

    for recipe in recipes:
        print(json.dumps(recipe, indent=4))


if __name__ == '__main__':
    example()
