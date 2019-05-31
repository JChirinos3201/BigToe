#! /usr/bin/python3

import re

from flask import (Flask, render_template, redirect, url_for,
                   session, request, flash)

from util import db

app = Flask(__name__)
app.secret_key = 'beans'


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
    return render_template('projects.html',
                           email=email,
                           projects=sorted(projects,
                                           key=lambda x: x[1].lower()))


@app.route('/get_files/<projectId>')
def get_files(projectId):
    '''
    Gets project files if user is signed in
    '''
    # GET FILES FROM PROJECT FROM DB
    # files = db.getFiles(projectId) # not quite there yet ;3
    # files = [file, file, file, ...]
    # file = (name, timestamp, projectid, fileid)
    projectName = db.getProjectName(projectId)
    return render_template('snippets/project_files.html',
                           projectName=projectName,
                           projectId=projectId,
                           files=[('sampleFilename', 'Yesterday',
                                   'sampleProjectId', 'sampleFileId')])


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
    # db.save()

    return redirect(url_for('projects'))


@app.route('/leave_project', methods=["POST"])
def leave_project():
    projectId = request.form['projectId']
    email = session['email']
    db.removeCollaborator(projectId, email)
    return 'All good!'


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
    email = str(request.form['email'])
    password = str(request.form['password'])
    password_verify = str(request.form['password-verify'])

    pass_regex_1 = re.compile('[A-Z]+')
    pass_regex_2 = re.compile('[a-z]+')
    pass_regex_3 = re.compile('[0-9]+')
    pass_regex_4 = re.compile('^[A-Za-z0-9]{6,}$')

    if pass_regex_1.search(password) and\
       pass_regex_2.search(password) and\
       pass_regex_3.search(password) and\
       pass_regex_4.search(password) and\
       password == password_verify:
        if db.registerUser(email, password):
            flash('Successfully registered. You may now log in', "success")
            return redirect(url_for('home'))
        else:
            flash('Email already registered', "danger")
            return redirect(url_for('register'))
    else:
        flash('Invalid password', "danger")
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

    if pass_regex_1.search(password) and\
       pass_regex_2.search(password) and\
       pass_regex_3.search(password) and\
       pass_regex_4.match(password) and\
       password == password_verify:
        db.changePassword(email, password)
        # db.save()
        flash('Successfully changed password!')
    elif password == password_verify:
        flash('Invalid password')
    else:
        flash('Passwords do not match')
    return redirect(url_for('profile'))


@app.route('/add_collaborator', methods=['POST'])
def add_collaborator():
    email = request.form['email']
    projectId = request.form['projectId']

    if db.addCollaborator(projectId, email):
        return 'heh we good ;3'
    else:
        return 'bruh thats not a user!'


@app.route('/get_collaborators/<projectId>')
def get_collaborators(projectId):
    collaborators = db.getCollaborators(projectId)
    return render_template('snippets/collaborators.html',
                           collaborators=collaborators)


@app.route('/projects/<projectId>/<fileId>')
def file(projectId, fileId):
    print(projectId)
    print(fileId)
    # filename = db.getFilename(fileId)
    # code = db.getCode(fileId)
    # projectName = db.getPname(projectId)
    return render_template('file.html', filename='sampleFilename',
                           code='#sample content\ndef foo():\n\treturn 5',
                           projectName='sampleProjectName')


@app.route('/get_code/<fileId>')
def get_code(fileId):
    return db.getCode(fileId)


@app.route('/run_code', methods=['POST'])
def run_code():
    # code = request.form['code']

    # bleh bleh run code
    # output = something
    output = '#this is temporary output\n\t#solely for testing purposes'
    return output


@app.route('/add_file', methods=["POST"])
def add_file():
    filename = request.form['filename']
    projectId = request.form['projectId']

    db.addFile(filename, projectId)
    # db.save()


if __name__ == '__main__':
    app.debug = True
    app.run()
