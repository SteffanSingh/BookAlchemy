from flask import Flask, request, flash, render_template, redirect, url_for, Blueprint
from data_managers.data_manager_interface_sql import session, SQLiteDataManager, database
from data_managers.data_models import User, Author, Book,Review
from Implementation.reusable_funciton import get_book_details
import  requests
from datetime import datetime

review_app = Blueprint("review_app", __name__)

data_manager = SQLiteDataManager(review_app)


@review_app.route("/add_review/<int:user_id>/<int:book_id>", methods=["GET", "POST"])
def add_review(user_id, book_id):
    """function to add the review for a particular user id and movie id:"""
    try:
        reviews_book = data_manager.list_all_reviews(book_id)
        user = data_manager.get_user(user_id)
        book_to_review = data_manager.get_book(book_id)
        review_dict = {
            "book_id": book_id,
            "user_id": user_id,
            "book": book_to_review,
            "reviews": reviews_book
        }
        book = book_to_review
        reviews = reviews_book
        if request.method == "POST":
            review = request.form['review']
            rating = request.form['rating']
            if review == "":
                flash("Please enter your review")
                return redirect(url_for("add_review", user_id=user_id, book_id=book_id))

            new_review = Review(
                review_text=review if review else None,
                rating=float(rating) if rating else 0,
                user=user,
                book=book_to_review
            )
            data_manager.add_review(new_review)
            return redirect(url_for("userBook_app.bookDetail", user_id=user_id, book_id=book_id))
        return render_template("add_review.html", review_dict=review_dict, book=book_to_review,
                               reviews=reviews_book)
    except Exception as error:
        print(error)
        return render_template("error.html", error=error)

@review_app.route("/review_delete/<int:review_id>")
def delete_review(review_id):
    """function to implement the deletion of particular review"""
    try:
        review_to_delete = data_manager.get_review(review_id)
        if review_to_delete:
            data_manager.delete_review(review_to_delete)
            return redirect(url_for("userBook_app.bookDetail", user_id=review_to_delete.user_id, book_id=review_to_delete.book_id))
    except Exception as error:
        return render_template("error.html", error=error)


