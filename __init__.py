#! /usr/bin/python3

from flask import (Flask, render_template, redirect, url_for,
                   session, request, flash, get_flashed_messages)

from util import database

app = Flask(__name__)
app.secret_key = 'beans'

DB_FILE="data/toes.db"
user=None
data=database.DB_Manager()
data.createUsersTable()
data.save()

#Sets the user variable to the username
#replace with a session variable????
def setUser(uname):
    global user
    user=uname

@app.route('/')
def landing():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
