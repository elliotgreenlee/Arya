from Utils.utils import load_json
import requests


class SpoonacularAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def random_recipes(self, recipe_count):
        endpoint = f"https://api.spoonacular.com/recipes/random"
        params = {
            "apiKey": self.api_key,
            "number": recipe_count  # Number of random recipes to retrieve
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()

            data = response.json()

            if "recipes" in data and data["recipes"]:
                for recipe in data["recipes"]:
                    print(f"Recipe Name: {recipe['title']}")
                    print(f"Ready in Minutes: {recipe['readyInMinutes']}")
                    print(f"Servings: {recipe['servings']}")
                    print(f"Summary: {recipe['summary']}")
            else:
                print("No recipes found.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


def example():
    spoonacular_credentials_path = '../Credentials/api_keys.json'
    api_keys = load_json(spoonacular_credentials_path)

    spoonacular = SpoonacularAPI(api_keys['spoonacular_api_key'])
    recipe_count = 1
    spoonacular.random_recipes(recipe_count)


if __name__ == '__main__':
    example()
