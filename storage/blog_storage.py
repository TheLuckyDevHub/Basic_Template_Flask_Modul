import json
import os
import logging

# Set up basic logging to output errors and warnings.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Custom Exceptions for clear error handling ---
class StorageError(Exception):
    """Base class for exceptions in this storage module."""
    pass

class DataFileError(StorageError):
    """Raised for errors related to file access (e.g., cannot read or write)."""
    pass

class DataFormatError(StorageError):
    """Raised for errors in the data format (e.g., invalid JSON, missing keys)."""
    pass

# --- Constants and Cache ---
BLOG_POSTS_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data.json')
DEFAULT_BLOG_DATA = [
    {
        "id": 1,
        "author": "Max Mustermann",
        "title": "Default Post",
        "content": "This is a post from default data."
    },
]
blog_posts_cached = None


def get_blog_posts() -> list[dict[str, str]]:
    """
    Returns a list of all blog posts from the data file.
    - Creates the file with default data if it doesn't exist.
    - Caches the data in memory after the first read.
    - Raises exceptions for file I/O or data format errors.
    """
    global blog_posts_cached
    if blog_posts_cached is not None:
        return blog_posts_cached

    if not os.path.exists(BLOG_POSTS_DATA_PATH):
        logging.warning(f"Data file not found at {BLOG_POSTS_DATA_PATH}. Creating it with default data.")
        save_blog_posts(DEFAULT_BLOG_DATA)
        posts = DEFAULT_BLOG_DATA
    else:
        try:
            with open(BLOG_POSTS_DATA_PATH, 'r') as filehandle:
                posts = json.load(filehandle)
        except json.JSONDecodeError as e:
            logging.error(f"Data format error in {BLOG_POSTS_DATA_PATH}: {e}")
            raise DataFormatError(f"Could not decode JSON from data file.") from e
        except OSError as e:
            logging.error(f"File read error for {BLOG_POSTS_DATA_PATH}: {e}")
            raise DataFileError(f"Could not read data file: {e}") from e

    # --- Basic Data Validation ---
    if not isinstance(posts, list):
        raise DataFormatError("Data file content must be a list of posts.")
    for post in posts:
        if not isinstance(post, dict) or "id" not in post:
            raise DataFormatError(f"Invalid post object found in data file: {post}")

    blog_posts_cached = posts
    return posts


def save_blog_posts(posts: list[dict[str, str]]) -> None:
    """
    Saves a list of blog posts to the JSON data file.
    - Invalidates the cache after writing.
    - Raises DataFileError on file I/O issues.
    """
    global blog_posts_cached
    try:
        with open(BLOG_POSTS_DATA_PATH, 'w') as filehandle:
            json.dump(posts, filehandle, indent=4)
        blog_posts_cached = None  # Invalidate cache after a successful write
    except (OSError, TypeError) as e:
        logging.error(f"Error saving data to {BLOG_POSTS_DATA_PATH}: {e}")
        raise DataFileError(f"Could not save data file: {e}") from e


def _get_next_id(posts: list[dict[str, str]]) -> int:
    """
    Calculates the next available ID for a new blog post.
    """
    if not posts:
        return 1
    try:
        # Find the highest existing ID and add 1
        return max(post["id"] for post in posts) + 1
    except (KeyError, TypeError) as e:
        raise DataFormatError("Could not determine next ID due to invalid post data.") from e


def add_blog_post(author: str, title: str, content: str) -> dict:
    """
    Adds a new blog post to the data file.
    Returns the newly created post dictionary.
    """
    posts = get_blog_posts()
    new_post = {
        "id": _get_next_id(posts),
        "author": author,
        "title": title,
        "content": content
    }
    posts.append(new_post)
    save_blog_posts(posts)
    return new_post


def delete_blog_post(post_id: int) -> bool:
    """
    Deletes a blog post by its ID.
    Returns True if a post was deleted, False otherwise.
    """
    posts = get_blog_posts()
    original_count = len(posts)
    posts_to_keep = [post for post in posts if post.get("id") != post_id]

    if len(posts_to_keep) < original_count:
        save_blog_posts(posts_to_keep)
        return True
    return False  # No post with the given ID was found


def get_blog_post_by_id(post_id: int) -> dict[str, str] | None:
    """
    Retrieves a single blog post by its ID.
    Returns the post dictionary or None if not found.
    """
    posts = get_blog_posts()
    for post in posts:
        if post.get("id") == post_id:
            return post
    return None


def update_blog_post(post_id: int, author: str, title: str, content: str) -> dict | None:
    """
    Updates an existing blog post.
    Returns the updated post dictionary or None if the post was not found.
    """
    posts = get_blog_posts()
    post_to_update = None
    for post in posts:
        # Use .get() for safer access
        if post.get("id") == post_id:
            post["author"] = author
            post["title"] = title
            post["content"] = content
            post_to_update = post
            break  # Exit loop once the post is found and updated

    if post_to_update:
        save_blog_posts(posts)
        return post_to_update
    return None  # Post ID not found
