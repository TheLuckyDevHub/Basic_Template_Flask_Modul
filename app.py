from flask import Flask, render_template
import storage.blog_storage as storage

app = Flask(__name__)


@app.route("/")
def index():
    # add code here to fetch the job posts from a file
    blog_posts = storage.get_blog_posts()
    return render_template("index.html", posts=blog_posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
