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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    '''
    Catch-all route just in case some typo or something happens
    '''
    return redirect(url_for('home'))


@app.route('/')
def home():
    '''
    Renders the homepage
    '''
    if 'email' in session:
        return redirect(url_for('projects'))
    return render_template('index.html')


@app.route('/projects')
def projects():
    '''
    Renders the main project page
    '''
    if 'email' not in session:
        return redirect(url_for('home'))
    email = str(session['email'])
    # GET PROJECTS FROM DB
    projects = db.getProjects(email)
    return render_template('projects.html', email=email, projects=projects)


@app.route('/get_files/<projectId>')
def get_files(projectId):
    '''
    Gets project files if user is signed in
    '''
    # GET FILES FROM PROJECT FROM DB
    # files = db.getFiles(projectId) # not quite there yet ;3
    # files = [file, file, file, ...]
    # file = (name, timestamp, projectid, fileid)
    return render_template('snippets/project_files.html',
                           projectId=projectId,
                           files=[('Sample Filename', 'Yesterday',
                                   'some project ID', 'some file ID')])


@app.route('/get_new_project')
def get_new_project():
    '''
    Renders new project template for injection into /projects
    '''
    return render_template('snippets/new_project.html')


@app.route('/create_new_project', methods=['POST'])
def create_new_project():
    '''
    Creates a new project in db then redirects to projects
    '''
    email = str(session['email'])
    # print("Email: ", email)
    # email = email[1:]
    # print("Email: ", email)
    name = request.form['project-name']

    db.createProject(name, email)
    db.save()

    return redirect(url_for('projects'))


@app.route('/authenticate', methods=['POST'])
def authenticate():
    '''
    Attempts to login user
    On failure, flashes and redirects home
    On success, flashes and redirects to project page
    '''
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
    '''
    Attempts to log user out, then redirects home
    '''
    if 'email' in session:
        session.pop('email')
    return redirect(url_for('home'))


@app.route('/register')
def register():
    '''
    Renders the register page if user isn't signed in
    '''
    if 'email' not in session:
        return render_template('register.html')
    return redirect(url_for('projects'))


@app.route('/register_account', methods=["POST"])
def register_account():
    '''
    Attempts to register a new account
    Flashes based on success
    Redirects to: home on success, register on failure
    '''
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
    '''
    Renders the profile template
    '''
    if 'email' not in session:
        return redirect(url_for('home'))
    email = session['email']
    return render_template('profile.html', email=email)


@app.route('/change_password', methods=['POST'])
def change_password():
    '''
    Attempts to change the current user's password
    Fails if password doesn't meet requirements
    Flashes and redirects to profile page
    '''
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


@app.route('/add_collaborator')
def add_collaborator():
    email = request.form['email']
    projectId = request.form['projectId']

    db.addCollaborator(projectId, email)
    db.save()


@app.route('/get_collaborators/<projectId>')
def get_collaborators(projectId):
    collaborators = db.getCollaborators(projectId)
    return render_template('snippets/collaborators.html',
                           collaborators=[])


@app.route('/projects/<project_id>/<file_id>')
def file(project_id, file_id):
    return render_template('file.html')


@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.form['code']

    # bleh bleh run code
    # output = something
    output = '#this is temporary output\n\t#solely for testing purposes'
    return output


if __name__ == '__main__':
    app.debug = True
    app.run()
