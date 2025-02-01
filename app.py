import os

from flask import Flask, render_template

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
