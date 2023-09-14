import json

# File path to your JSON file
JSON_FILE_PATH = "keyword_responses.json"

def load_keyword_responses():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def update_keyword_responses(keyword_responses):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(keyword_responses, file, indent=4)
