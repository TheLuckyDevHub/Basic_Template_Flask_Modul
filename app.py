from flask import Flask, render_template, request
import storage.blog_storage as storage

app = Flask(__name__)


@app.route("/")
def index():
    # add code here to fetch the job posts from a file
    blog_posts = storage.get_blog_posts()
    return render_template("index.html", posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        storage.add_blog_post(
            request.form['author'],
            request.form['title'],
            request.form['content'])

    return render_template('add.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
