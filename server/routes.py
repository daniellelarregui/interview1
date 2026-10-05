# server/routes.py

from flask import request, render_template, make_response
from server.webapp import flaskapp, cursor
from server.models import Book

@flaskapp.route('/')
def index():
    name = request.args.get('name')
    author = request.args.get('author')
    read = bool(request.args.get('read'))

    # New potentially dangerous user-controlled parameter
    search = request.args.get('search')

    if name:
        cursor.execute(
            "SELECT * FROM books WHERE name LIKE %s",
            (name,)
        )
        books = [Book(*row) for row in cursor]

    elif author:
        cursor.execute(
            "SELECT * FROM books WHERE author LIKE %s",
            (author,)
        )
        books = [Book(*row) for row in cursor]

    else:
        cursor.execute("SELECT name, author, read FROM books")
        books = [Book(*row) for row in cursor]

    # INTENTIONALLY VULNERABLE: pass tainted 'search' string directly to template
    # If the template uses it unsafely (e.g., with |safe), it becomes XSS.
    return render_template('books.html', books=books, search=search)


