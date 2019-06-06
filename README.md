# Team BigToe
# Project Code X Lab
#### Members: Joan Chirinos (PM), Anton Danylenko, Maryann Foley, and Susan Lin
---
#### Overview
This website provides a quick and easy way for those who are new to coding to work on projects and collaborate with their peers. Since everything is run in the browser, there is no need to install extra apps and detract from the main goal of writing the code itself.

The live code editor (via ajax) provides syntax highlighting and the overall functionality of the site provides a meaningful path towards productivity.

Our project implements Google OAuth as well. In addition, as a stretch goal, we hope to send emails to users regarding project notifications and invitations etc.

A database includes tables for files, projects, permissions, and users.

---
#### Demo
[Demo placeholder](https://youtu.be/dQw4w9WgXcQ)

---
## How to Run
#### Create a Virtual Environment
__To create a venv...__
1. In a terminal, navigate to the directory you want to keep your venv (eg. `cd ~/<venv_dir>`)
2. Run `python3 -m venv <venv_name>` (replace `<venv_name>` with whatever name you'd like)
3. Activate your virtual environment by running `source <venv_name>/bin/activate`
4. Your computer's name should be preceeded by `(venv_name)` now. You are inside your virtual environment.
5. You can deactivate your venv by running the command `deactivate`
6. You can activate the venv from any current working directory by running `source ~/venv_name/bin/activate`

#### Installing Dependencies
1. If you do not have python3, install python3.6 by typing `sudo apt-get install python3.6`
2. Clone the repo
3. After activating the virtual environment,
install our __dependencies__ with `pip install -r <path-to-file>requirements.txt`


### On localhost
#### Running Our Application
1. Run `python __init__.py` to run the app on your localhost.
2. Open `localhost:5000` in a browser

## On Apache2
0. Set up an Ubuntu droplet
1. Run `$ sudo apt install apache2`, followed by `$ sudo ufw allow in "Apache Full"`
2. Run `$ sudo apt-get install libapache2-mod-wsgi-py3`
3. Clone repo into `/var/www/BigToe/`, creating directories as needed
4. Run `$ sudo apt-get install python3-pip`
5. Run `$ sudo apt install python3-flask`
6. Write the following into `/etc/apache2/sites-available/BigToe.conf`

```
<VirtualHost *:80>
                ServerName 206.81.1.145
                ServerAdmin admin@206.81.1.145
                WSGIScriptAlias / /var/www/BigToe/bigtoe.wsgi
                <Directory /var/www/BigToe/BigToe/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/BigToe/BigToe/static
                <Directory /var/www/BigToe/BigToe/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

7. Run `$ sudo a2ensite BigToe`
8. Write the following into `/var/www/BigToe/bigtoe.wsgi`

```
#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/BigToe/')
sys.path.insert(1, '/var/www/BigToe/BigToe')

from BigToe import app as application
application.secret_key = 'Add your secret key'
```

9. From `/var/www/BigToe/BigToe/`, run `$ python3 util/db.py`
10. Run `$ sudo service apache2 restart`

## OAuth
[insert Maryann]

## Dependencies
### Python 3
We are using Python 3 as our primary language to facilitate scripting and to utilize the dependencies below.
We use the following __modules__:
1. __sqlite3__ (to utilize our sqlite3 database `tuesday.db`)
2. __uuid__ (to create unique identifiers for projects and messages)
3. __json__ & __request__
