# Simple Flask Blog

A basic blog application built with Flask that allows users to create, view, edit, and delete posts. The data is stored in a simple JSON file.

## Features

-   **View All Posts**: The main page lists all blog posts.
-   **Add a Post**: A dedicated form to add new posts.
-   **Edit a Post**: Edit existing posts using a similar form.
-   **Delete a Post**: Remove posts from the blog.
-   **JSON-based Storage**: Posts are stored in a `data.json` file, making it easy to see how data persistence can be handled simply.

## Project Structure

```
.
├── app.py              # Main Flask application file
├── requirements.txt    # Project dependencies
├── storage/
│   ├── blog_storage.py # Module for handling data storage (read/write to JSON)
│   └── data.json       # The JSON file where posts are stored
├── static/
│   └── index_style.css # Stylesheet for the application
├── templates/
│   ├── index.html      # Main template to display all posts
│   └── add.html        # Template for adding and editing posts
└── README.md           # This file
```

## Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository (or download the files).**

2.  **Create and activate a virtual environment:**
    ```bash
    # Create a virtual environment
    python -m venv .venv

    # Activate the virtual environment
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install the required dependencies:**
    Install the project dependencies from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```

## Usage

Once the application is running, open your web browser and navigate to:

```
http://127.0.0.1:5000
```

You can view all posts on the main page. Use the "Add Post" button to create a new entry. The "Edit" and "Delete" buttons next to each post allow you to manage existing entries.