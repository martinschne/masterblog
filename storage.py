import json


def save_posts(data_file, data: []):
    """
    Saves the given data to a file in JSON format.

    This function writes the provided data to a file, overwriting the existing
    content in the file. The data is saved in JSON format.

    Args:
        data_file (str): The path to the file where the data should be saved.
        data (list): The data to be saved, typically a list of blog posts.
    """
    with open(data_file, "w") as f:
        json.dump(data, f)


def load_posts(data_file) -> list[dict]:
    """
    Loads and returns data from a JSON file.

    This function reads the data from the specified file and parses it as JSON.

    Args:
        data_file (str): The path to the file from which data should be loaded.

    Returns:
        list: The parsed JSON data, typically a list of blog posts.
    """
    with open(data_file, "r") as f:
        return json.load(f)


def fetch_post_by_id(data_file, id: str) -> tuple[dict | None, list[dict]]:
    """
    Fetches a blog post by its ID.

    This function loads all posts from the file and returns the post with the
    matching ID. It also returns the list of all posts for further operations.

    Args:
        data_file (str): The path to the file containing the posts.
        id (str): The ID of the post to fetch.

    Returns:
        tuple: A tuple containing the matching post (or None if not found) and
               the list of all posts.
    """
    posts = load_posts(data_file)
    matching_post = next((post for post in posts if post["id"] == id), None)
    return matching_post, posts
