#! /usr/bin/python3

from flask import (Flask, render_template, redirect, url_for,
                   session, request, flash, get_flashed_messages)

from util import db

app = Flask(__name__)
app.secret_key = 'beans'


@app.route('/')
def landing():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
