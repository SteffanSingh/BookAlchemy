from flask import Flask, request, flash, render_template, redirect, url_for, Blueprint
from data_managers.data_manager_interface_sql import session, SQLiteDataManager, database
from data_managers.data_models import User, Author, Book
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt


auth_app = Blueprint('auth_app', __name__)
login_manager = LoginManager()
data_manager = SQLiteDataManager(auth_app)

app = Flask(__name__)
bcrypt = Bcrypt(app)




def check_passwrod(password, hashed_password):
    user_password = password
    pw_is_match = bcrypt.check_password_hash(hashed_password, user_password)
    return pw_is_match


def encrypt_password(user_password):
    hashed_password = bcrypt.generate_password_hash(user_password).decode("utf-8")
    return hashed_password


@login_manager.user_loader
def load_user(user_id):
    user = data_manager.get_user(user_id)
    if user:
        return user
    else:
        return None

@auth_app.route("/logout")
def logout():
    logout_user()
    flash("You are logged out")
    books = session.query(Book).limit(18)
    authors = data_manager.list_all_authors()
    return render_template("home_page.html", books=books, authors=authors)



@auth_app.route("/signup", methods=["GET", "POST"])
def signup():
    """The function to implement the signup component for registration. """
    try:
        if request.method == "POST":
            name = request.form.get("firstName")
            email = request.form.get("email")
            password = request.form.get("password")
            if not name:
                flash("Please enter your name")
                return redirect(url_for("auth_app.signup"))
            if len(name) > 20:
                flash("Enter your first and last name only.Name cant be more than 20 characters!")
                return redirect(url_for("auth_app.signup"))

            existing_user = data_manager.user_by_email(email)
            if existing_user:
                flash("Email is already registered!")
                return redirect(url_for("auth_app.signup"))
            if not password:
                flash("Enter your password!")
                return redirect(url_for("auth_app.signup"))
            if len(password) < 6:
                flash("Password should have minimum 6 characters!")
                return redirect(url_for("auth_app.signup"))
            hashed_password = encrypt_password(password)
            if email and password:
                user = User(
                    name=name.title(),
                    email=email,
                    password=hashed_password,
                    book=[]
                )
                data_manager.add_user(user)
                flash("Signup successful! Login to access book library. ")
                return redirect(url_for("auth_app.signin"))
            else:
                flash("Email or password cant be blank!")
                return redirect(url_for("auth_app.signup"))
        return render_template("signup.html")
    except Exception as error:
        print(error)
        return render_template("error.html", error=error)


# Login Route
@auth_app.route("/login", methods=["GET", "POST"])
def signin():
    try:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form.get("password")
            user = data_manager.user_by_email(email)
            if not user:
                flash("Email is not registered yet")
                return redirect(url_for("auth_app.signin"))
            password_match = check_passwrod(password, user.password)
            if user and not password_match:
                flash("Password is incorrect! Try again.")
                return redirect(url_for("auth_app.signin"))

            user_dict = {
                "user_name": user.name,
                "books": user.book,
                "user_id": user.id
            }
            authors = data_manager.list_all_authors()
            flash("Login successful! Welcome to Book Library!")
            return redirect(url_for("userBook_app.user_books", user_id = user.id))
        return render_template("login.html")
    except Exception as e:
        flash("An error occurred.")
        print(e)
        return render_template("error.html")


# Logout Route

@auth_app.route("/resetPassword", methods=["GET", "POST"])
def resetPassword():
    try:
        users = data_manager.list_all_users()
        emails = [user.email for user in users]
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            hashed_password = encrypt_password(password)
            if email == "" or password == "":
                flash("Email and password cant be blank!")
                return redirect(url_for("auth_app.resetPassword"))
            if len(password) < 6:
                flash("Password should have minimum 6 characters !")
                return redirect(url_for("auth_app.resetPassword"))
            if email in emails:
                user = data_manager.user_by_email(email)
                user.password = hashed_password
                data_manager.commit_change()
                flash("Reset Password successful")
                return redirect(url_for("auth_app.signin"))
            else:
                flash("Email is not registered yet ! Please Register.")
                return redirect(url_for("auth_app.signup"))
        return render_template("forgot_password.html")
    except Exception as error:
        return render_template("error.html", error=error)
