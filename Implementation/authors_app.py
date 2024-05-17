from flask import Flask, request, flash, render_template, redirect, url_for, Blueprint
from data_managers.data_manager_interface_sql import session, SQLiteDataManager, database
from data_managers.data_models import User, Author, Book
import requests
from datetime import datetime
from Implementation.reusable_funciton import get_book_details


authors_app = Blueprint("authors_app", __name__)

data_manager = SQLiteDataManager(authors_app)

@authors_app.route("/add_author/<int:user_id>", methods=["GET", "POST"])
def author_add(user_id):
    try:

        user = data_manager.get_user(user_id)
        if request.method == "POST":
            name = request.form.get("name")
            birthdate = request.form.get("birthdate")
            date_of_death = request.form.get("date_of_death")
            print(name, birthdate)
            # Instantiating the author class
            author = Author(
                name=name.title(),
                birth_date=datetime.strptime(birthdate, "%Y-%m-%d"),
                date_of_death=datetime.strptime(date_of_death, "%Y-%m-%d") if date_of_death else None
            )
            data_manager.add_author(author)
            flash(f"""Author "{name.title()}" has been successfully added!""")
            return redirect(url_for("authors_app.author_add", user_id=user_id))
        return render_template("add_author.html", user_id=user_id, user=user)
    except Exception as error:
        return render_template("error.html", error=error)

@authors_app.route("/authors_list/<int:user_id>")
def authors_lists(user_id):
    try:
        authors = data_manager.list_all_authors()
        user = data_manager.get_user(user_id)
        return render_template("authors_list.html", user_id=user_id, authors=authors, user=user)
    except Exception as error:
        return render_template("error.html", error=error)


@authors_app.route("/author/<int:user_id>/<int:author_id>/delete", methods=["GET", "POST"])
def delete_author(user_id, author_id):
    try:
        if request.method == "POST":
            author = data_manager.get_author(author_id)
            if author:
                associated_books = data_manager.assocaited_books(author_id)
                for book in associated_books:
                    data_manager.delete_book(book.book_id)
                # Delete the author
                data_manager.delete_author(author_id)
            flash(f""" The author "{author.name}" has been sucessfully deleted !""")
            return redirect(url_for("authors_app.authors_lists", user_id=user_id))
        return render_template("home.html", author_id=author_id)
    except Exception as error:
        return render_template("error.html", error=error)
