# -*- coding: utf-8 -*-
"""
    Sausage
    ~~~~~~~
    Purty intro goes here 
"""

import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash 

# ZLC: I'm changing all instances of "flaskr" to "sausage" :) 


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sausage.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('SAUSAGE_SETTINGS', silent=True)

# ZLC: Why is there a dict after app.config.update? In the documentation, 
# http://flask.pocoo.org/docs/0.11/config/ 
# the update method is a method from the dict object anyway..?? I dun geddit 

# Also what precisely is that SECRET_KEY doing 

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# ZLC: PLEASE REMEMBER THAT YOU MADE THIS CHANGE ("initdbYO") 
# lest you sabotage yourself later lel 
@app.cli.command('initdbyo')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database. Whooop de dooo dooo.'

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# VIEW FUNCTIONS 


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



# This is where I have no idea what I'm doing, but I'm trying to 
# deploy to Heroku. Have read Procfile documentation but understanding 
# of Flask and Heroku in tandem still very hazy; therefore will simply 
# make my lil dyno run python sausage.py and see what happens 

# But for that to happen I have to have the main function 
# so here goes 

if __name__ == "__main__": 
    #I have to initialize the database first, right? 
    #But instead of using the CLI I'll just run the fn directly: 
    init_db()
    print 'Initialized the database. Whooop de dooo dooo.'
    #let's try screwing with this. Having read Python 2.7 os documentation, 
    #replacing os.environ.get with os.getenv. 
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# Let's see how that goes... 
