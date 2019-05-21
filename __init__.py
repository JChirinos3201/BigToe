#! /usr/bin/python3

import re

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
db.createUsersTable()
db.createProjectIDTable()
db.createPermissionsTable()
db.save()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/projects')
def projects():
    if 'email' not in session:
        return redirect(url_for('home'))
    email = session['email']
    # GET PROJECTS FROM DB
    projects = None
    return render_template('projects.html', email=email, projects=[('69696969', 'projectName')])


@app.route('/get_files/<projectId>')
def get_files(projectId):
    # GET FILES FROM PROJECT FROM DB
    files = None
    # files = [file, file, file, ...]
    # file = (name, timestamp, projectid, fileid)
    return render_template('snippets/project_files.html', files=[('sample filename', '6 days ago', projectId, '420blazeit')])


@app.route('/get_new_project')
def get_new_project():
    return render_template('snippets/new_project.html')


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


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
    return redirect(url_for('home'))


@app.route('/register')
def register():
    if 'email' not in session:
        return render_template('register.html')
    return redirect(url_for('projects'))


@app.route('/register_account', methods=["POST"])
def register_account():
    email = request.form['email']
    password = request.form['password']
    password_verify = request.form['password-verify']

    if db.findUser(email):
        flash('Email already registered')
        return redirect(url_for('register'))

    pass_regex_1 = re.compile('[A-Z]+')
    pass_regex_2 = re.compile('[a-z]+')
    pass_regex_3 = re.compile('[0-9]+')
    pass_regex_4 = re.compile('^[A-Za-z0-9]{6,}$')

    if pass_regex_1.search(password) and\
       pass_regex_2.search(password) and\
       pass_regex_3.search(password) and\
       pass_regex_4.search(password) and\
       password == password_verify:
        db.registerUser(email, password)
        db.save()
        flash('Successfully registered. You may now log in')
        return redirect(url_for('home'))
    else:
        flash('Invalid password')
        return redirect(url_for('register'))


@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('home'))
    email = session['email']
    return render_template('profile.html', email=email)


@app.route('/change_password', methods=['POST'])
def change_password():
    if 'email' not in session:
        return redirect(url_for('home'))

    email = session['email']
    password = request.form['password']
    password_verify = request.form['password-verify']

    pass_regex_1 = re.compile('[A-Z]+')
    pass_regex_2 = re.compile('[a-z]+')
    pass_regex_3 = re.compile('[0-9]+')
    pass_regex_4 = re.compile('^[A-Za-z0-9]{6,}$')

    if pass_regex_1.match(password) and\
       pass_regex_2.match(password) and\
       pass_regex_3.match(password) and\
       pass_regex_4.match(password) and\
       password == password_verify:
        db.changePassword(email, password)
        db.save()
        flash('Successfully changed password!')
    elif password == password_verify:
        flash('Invalid password')
    else:
        flash('Passwords do not match')
    return redirect(url_for('profile'))



if __name__ == '__main__':
    app.debug = True
    app.run()
