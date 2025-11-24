from flask import Flask, render_template, request, redirect
import storage.blog_storage as storage

app = Flask(__name__)


@app.route("/")
def index():
    """
    Renders the main page, displaying a list of all blog posts.

    Fetches all blog posts from the storage and passes them to the
    index.html template.

    Returns:
        Rendered HTML template for the home page.
    """
    # add code here to fetch the job posts from a file
    blog_posts = storage.get_blog_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Handles the creation of a new blog post.

    - GET: Displays a form to create a new post.
    - POST: Processes the submitted form data and saves the new post.
      Redirects to the home page upon successful creation.

    Returns:
        - Rendered 'add.html' template on GET.
        - Redirect to the home page ('/') on POST.
    """
    if request.method == "POST":
        storage.add_blog_post(
            request.form["author"],
            request.form["title"],
            request.form["content"]
        )
        return redirect("/")

    return render_template(
        "add.html",
        action="add",
        title="Add Blog Post",
        header_post_container="New Post",
        post_author="Author",
        post_title="Title",
        post_content="Content",
        button_text="Add Post",
    )


@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete(post_id):
    """
    Deletes a blog post identified by its ID.

    This route is typically accessed via a POST request from a button,
    but also supports GET for simpler links. It deletes the post
    and then redirects to the home page.

    Args:
        post_id (int): The ID of the post to be deleted.

    Returns:
        Redirect to the home page ('/').
    """
    storage.delete_blog_post(post_id)
    return redirect("/")


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit(post_id):
    """
    Handles editing an existing blog post.

    - GET: Displays a pre-filled form for the specified post.
    - POST: Processes and saves the updated post data.
      Redirects to the home page upon successful update.

    If the post is not found, it returns a 404 error.

    Args:
        post_id (int): The ID of the post to be edited.

    Returns:
        - Rendered 'add.html' template with post data on GET.
        - Redirect to the home page ('/') on POST.
        - A 404 error message if the post is not found.
    """
    if request.method == "POST":
        storage.update_blog_post(
            post_id,
            request.form["author"],
            request.form["title"],
            request.form["content"],
        )
        return redirect("/")

    post = storage.get_blog_post_by_id(post_id)
    if post:
        return render_template(
            "add.html",
            action=f"edit/{post_id}",
            title="Edit Blog Post",
            header_post_container="Edit Post",
            post_author=post["author"],
            post_title=post["title"],
            post_content=post["content"],
            button_text="Update Post",
        )

    return "Post not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
