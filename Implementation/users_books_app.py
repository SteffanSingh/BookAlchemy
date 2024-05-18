from datetime import datetime
import requests
from flask import request, flash, render_template, redirect, url_for, Blueprint
from Implementation.reusable_funciton import get_book_details
from data_managers.data_manager_interface_sql import SQLiteDataManager
from data_managers.data_models import Author, Book


userBook_app = Blueprint("userBook_app", __name__)

data_manager = SQLiteDataManager(userBook_app)


@userBook_app.route('/users')
def list_users():
    """function to display all the users with their favourite movies."""
    try:
        users = data_manager.list_all_users()
        return render_template('all_users.html', users=users)
    except Exception as error:
        return render_template("error.html")


@userBook_app.route("/update_user/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    """Function to implement the user profile like   email, profile image."""
    try:
        user_to_update = data_manager.get_user(user_id)
        if request.method == "POST":
            user_name = request.form.get("name")
            user_email = request.form.get("email")
            user_profile_image = request.form.get("profile")
            user_to_update.name = user_name if user_name else user_to_update.name
            user_to_update.email = user_email if user_email else user_to_update.email
            user_to_update.profile_image = user_profile_image if user_profile_image else " "
            data_manager.commit_change()
            flash(f"""{user_to_update.name}´s profile has been updated successfully !""")
            return redirect(url_for("userBook_app.update_user", user_id=user_id))
        return render_template("update_user.html", user_id=user_id, user=user_to_update)
    except Exception as error:
        return render_template("error.html")


@userBook_app.route("/delete_user/<int:user_id>", methods=["GET", "DELETE"])
def delete_user(user_id):
    """function to implement to delete user from a given user list."""
    try:
        user = data_manager.get_user(user_id)
        if not user:
            return render_template("error.html", error="User not found")
        data_manager.delete_user(user_id)
        return redirect(url_for("userBook_app.list_users"))
    except Exception as error:
        return render_template("error.html", error=error)


@userBook_app.route("/user/books/<int:user_id>")
def user_books(user_id):
    """Return the list of all user books and authors to render on
        user home page for a particular user id."""
    try:
        user = data_manager.get_user(user_id)
        user_books = user.book
        authors = data_manager.list_all_authors()
        return render_template("home.html", books=user_books, authors=authors, user_id=user_id)
    except Exception as error:
        return render_template("error.html", error=error)


@userBook_app.route("/add_book/<int:user_id>", methods=["GET", "POST"])
def book_add(user_id):
    """ Function to return the list of books after adding to a
            particular user with given user id."""
    try:
        authors = data_manager.list_all_authors()
        user_books = data_manager.list_user_books(user_id)
        user = data_manager.get_user(user_id)
        if request.method == "POST":
            title = request.form.get("title")
            publication_year_form = request.form.get("publication_year")
            isbn = request.form.get("isbn")
            author = request.form.get("author")
            book_details = get_book_details(title)
            """if not book_details:
                flash("Oops! This book is not available in database, Please try again !")
                return redirect(url_for("userBook_app.book_add", user_id=user_id))"""

            if book_details:
                publication_year_data = get_book_details(title)[3][:4]
                description = get_book_details(title)[4]
                rating = get_book_details(title)[5]
                isbn = get_book_details(title)[0]
                book_cover_image = get_book_details(title)[1]
                author_names = get_book_details(title)[2]

                # author_death_date = get_isbn(title)[4]
                # author_birth_date = get_isbn(title)[3]
                # print(datetime.strptime(publication_year, "%Y-%m-%d"),)
                author_info_api_url = f"https://en.wikipedia.org/wiki/{author_names[0].replace(' ', '_')}"
                response = requests.get(author_info_api_url)
                author_exist = data_manager.author_exist_or_not(author_names[0].title())
                if (not author_exist) and (Author.name not in author_names):
                    author = Author(
                        name=author_names[0].title(),
                        birth_date=None,
                        date_of_death=None
                    )
                    data_manager.add_author(author)
                    author_id = author.id
                else:
                    author_id = author_exist.id
                if publication_year_data and publication_year_data != "N/A":
                    if publication_year_data and len(publication_year_data) > 4:
                        if len(publication_year_data) == 7:
                            formatted_date_string = publication_year_data + '-01'
                            publication_year = datetime.strptime(formatted_date_string, "%Y-%m-%d")
                        else:
                            publication_year = datetime.strptime(publication_year_data, "%Y-%m-%d")
                    else:
                        publication_new_year = f"{int(publication_year_data)}-01-01"
                        publication_year = datetime.strptime(publication_new_year, "%Y-%m-%d")
                else:
                    publication_year = datetime.strptime(publication_year_form, "%Y-%m-%d")
                book_exist = data_manager.book_exist_or_not(title.title())
                if book_exist:
                    user.book.append(book_exist)
                    data_manager.commit_change()
                else:
                    book = Book(
                        title=title.title(),
                        publication_year=publication_year,
                        isbn=isbn,
                        author_id=author_id,
                        book_cover=book_cover_image,
                        description=description,
                        rating=rating
                    )
                    user.book.append(book)
                    data_manager.add_book(book)
            else:
                book = Book(
                    title=title.title(),
                    publication_year=datetime.strptime(publication_year_form, "%Y-%m-%d"),
                    isbn=isbn,
                    author_id=data_manager.author_by_name(author),
                    book_cover="Enter your book cover image",
                    description=" ",
                    rating=0
                )

                book_exist = data_manager.book_exist_or_not(title.title())
                if not book_exist:
                    data_manager.add_book(book)
                    user.book.append(book)
                else:
                    user.book.append(book_exist)
                    data_manager.commit_change()
            books = data_manager.list_user_books(user_id)
            authors = data_manager.list_all_authors()
            flash(f"""Book "{title.title()}" has been successfully added !""")
            return redirect(url_for("userBook_app.book_add", user_id=user_id))
        return render_template("add_book.html", user_id=user_id, user=user, authors=authors)
    except Exception as error:
        return render_template("error.html", error=error)


@userBook_app.route("/search_new_book/<int:user_id>", methods=["GET", "POST"])
def search_new_book(user_id):
    try:
        user = data_manager.get_user(user_id)
        if request.method == "POST":
            title = request.form.get("title")
            book_exist = data_manager.book_exist_or_not(title.title())
            if not book_exist:
                bookDetails = get_book_details(title)
                if bookDetails:
                    publication_year_data = get_book_details(title)[3][:4]
                    description = get_book_details(title)[4]
                    rating = get_book_details(title)[5]
                    isbn = get_book_details(title)[0]
                    book_cover_image = get_book_details(title)[1]
                    author_names = get_book_details(title)[2]
                    author_info_api_url = f"https://en.wikipedia.org/wiki/{author_names[0].replace(' ', '_')}"
                    response = requests.get(author_info_api_url)
                    author_exist = data_manager.author_exist_or_not(author_names[0].title())
                    if (not author_exist) and (Author.name not in author_names):
                        author = Author(
                            name=author_names[0].title(),
                            birth_date=None,
                            date_of_death=None
                        )
                        data_manager.add_author(author)
                        author_id = author.id
                    else:
                        author_id = author_exist.id
                    if publication_year_data and publication_year_data != "N/A":
                        if publication_year_data and len(publication_year_data) > 4:
                            if len(publication_year_data) == 7:
                                formatted_date_string = publication_year_data + '-01'
                                publication_year = datetime.strptime(formatted_date_string, "%Y-%m-%d")
                            else:
                                publication_year = datetime.strptime(publication_year_data, "%Y-%m-%d")
                        else:
                            publication_new_year = f"{int(publication_year_data)}-01-01"
                            publication_year = datetime.strptime(publication_new_year, "%Y-%m-%d")
                    else:
                        publication_year = datetime.strptime("2000-01-01", "%Y-%m-%d")
                    book_exist = data_manager.book_exist_or_not(title.title())
                    if book_exist in user.book:

                        flash(f"""   Book Already exists in the {user.name}´s library !""")
                        return render_template("search_new_book_result.html", user=user, book=book_exist,
                                               user_id=user_id)
                    else:
                        book = Book(
                            title=title.title(),
                            publication_year=publication_year,
                            isbn=isbn,
                            author_id=author_id,
                            book_cover=book_cover_image,
                            description=description,
                            rating=rating
                        )

                        book_exist = data_manager.book_exist_or_not(title.title())
                        if not book_exist:
                            data_manager.add_book(book)
                            user.book.append(book)
                        else:
                            user.book.append(book_exist)
                            data_manager.commit_change()
                        return render_template("search_new_book_result.html", user=user, book=book, user_id=user_id)
                else:
                    return render_template("book_not_found.html")
            else:
                if book_exist in user.book:
                    flash(f"""   Book Already exists in the {user.name}´s library !""")
                    return render_template("search_new_book.html", user=user, book=book_exist,
                                           user_id=user_id)
                else:
                    flash(f"""Book already exists in the Admin library, would like to add in your library?""")
                    return render_template("search_new_book_result.html", user=user, book=book_exist, user_id=user_id)
        return render_template("search_new_book.html", user_id=user_id, user=user)
    except Exception as error:
        return render_template("error.html", error=error)


@userBook_app.route("/add_book_to_user/<int:user_id>/<int:book_id>")
def add_book_to_user(user_id, book_id):
    try:
        user = data_manager.get_user(user_id)
        book = data_manager.get_book(book_id)
        if book not in user.book:
            user.book.append(book)
            data_manager.commit_change()
        return render_template("home.html", books=user.book, user_id=user_id)
    except Exception as error:
        return render_template("error.html", error=error)


@userBook_app.route("/user/<int:user_id>/book_update/<int:book_id>", methods=["GET", "POST"])
def user_book_update(user_id, book_id):
    """Function to update the book details such title, description, rating etc."""
    try:
        user = data_manager.get_user(user_id)
        authors = data_manager.list_all_authors()
        book_to_update = data_manager.get_book(book_id)
        book_title = book_to_update.title
        if request.method == "POST":
            update_title = request.form.get("title")
            update_publication_year = request.form.get("publication_year")
            update_author = request.form.get("author")
            author_id = data_manager.author_by_name(update_author)
            update_isbn = request.form.get("title")
            update_book_cover = request.form.get("book-cover")
            update_description = request.form.get("description")
            update_rating = request.form.get("rating")
            # updating the book details
            book_to_update.title = update_title.title() if update_title else book_to_update.title
            book_to_update.publication_year = datetime.strptime(update_publication_year,
                                                                "%Y-%m-%d") if update_publication_year else book_to_update.publication_year
            book_to_update.isbn = update_isbn if update_isbn else book_to_update.isbn
            book_to_update.book_cover = update_book_cover if update_book_cover else book_to_update.book_cover
            book_to_update.author_id = author_id if update_author else book_to_update.author_id
            book_to_update.description = update_description if update_description else book_to_update.description
            book_to_update.rating = update_rating if update_rating else book_to_update.rating
            data_manager.commit_change()
            flash(f"""Book "{book_to_update.title}" has been updated successfully !""")
            return redirect(url_for("userBook_app.user_book_update", user_id=user_id, book_id=book_id))
        return render_template("update_book.html", book=book_to_update, user=user, user_id=user_id, book_id=book_id,
                               title=book_title,
                               authors=authors)
    except Exception as error:
        return render_template("error.html", error=error)


@userBook_app.route("/bookDetails/<int:user_id>/<int:book_id>")
def bookDetail(user_id, book_id):
    """Return the book details for a given book with book id
        of a particular user with given user id."""
    try:
        user = data_manager.get_user(user_id)
        book = data_manager.get_book(book_id)
        book_reviews = data_manager.list_all_reviews(book_id)
        length = len(book_reviews)
        # print(book.details)
        return render_template("book_details.html", user=user, user_id=user_id, book=book, length=length,
                               reviews=book_reviews)
    except Exception as error:
        return render_template("error.html", error=error)


@userBook_app.route("/sort/<int:user_id>")
def sort_book(user_id):
    """Return the sorted book list for a particular user with a given user id."""
    try:
        sort_by = request.args.get("sort_by")
        authors = data_manager.list_all_authors()
        if sort_by == "title":
            books = data_manager.sort_by_book_title_ascending(user_id)
        elif sort_by == "author":
            books = data_manager.sort_by_authors_ascending(user_id)
        else:
            books = []
        return render_template("home.html", books=books, user_id=user_id, authors=authors, sort_by=sort_by)
    except Exception as error:
        return render_template("error.html", error=error)


@userBook_app.route("/book_delete/<int:user_id>/<int:book_id>")
def delete_book(user_id, book_id):
    user = data_manager.get_user(user_id)
    book = data_manager.get_book(book_id)
    try:
        if book in user.book:
            user.book.remove(book)
            data_manager.commit_change()
            """association_deleted = data_manager.remaining_assocaition(user_id,book_id)

            # Check if exactly one row was deleted from the association table
            # Check if an association exists
            if association_deleted:
                # Delete only the found association
                data_manager.delete_book(association_deleted)
            """
            return redirect(url_for("userBook_app.user_books", user_id=user_id))
    except Exception as e:
        return render_template("error.html", error=e)


@userBook_app.route("/search/<int:user_id>", methods=["GET", "POST"])
def search(user_id):
    try:
        if request.method == "POST":
            keyword = request.form.get("keyword")
            book_data = data_manager.search_book(user_id, keyword)
            if book_data:
                return render_template("search_result.html", keyword=keyword, user_id=user_id, books=book_data)
            else:
                user = data_manager.get_user(user_id)
                return render_template("no_result.html", user_id=user_id, user=user)
        books = data_manager.list_user_books(user_id)
        authors = data_manager.list_all_authors()
        return render_template("home.html", books=books, user_id=user_id, authors=authors)
    except Exception as error:
        return render_template("error.html", error=error)
