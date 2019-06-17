import uuid
import datetime

import sqlite3

#DB_FILE = 'data/toes.db'

DB_FILE = '/var/www/codexlab/codexlab/data/toes.db'


def create_db():
    '''
    Creates the tables in the DB file
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY, \
              password TEXT)')

    c.execute('CREATE TABLE IF NOT EXISTS google(email TEXT PRIMARY KEY)')

    c.execute('CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, \
              name TEXT)')

    c.execute('CREATE TABLE IF NOT EXISTS drivers(fileId TEXT, \
                        driver TEXT, times REAL)')

    c.execute('CREATE TABLE IF NOT EXISTS permissions(id TEXT, email TEXT)')

    c.execute('CREATE TABLE IF NOT EXISTS files(projectId TEXT, \
              fileId TEXT PRIMARY KEY, filename TEXT, content TEXT,\
              times REAL)')

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

# =================== google fxns ====================


def getGUsers():
    '''
    Returns a dict of G users
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT email FROM google')
    tuples = c.fetchall()
    ret=[]
    for t in tuples:
        ret.append(t[0])
    #d = list(tuples)
    return ret


def registerGUser(email):
    '''
    Registers G user given email
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if email in getGUsers():
        return False
    c.execute('INSERT INTO google VALUES(?)', (email))
    db.commit()
    db.close()
    return True


def verifyGUser(email):
    '''
    Checks if email and password in DB
    '''
    users = getGUsers()
    if email in users:
        return True
    return False



# ==================== project fxns ====================


def getProjectIds():
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
    return getProjectIds().get(projectId, None)


def createProject(name, email):
    '''
    Creates a new project, and adds a user to the permissions table
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    id = str(uuid.uuid4())

    # make sure we don't have a duplicate id (unlikely, but possible)
    all_ids = getProjectIds().keys()
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
    if email not in getUsers():
        # print("User doesn't exist") #Flash this to user somehow
        return False
    if projectId in findProjects(email):
        # print("User already added") #Flash this to user somehow
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
    c.execute('DELETE FROM permissions WHERE id=? AND email=?',
              (projectId, email))
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


def getProjects(email):
    '''
    Returns a list of tuples for each project
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT id, name FROM projects')
    projects = c.fetchall()

    c.execute('SELECT id FROM permissions WHERE email=?', (email,))
    ids = [x[0] for x in c.fetchall()]

    projects = list(filter(lambda x: x[0]in ids, projects))

    return projects


# ==================== file fxns ====================


def getFiles(projectId):
    '''
    Returns a list of tuples of all files associated with a project
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT fileId, filename, content, times FROM files\
              WHERE projectId=?', (projectId,))
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
    currentIds = [x[0] for x in getFiles(projectId)]
    while fileId in currentIds:
        fileId = str(uuid.uuid4())

    t = datetime.datetime.today().timestamp()

    c.execute('INSERT INTO files VALUES(?, ?, ?, ?, ?)',
              (projectId, fileId, filename, '', t))

    c.execute('INSERT INTO drivers VALUES(?, ?, ?)',
              (fileId, 'None', t))

    db.commit()
    db.close()
    return True


def getFilename(fileId):
    '''
    Returns filename given fileId
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute('SELECT filename FROM files WHERE fileId=?', (fileId,))
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
    print(tuple)
    if tuple == []:
        return ''
    return tuple[0][0]


def updateCode(fileId, code):
    '''
    Updates code given patches to apply
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    t = datetime.datetime.today().timestamp()

    c.execute('UPDATE files SET content=? WHERE fileId=?', (code, fileId))
    c.execute('UPDATE drivers SET times=? WHERE fileId=?', (t, fileId))
    c.execute('UPDATE files SET times=? WHERE fileId=?', (t, fileId))

    db.commit()
    db.close()


def getDriver(fileId):
    '''
    returns current driver of specified file
    '''
    # need to set some code that kicks out the driver after 1 minute of
    # inactivity
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT driver FROM drivers WHERE fileId=?', (fileId,))

    email = c.fetchone()[0]
    print(email, 'this is from db')
    return email


def updateDriver(fileId, email):
    '''
    updates current driver of specified file
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('UPDATE drivers SET driver=? WHERE fileId=?', (email, fileId))
    c.execute('UPDATE drivers SET times=? WHERE fileId=?',
              (datetime.datetime.today().timestamp(), fileId))

    db.commit()
    db.close()


if __name__ == '__main__':
    create_db()
