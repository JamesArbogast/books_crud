from werkzeug import datastructures
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

DATABASE_SCHEMA = 'books_db'

class Author: #pascal case -> first upper, rest lower, word is singular
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#C
    @classmethod
    def create(cls, info):
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        data = {
            "name" : info['name']
        }
        new_author_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return new_author_id

#R
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors"
        all_table_name = connectToMySQL(DATABASE_SCHEMA).query_db(query)
        all_authors = []
        for author in all_table_name:
            all_authors.append(cls(author))
        return all_table_name

    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM authors WHERE id= %(author_id)s;"
        data = {
            "author_id": id
        }
        one_table_name = connectToMySQL(DATABASE_SCHEMA).query_db(query, data) 
        return one_table_name

    @classmethod
    def get_one_by_name(cls, name):
        query = "SELECT * FROM authors WHERE name= %(name)s;"
        data = {
            "username": name
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)   
        return result

#U
    @classmethod
    def update_one(cls, info):
        query = "UPDATE authors SET name=%(name)s WHERE id=%(id)s;"
        data = {
            "name": info['name'],
            "id": info['id']
        }
        result = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return result

    @classmethod
    def show_faves(cls, id):
        query = "SELECT books.title as title, books.num_of_pages FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON favorites.author_id = authors.id WHERE authors.id=%(id)s;"
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
    def create_faves(cls, info): 
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"  
        data = {        
            "book_id" : info['book_id'],
            "author_id" : info['author_id']
        }
        new_fave_id = connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        return new_fave_id
#D
    @classmethod
    def delete_one(cls, id):
        query = "DELETE FROM authors WHERE id=%(id)s;"
        data = {
            "id": id
        }
        connectToMySQL(DATABASE_SCHEMA).query_db(query, data)
        print(f"The author with the ID:{id} has been deleted")
        return id
