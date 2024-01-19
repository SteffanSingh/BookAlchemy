from flask import Flask,  render_template, request,redirect,url_for
from  flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
import  requests, json
import re
from datetime import date

from sqlalchemy import create_engine, Column, Integer,String, ForeignKey,join
from sqlalchemy.orm import declarative_base, sessionmaker, joinedload
from datetime import  datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Base = declarative_base()

engine = create_engine('sqlite:///library.sqlite3')
Base.metadata.create_all(engine)

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
db.init_app(app)


@app.route("/")
def home():
    books = session.query(Book).all()
    authors = session.query(Author).all()
    #combine_table = session.query(Book, Author).\
     #                join(Author, Book.title).\
      #              filter(Book.title == Author.name).all()

    return  render_template("home.html", books = books, authors=authors, Author=Author )


@app.route("/add_author", methods = ["GET", "POST"])
def author_add():
    if request.method =="POST":
        name = request.form.get("name")
        birthdate= request.form.get("birthdate")
        date_of_death = request.form.get("date_of_death")
        print(name, birthdate)
        #Instantiating the author class
        author = Author(
            name = name,
            birth_date = datetime.strptime(birthdate, "%Y-%m-%d"),
            date_of_death = datetime.strptime(date_of_death, "%Y-%m-%d")
        )
        session.add(author)
        session.commit()
        return render_template("success_author.html")
    return render_template("add_author.html")

def get_isbn(title):
    google_books_api_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{title}"
    response = requests.get(google_books_api_url)
    data = response.json()
    response_content= response.content
    data = json.loads(response_content.decode('utf-8'))

    if "items" in data and len(data["items"]) > 0:
        book_info = data["items"][0]["volumeInfo"]
        author_name = book_info.get('authors', ['N/A'])
        cover_image_url = book_info.get('imageLinks', {}).get('thumbnail', 'N/A')
        isbn = data['items'][0].get('id', 'N/A')  # ISBN is assumed to be in the 'id' field
        authors_info = book_info.get('authors', [])
        publication_year = book_info.get('publishedDate', 'N/A')

        # Extract birth and death dates from the author information response


        #for author_name in authors_info:

        return  isbn,cover_image_url, author_name, publication_year
    return None


@app.route("/add_book", methods=["GET", "POST"])
def book_add():
    if request.method == "POST":
        title = request.form.get("title")
        publication_year_data = get_isbn(title)[3]
        publication_year_form = request.form.get("publication_year")
        isbn = get_isbn(title)[0]
        book_cover_image = get_isbn(title)[1]
        author_names = get_isbn(title)[2]
        print(author_names)
        author_name = request.form.get("author")
        #author_death_date = get_isbn(title)[4]
       # author_birth_date = get_isbn(title)[3]
        #print(datetime.strptime(publication_year, "%Y-%m-%d"),)
        author_info_api_url = f"https://en.wikipedia.org/wiki/{author_names[0].replace(' ', '_')}"
        response = requests.get(author_info_api_url)
        if Author.name not in author_names:
            author = Author(
                name=author_names[0],
                birth_date= None,
                date_of_death=None
            )
            session.add(author)
            session.commit()
            author_id = author.id

        else:
            author_id = session.query(Author).filter(Author.name == author_name ).one().id
        print(publication_year_data)
        print(type(publication_year_data))

        if publication_year_data:
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

        #Instantiating the book class
        book = Book(
            title=title,
            publication_year = publication_year ,
            isbn =  isbn,
            author_id= author_id,
            book_cover= book_cover_image
        )

        session.add(book)
        session.commit()
        return render_template("success_book.html")

    authors = session.query(Author).all()

    return  render_template("add_book.html", authors=authors)


@app.route("/book_sort")
def sort_book():
    books = session.query(Book).\
            order_by(Book.title.asc()).all()

    authors = session.query(Author).all()
    # combine_table = session.query(Book, Author).\
    #                join(Author, Book.title).\
    #              filter(Book.title == Author.name).all()

    return render_template("sorted_book_home.html", books=books, authors=authors, Author=Author)




@app.route("/author_sort")
def sort_author():
    books = session.query(Book). \
        join(Author). \
        options(joinedload(Book.author)). \
        order_by(Author.name.asc()).all()
    authors = session.query(Author).all()
    return render_template("sorted_book_home.html", books=books, authors=authors, Author=Author)


@app.route("/book/<int:book_id>/delete",methods= ["GET","POST"])
def delete_book(book_id):
    if request.method == "POST":

        session.query(Book).filter(Book.id == book_id).delete()

        return redirect(url_for("home"))

    return render_template("home.html", book_id=book_id)





@app.route("/author/<int:author_id>/delete",methods= ["GET","POST"])
def delete_author(author_id):
    if request.method == "POST":
        author = session.query(Author).get(author_id)
        if author:
            associated_books = session.query(Book).filter(Book.author_id == author_id).all()

            for book in associated_books:
                session.delete(book)

            # Delete the author
            session.delete(author)
            session.commit()

        return redirect(url_for("home"))

    return render_template("home.html", author_id=author_id)

#Keyword search
@app.route("/search" , methods=["GET","POST"])
def search():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        books = session.query(Book).all()
        book_data = session.query(Book).filter(Book.title.like(f"%{keyword}%")).all()

        if book_data:
            return render_template("search_result.html", keyword=keyword, books=book_data)
        else:
            return render_template("no_result.html")

    books = session.query(Book).all()
    authors = session.query(Author).all()
    return   render_template("home.html", books = books, authors=authors, Author=Author )


if __name__ == "__main__":
    #with app.app_context():
     #  db.create_all()

    app.run(host="0.0.0.0", port=5000)



