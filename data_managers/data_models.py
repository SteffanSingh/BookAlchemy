from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, DateTime, Text, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from flask import Flask
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()

user_book_association = db.Table(
    'user_book_association',
    db.Column('id', db.Integer, db.ForeignKey('users.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.book_id')),

)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)  # New column for admin status
    createdAt = Column(DateTime, default=datetime.now)
    profile_image = Column(String)
    book = relationship('Book', backref='users', secondary=user_book_association)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email} )"

    def __str__(self):
        return f"The user is {self.name}"


class Author(db.Model):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)
    #books = relationship('Book', backref='author')


    def __repr__(self):
        return f"author(author id={self.id}, author name = {self.name} )"

    def __str__(self):
        return f"""The author is {self.name} with birth date  {self.birth_date},\
         and was dead on {self.date_of_death} """


class Book(db.Model):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    publication_year = Column(Date)
    isbn = Column(String(13))
    book_cover = Column(Text)
    description = Column(String)
    rating = Column(Float)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship('Author', backref='books')

    # review = relationship('Review', backref='reviews',secondary=user_movie_association)

    def __repr__(self):
        return f"""Book( Book id= {self.book_id}, title= {self.title}, 
        Released year= {self.publication_year}) """

    def __str__(self):
        f"""   Book name= {self.title},  year= {self.publication_year}. """


class Review(db.Model):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    review_text = Column(String)
    rating = Column(Float)
    user = relationship('User')
    book = relationship('Book')

    def __repr__(self):
        return f"Review(review id={self.review_id}, user id={self.user_id}, book id={self.book_id}, rating = {self.rating})"

    def __str__(self):
        return f"Review(Book id={self.book_id}, user id={self.user_id}, rating = {self.rating})"



# user= User()
# print(user)
# movies = db.session.query(User).all()
# for movie in movies:
#   print(movie.movie_name)

# db.create_all()
