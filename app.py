import os

from flask import Flask, render_template, request, redirect, url_for
from nanoid import generate

from storage import load_posts, save_posts

app = Flask(__name__)

# initial storage setup
os.makedirs(app.instance_path, exist_ok=True)
POSTS_FILE = os.path.join(app.instance_path, "posts.json")

# add empty posts file if none found
if not os.path.exists(POSTS_FILE):
    save_posts(POSTS_FILE, [])


@app.route('/')
def index():
    blog_posts = load_posts(POSTS_FILE)
    return render_template('index.html', posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        current_posts = load_posts(POSTS_FILE)
        new_post = {
            "id": generate(),
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "content": request.form.get("content")
        }
        current_posts.append(new_post)
        save_posts(POSTS_FILE, current_posts)
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route('/delete/<post_id>')
def delete(post_id):
    current_posts = load_posts(POSTS_FILE)
    remaining_posts = [post for post in current_posts if str(post['id']) != post_id]
    save_posts(POSTS_FILE, remaining_posts)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
