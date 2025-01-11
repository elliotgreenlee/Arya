import json


def load_json(file_path):
    with open(file_path, 'r') as file:
        dictionary = json.load(file)
        return dictionary
