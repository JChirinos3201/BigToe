#! /usr/bin/python3

from flask import (Flask, render_template, redirect, url_for,
                   session, request, flash, get_flashed_messages)

from util import database

app = Flask(__name__)
app.secret_key = 'beans'

DB_FILE="data/toes.db"
user=None
data=database.DB_Manager(DB_FILE)
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

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('landing'))

    username = session['username']
    return render_template('landing.html', username = session['username'])

# @app.route('/authenticate', methods=['POST'])
# def authenticate():
#     #
    # username, password = request.form['email'], request.form['password']
    #
    # if 'submit' not in request.form:
    #     return redirect(url_for('index'))
    #
    # elif request.form['submit'] == 'Login':
    #     if len(email.strip()) != 0 and len(password.strip()) != 0 and db.verifyUser(username, password):
    #         session['username'] = username
    #         return redirect(url_for('home'))
    #     # user was found but password is incorrect
    #     elif db.findUser(username):
    #         flash('incorrect email!')
    #     # user not found in DB at all
    #     else:
    #         flash('incorrect bud!')
    # else:
    #     passwordCheck = request.form['passwordConfirmation']
    #     email = request.form['email']
    #
    #     print('\n\nREGISTERING USER\n\n')
    #     print('\n\tPassword: {}\n\tPassword Check: {}\n\tEmail: {}\n\n\n'.format(password, passwordCheck, email))
    #
    #     if password != passwordCheck:
    #         flash('Passwords don\'t match!')
    #     elif ' ' in password or len(password.strip()) == 0:
    #         flash('bad password!')
    #     elif ' ' in email or len(email.strip()) == 0 or '@' not in email or '.' not in email:
    #         flash('bad email!')
    #     else:
    #         db.registerUser(email, password)
    # return redirect(url_for('index'))



if __name__ == '__main__':
    app.debug = True
    app.run()
