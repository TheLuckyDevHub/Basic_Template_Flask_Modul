import json
import os

# Basic color codes
RED = '\033[91m'
RESET = '\033[0m'  # This resets the color back to default


BLOG_POSTS_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data.json')
DEFAULT_BLOG_DATA = [
    {
        "id": 1,
        "author": "John Doe",
        "title": "Default Post",
        "content": "This is a post from default data."
    },
]
blog_posts_cached = None

def get_blog_posts() -> list[dict[str, str]]:
    """
    Returns a list of dictionaries that
    contains the blog posts information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    [
      {
        "id": 1,
        "author": "John Doe",
        "title": "My First Post",
        "content": "This is the content of my first post."
      },
      {
        "id": 2,
        "author": "Jane Doe",
        "title": "Another Post",
        "content": "More content here."
      }
    ]
    """
    global blog_posts_cached

    if blog_posts_cached != None:
        return blog_posts_cached

    posts = DEFAULT_BLOG_DATA

    if not os.path.exists(BLOG_POSTS_DATA_PATH):
        print(f'{RED}Data file {BLOG_POSTS_DATA_PATH} not exist get the default blog posts data!{RESET}')
        save_blog_posts(posts)
        return posts

    try:
        with open(BLOG_POSTS_DATA_PATH, 'r') as filehandle:
            try:
                posts = json.load(filehandle)
            except json.decoder.JSONDecodeError as e:
                print(f'{RED}Json file {BLOG_POSTS_DATA_PATH} could not be loaded JSON decoder error:{RESET} {e.msg}')
            except Exception as e:
                """
                This general exception is here, which can give many other errors, e.g.memory full, no
                permission, file corrupted etc.
                """
                print(f'{RED}Json file {BLOG_POSTS_DATA_PATH} could not be loaded general error:{RESET} {e}')
    except Exception as e:
        """
        This general exception is here, which can give many other errors, e.g.memory full, no
        permission, file corrupted etc.
        """
        print(f'{RED}Data file {BLOG_POSTS_DATA_PATH} could not be opened general error:{RESET} {e}')

    blog_posts_cached = posts
    return posts


def save_blog_posts(posts: list[dict[str, str]]) -> None:
    """
    Saves the blog posts data to the JSON file.

    The function takes a list of dictionaries containing
    blog posts information and saves it to the JSON file.
    """
    try:
        with open(BLOG_POSTS_DATA_PATH, 'w') as filehandle:
            json.dump(posts, filehandle, indent=4)
    except Exception as e:
        """
        This general exception is here, which can give many other errors, e.g.memory full, no
        permission, file corrupted etc.
        """
        print(f'{RED}Data file {BLOG_POSTS_DATA_PATH} could not be saved general error:{RESET} {e}')
    global blog_posts_cached
    blog_posts_cached = None
