import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from nanoid import generate

from storage import load_posts, save_posts, fetch_post_by_id

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

# initial storage setup
os.makedirs(app.instance_path, exist_ok=True)
POSTS_FILE = os.path.join(app.instance_path, "posts.json")

# add empty posts file if none found
if not os.path.exists(POSTS_FILE):
    save_posts(POSTS_FILE, [])


def _is_valid_post(post: dict) -> bool:
    """
    Validates the given blog post.

    Checks if the 'title', 'author', and 'content' fields of the post
    are not empty. If any field is empty, an error message is flashed.

    Args:
        post (dict): A dictionary representing the blog post to validate.

    Returns:
        bool: True if the post is valid (no empty fields), False otherwise.
    """
    errors = 0
    if len(post["title"].strip()) == 0:
        flash("Title field cannot be empty!")
        errors += 1
    if len(post["author"].strip()) == 0:
        flash("Author field cannot be empty!")
        errors += 1
    if len(post["content"].strip()) == 0:
        flash("Content field cannot be empty!")
        errors += 1

    return errors == 0


@app.route('/')
def index() -> str:
    """
    Renders the index page showing all blog posts.

    This function loads all posts from the file and renders the
    'index.html' template, passing the posts to the template.

    Returns:
        Response: The rendered 'index.html' template with posts.
    """
    blog_posts = load_posts(POSTS_FILE)
    return render_template('index.html', posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add() -> Response | str:
    """
    Handles the creation of a new blog post.

    If the request method is POST, this function creates a new post
    with the provided form data, validates it, and adds it to the list of posts.
    If the request method is GET, it renders the form to add a new post.

    Returns:
        Response: Redirect to the 'index' route if successful, or render
                  the 'add.html' template if the request is GET.
    """
    if request.method == "POST":
        current_posts = load_posts(POSTS_FILE)
        new_post = {
            "id": generate(),
            "title": request.form.get("title").strip(),
            "author": request.form.get("author").strip(),
            "content": request.form.get("content").strip()
        }

        if not _is_valid_post(new_post):
            return redirect(url_for("add"))

        current_posts.append(new_post)
        save_posts(POSTS_FILE, current_posts)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route('/delete/<post_id>')
def delete(post_id: str) -> Response:
    """
    Deletes a blog post by its ID.

    This function removes a post from the list of posts based on the
    provided post ID and saves the updated list back to the file.

    Args:
        post_id (str): The ID of the post to delete.

    Returns:
        Response: Redirect response to the 'index' route after deleting the post.
    """
    current_posts = load_posts(POSTS_FILE)
    remaining_posts = [post for post in current_posts if str(post['id']) != post_id]
    save_posts(POSTS_FILE, remaining_posts)
    return redirect(url_for("index"))


@app.route('/update/<post_id>', methods=["GET", "POST"])
def update(post_id: str) -> tuple[str, int] | Response | str:
    """
    Updates an existing blog post.

    If the request method is POST, this function updates the post with
    the provided ID using the form data. If the request method is GET,
    it renders the form pre-filled with the current post data.

    Args:
        post_id (str): The ID of the post to update.

    Returns:
        Response: Redirect to the 'index' route after updating the post,
                  or render the 'update.html' template if the request is GET.
    """
    post, posts = fetch_post_by_id(POSTS_FILE, post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        for post in posts:
            if post["id"] == post_id:
                post["title"] = request.form.get("title").strip()
                post["author"] = request.form.get("author").strip()
                post["content"] = request.form.get("content").strip()
                break

        save_posts(POSTS_FILE, posts)
        return redirect(url_for("index"))

    return render_template('update.html', post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
