from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_author import Author
from flask_app.models.model_book import Book

@app.route('/books')
def all_books():
    context = {
        "all_books" : Book.get_all()
    }
    return render_template('new_book.html', **context)

@app.route('/books/create', methods=['POST'])
def book_create():
    print(request.form)
    Book.create(request.form)
    return redirect('/books')

@app.route('/books/<int:id>')
def show_book(id):
    book = Book.get_one(id)[0]
    authors = Author.get_all()
    faves = Book.show_book_faves(id)
    context = { 
        "book" : book,
        "all_faves" : faves,
        "all_authors" : authors
    }
    return render_template('show_book.html', **context)

@app.route('/book/<int:id>/add_fave', methods=['POST'])
def book_add_fave(id): 
    author_id = request.form['author_id']
    book_id =  Book.get_one(id)[0] 
    info = {
        "author_id" : author_id,
        "book_id" : book_id['id']
    }
    Book.create_book_faves(info)
    return redirect(f'/books/{book_id["id"]}')