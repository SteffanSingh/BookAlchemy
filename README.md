# Book Library

## A digital book library for book lovers to create and manage a vast collection of books based on their favorite authors and genres. Users can add, delete, and update book details as needed.

- **Server-Side Rendering:** The application uses server-side rendering for dynamic content.
- **Search Functionality:** Search for books by title, publication year, and author.
- **Sorting:** Sort books for a particular user by title and author.
- **Authentication:** Signup, signin, and password reset functionalities are implemented.
- **Technologies Used:** Python, Flask, SQL, Jinja2, HTML, CSS.

<p align="center">
  <img src="https://github.com/SteffanSingh/BookAlchemy/blob/7d60c39e60bcec63115ba7356160c4c65bae4229/Project-Images/bookLibrary1.png" alt="Book Library Home Page">
  <img src="https://github.com/SteffanSingh/BookAlchemy/blob/7d60c39e60bcec63115ba7356160c4c65bae4229/Project-Images/bookdetails.png" alt="Book Details Page">
  <img src="https://github.com/SteffanSingh/BookAlchemy/blob/7d60c39e60bcec63115ba7356160c4c65bae4229/Project-Images/updatepage.png" alt="Book Update Page">
</p>

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and authorization
- Add, update, delete, and view book details
- Search for books by title, publication year, and author
- Sort books by title and author
- Responsive design with HTML and CSS

## Installation

### Prerequisites

- Python 3.7+
- Flask
- SQLAlchemy
- Flask-Login
- Jinja2
- Other dependencies listed in `requirements.txt`

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/book-library.git
    cd book-library
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

5. Run the application:

    ```bash
    flask run
    ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5000`.
2. Create an account or log in if you already have one.
3. Use the navigation menu to add, update, delete, or view books.
4. Use the search bar to find books.
5. Sort books using the dropdown menu.

## API Endpoints

### User Endpoints

- **GET /users/<int:user_id>**
  - Get user details.

- **POST /users/<int:user_id>/add_book**
  - Add a new book for the user.

- **POST /users/<int:user_id>/update_book/<int:book_id>**
  - Update details of an existing book.

- **GET /users/<int:user_id>/delete_book/<int:book_id>**
  - Delete a book for the user.

### Sorting Books

- **GET /sort/<int:user_id>**
  - Sort books by title or author.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
