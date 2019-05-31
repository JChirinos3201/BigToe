import uuid

import sqlite3

DB_FILE = 'data/toes.db'

# for running (?)
# DB_FILE = '/var/www/BigToe//BigToe/data/toes.db'


def create_db():
    '''
    Creates the tables in the DB file
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, \
              password TEXT)')

    c.execute('CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, \
              name TEXT)')

    c.execute('CREATE TABLE IF NOT EXISTS permissions(id TEXT, email TEXT)')

    c.execute('CREATE TABLE IF NOT EXISTS files(projectId TEXT, \
              fileId TEXT PRIMARY KEY, filename TEXT, content TEXT)')

    db.commit()
    db.close()

    return True


# =================== user fxns ====================


def getUsers():
    '''
    Returns a dict of users and passwords
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT email, password FROM users')
    tuples = c.fetchall()
    d = dict(tuples)
    return d


def registerUser(email, password):
    '''
    Registers user given email and password
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if email in getUsers():
        return False
    c.execute('INSERT INTO users VALUES(?, ?)', (email, password))
    db.commit()
    db.close()
    return True


def verifyUser(email, password):
    '''
    Checks if email and password in DB
    '''
    users = getUsers()
    if email in users and users[email] == password:
        return True
    return False


def changePassword(email, new_password):
    '''
    Changes the row in users to reflect a new password
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if email not in getUsers():
        return False
    c.execute('UPDATE users SET password=? WHERE email=?',
              (new_password, email))
    db.commit()
    db.close()
    return True


# ==================== project fxns ====================


def getProjects():
    '''
    Returns a dict of all ids and projects
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT id, name FROM projects')
    tuples = c.fetchall()
    d = dict(tuples)
    return d


def getProjectName(projectId):
    '''
    Returns the name of a project given an id
    '''
    return getProjects().get(projectId, None)


def createProject(name, email):
    '''
    Creates a new project, and adds a user to the permissions table
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    id = str(uuid.uuid4())

    # make sure we don't have a duplicate id (unlikely, but possible)
    all_ids = getProjects().keys()
    while id in all_ids:
        id = str(uuid.uuid4())

    c.execute('INSERT INTO projects VALUES(?, ?)', (id, name))
    c.execute('INSERT INTO permissions VALUES(?, ?)', (id, email))
    db.commit()
    db.close()
    return True


# ==================== permission fxns ====================


def getPermissions():
    '''
    Return tuples of projectIds and emails
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT id, email FROM permissions')
    t = c.fetchall()
    return t


def findProjects(email):
    '''
    Return list of all projectIds user can access
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT id FROM permissions WHERE email=?', (email,))
    t = [x[0] for x in c.fetchall()]  # gets ids sans tuples
    return t


def addCollaborator(projectId, email):
    '''
    Gives user access to a project
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if projectId in findProjects(email):
        return False
    c.execute('INSERT INTO permissions VALUES(?, ?)', (projectId, email))
    db.commit()
    db.close()
    return True


def removeCollaborator(projectId, email):
    '''
    Revokes user access to a project
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('DELETE FROM permissions WHERE email=?', (email,))
    db.commit()
    db.close()


def getCollaborators(projectId):
    '''
    Returns a list of all collaborators to a project
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT email FROM permissions WHERE id=?', (projectId,))
    email_list = [x[0] for x in c.fetchall()]
    return email_list


# ==================== file fxns ====================


def getFiles(projectId):
    '''
    Returns a list of tuples of all files associated with a project
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT fileId, filename, content FROM files WHERE projectId=?',
              (projectId,))
    t = c.fetchall()
    return t


def addFile(filename, projectId):
    '''
    Adds a new file given a projectId
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    fileId = str(uuid.uuid4())

    # make sure there are no duplicate file ids (unlikely, but possible)
    currentIds = [x[0] for x in getFiles()]
    while fileId in currentIds:
        fileId = str(uuid.uuid4())

    c.execute('INSERT INTO files VALUES(?, ?, ?, ?)',
              (projectId, fileId, filename, ''))
    db.commit()
    db.close()
    return True


def getFilename(fileId):
    '''
    Returns filename given fileId
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT name FROM files WHERE fileId=?', (fileId,))
    tuple = c.fetchall()
    if tuple == []:
        return False
    return tuple[0][0]


def getCode(fileId):
    '''
    Returns the code stored in a file given the fileId
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT content FROM files WHERE fileId=?', (fileId,))
    tuple = c.fetchall()
    if tuple == []:
        return False
    return tuple[0][0]


def updateCode(fileId, patches):
    '''
    Updates code given patches to apply
    '''
    pass
