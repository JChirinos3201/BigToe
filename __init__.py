#! /usr/bin/python3

from flask import (Flask, render_template, redirect, url_for,
                   session, request, flash, get_flashed_messages)

from util import database

app = Flask(__name__)
app.secret_key = 'beans'

# for testing
DB_FILE = "data/toes.db"

# for running
# DB_FILE = "/var/www/BigToe/BigToe/data/toes.db"

db = database.DB_Manager(DB_FILE)
data.createUsersTable()
data.save()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/projects')
def projects():
    if 'email' not in session:
        return redirect(url_for('home'))
    username = session['username']
    return render_template('projects.html', username=username)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    email, password = request.form['email'], request.form['password']
    if len(email.strip()) != 0\
       and len(password.strip()) != 0\
       and db.verifyUser(email, password):
        session['email'] = email
        return redirect(url_for('projects'))
    # user was found but password is incorrect
    else:
        flash('Incorrect email or password!')
        return redirect(url_for('home'))


@app.route('/register')
def register():
    if 'email' not in session:
        return render_template('register.html')
    return redirect(url_for('landing'))


@app.route('/register_account', methods=["POST"])
def register_account():



if __name__ == '__main__':
    app.debug = True
    app.run()
