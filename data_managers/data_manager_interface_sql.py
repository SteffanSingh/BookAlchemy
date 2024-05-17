import json
import os
from .data_manager_interface import DataManagerInterface
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import declarative_base, sessionmaker, joinedload
from flask import Flask
from data_managers.data_models import User, Book, Author, Review, user_book_association
from .data_models import db
from flask_sqlalchemy import SQLAlchemy



database = f"sqlite:///./data/library.sqlite3"
Base = declarative_base()
engine = create_engine(database)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        self.db = db  # db = SQLAlchemy()

    def list_all_users(self):
        # Return all the users all users
        users = db.session.query(User).all()
        if users:
            return users
        else:
            return []

    def list_user_books(self, user_id):
        user = db.session.query(User).get(user_id)
        if user:
            books = user.book
            if books:
                return books
            else:
                return []
        else:
            return None

    def add_user(self, user):
        db.session.add(user)
        db.session.commit()

    def delete_user(self, user_id):
        try:
            user = db.session.query(User).get(user_id)
            db.session.query(user_book_association).filter_by(id=user_id).delete()
            db.session.delete(user)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return error

    def get_user(self, user_id):
        user = db.session.query(User).get(user_id)
        if user:
            return user
        else:
            return None

    def list_all_authors(self):
        # Return all the users all users
        authors = db.session.query(Author).all()
        if authors:
            return authors
        else:
            return []

    def get_author(self, author_id):
        book = db.session.query(Author).get(author_id)
        if book:
            return book
        else:
            return None

    def get_book(self, book_id):
        book = db.session.query(Book).get(book_id)
        if book:
            return book
        else:
            return None

    def add_book(self, book):
        books = db.session.query(Book).all()
        db.session.add(book)
        db.session.commit()

    def add_author(self, author):
        db.session.add(author)
        db.session.commit()

    def update_movie(self, movie):
        db.session.commit()

    def commit_change(self):
        db.session.commit()

    def delete_book(self, book_id):
        books = db.session.query(Book).all()
        book = db.session.query(Book).get(book_id)
        if book:
            db.session.delete(book)
            db.session.commit()
        else:
            raise ValueError("Book not found")

    def assocaited_books(self,author_id):
        books_with_author_id = db.session.query(Book).filter(Book.author_id == author_id).all()
        return books_with_author_id


    def delete_author(self, author_id):
        author = db.session.query(Author).get(author_id)
        if author:
            db.session.delete(author)
            db.session.commit()
        else:
            raise ValueError("Author not found")

    def author_by_name(self, author_name):
        author= db.session.query(Author).filter_by(name=author_name).first()
        if author:
            return author.id
        else:
            return None
    def remaining_assocaition(self,user_id, book_id):
        remaining_associations = db.session.query(user_book_association).filter(
            user_book_association.c.id == user_id,
            user_book_association.c.book_id == book_id
        ).first()
        return  remaining_associations

    def book_exist_or_not(self, book_name):
        existing_book = db.session.query(Book).filter_by(title = book_name).first()
        return existing_book

    def author_exist_or_not(self, author_name):
        existing_book = db.session.query(Author).filter_by(name = author_name).first()
        if existing_book:
            return existing_book
        else:
            return None
    def user_by_email(self, email_check):
        user = db.session.query(User).filter_by(email=email_check).first()
        if user:
            return user
        else:
            None

    def sort_by_book_title_ascending(self, user_id):
        #users_sorted_list =sorted_books = db.session.query(Book).join(user_book_association).join(User).filter(User.id == user_id).order_by(Book.title.asc()).all()
        sorted_book_list = db.session.query(Book).join(User.book).filter(User.id == user_id). \
                                        order_by(Book.title.asc()).all()
        user = db.session.query(User).get(user_id)
        if user.book:
            return sorted_book_list
        else:
            return []

    def sort_by_authors_ascending(self, user_id):
        #user_sorted_books= sorted_books = db.session.query(Book).join(user_book_association).join(User).filter(User.id == user_id).order_by(Book.author.name.asc()).all()
        sorted_book_list = db.session.query(Book).join(user_book_association).join(User).join(Author).filter(
            User.id == user_id).order_by(Author.name.asc()).all()
        user = db.session.query(User).get(user_id)
        if user.book:
            return sorted_book_list
        else:
            return []


    def search_book(self, user_id, keyword):
        search_books_list = db.session.query(Book).join(Book.author). \
            filter(or_(Book.title.like(f"%{keyword}%"), Author.name.like(f"%{keyword}%"))).all()
        search_books_list = db.session.query(Book).join(User.book).join(Book.author). \
                                filter(User.id == user_id). \
                                filter(or_(
                                    Book.title.ilike(f"%{keyword}%"),
                                    Book.isbn.ilike(f"%{keyword}%"),
                                    Book.publication_year.ilike(f"%{keyword}%"),
                                    Author.name.ilike(f"%{keyword}%")
                                    )).all()
        return search_books_list


    def list_all_reviews(self, book_id):
        reviews = db.session.query(Review).filter(Review.book_id == book_id).all()
        if reviews:
            return reviews
        else:
            return []


    def add_review(self, review):
        db.session.add(review)
        db.session.commit()


    def get_review(self, review_id):
        review = db.session.query(Review).get(review_id)
        return review


    def delete_review(self, review):
        db.session.delete(review)
        db.session.commit()

