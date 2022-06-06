from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'
app.database = 'sample.db'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

def connect_db():
    return sqlite3.connect(app.database)

@app.route('/')
@login_required
def home(error = None):
    with connect_db() as db:
        cur = db.execute('select id, name, description from items')
        items = [dict(id=row[0], name=row[1], description=row[2]) for row in cur.fetchall()]
    return render_template('index.html', items=items, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('home'))

@app.route('/add_item', methods=['POST'])
@login_required
def add_item():
    error = None
    if request.form['name'] != '' and request.form['description'] != '' and len(request.form) == 2:
        with connect_db() as db:
            name = request.form['name']
            description = request.form['description']
            db.execute(f'INSERT INTO items(name, description) VALUES("{name}", "{description}")')
    else:
        error = 'Invalid new Item. Please try again.'
    return home(error)

if __name__ == '__main__':
    app.run(debug=True)
