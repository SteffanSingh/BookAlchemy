from datetime import datetime
import json
import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from Implementation.users_books_app import userBook_app
from Authentication.authentication import auth_app,login_manager
from data_managers.data_manager_interface_sql import SQLiteDataManager, session
from data_managers.data_models import Review, Author, Book, db
from Implementation.authors_app import authors_app
from Implementation.review_app import review_app


app = Flask(__name__)
app.register_blueprint(auth_app)
app.register_blueprint(userBook_app)
app.register_blueprint(authors_app)
app.register_blueprint(review_app)

app.secret_key = '123456'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = f'sqlite:///../data/library.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = database
db.init_app(app)
login_manager.init_app(app)

data_manager = SQLiteDataManager(app)



@app.route("/")
def home():
    """Return the list of all authors and limited books to display on homepage."""
    books = session.query(Book).limit(18)
    authors = data_manager.list_all_authors()
    return render_template("home_page.html", books=books, authors=authors)




if __name__ == "__main__":
    """To create the table in the database, we need to run these 2 lines of codes, once 
        table is creaed then we can comment these lines."""
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
