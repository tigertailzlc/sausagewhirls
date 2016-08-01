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

