from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date,Text
from sqlalchemy.orm import declarative_base, sessionmaker,relationship
from flask import Flask

db = SQLAlchemy()


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

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    publication_year = Column(Date)
    isbn = Column(String(13))
    book_cover= Column(Text)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship('Author', backref='books')



    def __repr__(self):
        return f"""Book(book id= {self.book_id}, title= {self.title}, publication year= {self.publication_year}
                    isbn= {self.isbn}) """

    def __str__(self):
        f"""Book(  title= {self.title}, publication year= {self.publication_year}

                            isbn= {self.isbn}) """

#db.create_all()