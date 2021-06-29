from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

DATABASE_SCHEMA = 'books_db'

class Book: #pascal case -> first upper, rest lower, word is singular
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#C
    @classmethod
    def create(cls, info):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s)"
        data = {
            "title" : info['title'],
            "num_of_pages" : info['num_of_pages']
        }
        new_book_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return new_book_id

#R
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books"
        all_table_name = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        all_books = []
        for book in all_table_name:
            all_books.append(cls(book))
        return all_table_name

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM books WHERE id= %(book_id)s;"
        data = {
            "book_id": id
        }
        one_table_name = connectToMySQL(DATABASE_SCHEMA).query_db(query, data) 
        return one_table_name

    @classmethod
    def get_one_by_title(cls, title):
        query = "SELECT * FROM books WHERE title= %(title)s;"
        data = {
            "title": title
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)   
        return result

#U
    @classmethod
    def update_one(cls, info):
        query = "UPDATE books SET title=%(title)s WHERE id=%(id)s;"
        data = {
            "title": info['title'],
            "num_of_pages" : info['num_of_pages'],
            "id": info['id']
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return result

    @classmethod
    def show_book_faves(cls, id):
        query = "SELECT  authors.name as name FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON favorites.book_id = books.id WHERE books.id=%(id)s;"
        data = {
            "id": id
        }
        favorites =  connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        all_faves = []
        for fave in favorites:
            all_faves.append(fave)
            print(all_faves)
        return favorites
    
    @classmethod
    def create_book_faves(cls, info): 
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        data = {
            "author_id" : info['author_id'],
            "book_id" : info['book_id']
        }
        new_fave_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return new_fave_id
#D
    @classmethod
    def delete_one(cls, id):
        query = "DELETE FROM books WHERE id=%(id)s;"
        data = {
            "id": id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        print(f"The book with the ID:{id} has been deleted")
        return id
