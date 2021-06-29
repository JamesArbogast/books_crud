from flask.wrappers import Request
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_author import Author
from flask_app.models.model_book import Book

@app.route('/authors')
def all_authors():
    context = {
        "all_authors" : Author.get_all()
    }
    return render_template('new_author.html', **context)

@app.route('/authors/create', methods=['POST'])
def author_create():
    print(request.form)
    Author.create(request.form)
    return redirect('/authors')

@app.route('/authors/<int:id>')
def show_author(id):
    author = Author.get_one(id)[0]
    books = Book.get_all()
    faves = Author.show_faves(id)
    context = { 
        "all_books" : books,
        "all_faves" : faves,
        "author" : author
    }
    print(faves)
    return render_template('show_author.html', **context)

@app.route('/author/<int:id>/add_fave', methods=['POST'])
def author_add_fave(id): 
    book_id = request.form['book_id']
    id =  Author.get_one(id)[0]  
    info = {    
        "book_id" : book_id, 
        "author_id" : id['id']
    }
    Author.create_faves(info)
    return redirect(f'/authors/{id["id"]}')
