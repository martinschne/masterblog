# Ensure the /instance folder exists
import json
import os


# Function to save JSON data
def save_posts(data_file, data: []):
    with open(data_file, "w") as f:
        json.dump(data, f)


# Function to load JSON data
def load_posts(data_file):
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)

    return []
