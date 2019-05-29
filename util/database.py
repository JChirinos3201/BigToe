import uuid

import sqlite3   # enable control of an sqlite database


class DB_Manager:
    '''
    HOW TO USE:
    Every method openDB by connecting to the inputted path of
    a database file. After performing all operations on the
    database, the instance of the DB_Manager must save using
    the save method.
    The operations/methods can be found below.
    '''

    def __init__(self, dbfile):
        '''
        SET UP TO READ/WRITE TO DB FILES
        '''

        self.DB_FILE = dbfile
        self.db = None
    # ========================HELPER FXNS=======================

    def openDB(self):
        '''
        OPENS DB_FILE AND RETURNS A CURSOR FOR IT
        '''
        # open if file exists, otherwise create
        self.db = sqlite3.connect(self.DB_FILE)
        return self.db.cursor()

    def createUsersTable(self):
        '''
        CREATES A 2 COLUMN users table if it doesnt already exist.
        Will be replaced by oauth.
        '''
        c = self.openDB()
        c.execute('CREATE TABLE IF NOT EXISTS users(email TEXT, password TEXT)')
        c.execute('INSERT INTO users VALUES (?, ?)', ('admin', 'password'))

    def createProjectIDTable(self):
        '''
        CREATES A 2 COLUMN id table if it doesnt already exist
        '''
        c = self.openDB()
        c.execute('CREATE TABLE IF NOT EXISTS ids(id TEXT, name TEXT)')
        # c.execute('INSERT INTO ids VALUES (?, ?)', ('000', 'worm'))


    def createPermissionsTable(self):
        '''
        CREATES A 2 COLUMN permissions table if it doesnt already exist
        '''
        c = self.openDB()
        c.execute('CREATE TABLE IF NOT EXISTS permissions(id TEXT,email TEXT)')

    def createFilesTable(self):
        '''
        CREATES A 3 COLUMN files table if it doesnt already exist
        '''
        c = self.openDB()
        c.execute('CREATE TABLE IF NOT EXISTS files(id TEXT,name TEXT,content TEXT)')

    def insertRow(self, tableName, data):
        '''
        APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
        @tableName is the name the table being written to
        @data is a tuple containing data to be entered
        must be 2 columns big
        '''
        c = self.openDB()
        # print(data)
        command = 'INSERT INTO {0} VALUES {1}'.format(tableName, data)
        #print(command)
        # print(command)
        c.execute(command)

    def isInDB(self, tableName):
        '''
        RETURNS True IF THE tableName IS IN THE DATABASE
        RETURNS False OTHERWISE
        '''
        c = self.openDB()
        command = 'SELECT * FROM sqlite_master WHERE type = "table"'
        c.execute(command)
        selectedVal = c.fetchall()
        # list comprehensions -- fetch all tableNames and store in a set
        tableNames = set([x[1] for x in selectedVal])

        return tableName in tableNames

    def table(self, tableName):
        '''
        PRINTS OUT ALL ROWS OF INPUT tableName
        '''
        c = self.openDB()
        command = 'SELECT * FROM "{0}"'.format(tableName)
        c.execute(command)
        selectedVal = c.fetchall()
        print(dict(selectedVal))

    def save(self):
        '''
        COMMITS CHANGES TO DATABASE AND CLOSES THE FILE
        '''
        #self.openDB()
        self.db.commit()
        self.db.close()
        print(self.db)
    # ========================HELPER FXNS=======================
    # ==========================================================
    # ======================== DB FXNS =========================
    # ==========================================================
    # ======================= USER FXNS ========================

    def getUsers(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT users AND
        CORRESPONDING PASSWORDS
        '''
        c = self.openDB()
        if not self.isInDB('users'):
            self.createUsersTable()
            self.save()
        print("TABLE: ", self.table('users'))
        command = 'SELECT email, password FROM users'
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def registerUser(self, email, password):
        '''
        ADDS user TO users table
        '''
        if not self.isInDB('users'):
            self.createUsersTable()
            self.save()
        # userName is already in database -- do not continue to add
        if self.findUser(email):
            return False
        # userName not in database -- continue to add
        else:
            row = (email, password)
            self.insertRow('users', row)
            return True

    def findUser(self, email):
        '''
        CHECKS IF userName IS UNIQUE
        '''
        return email in self.getUsers()

    def verifyUser(self, email, password):
        '''
        CHECKS IF userName AND password MATCH THOSE FOUND IN DATABASE
        '''
        c = self.openDB()
        if not self.isInDB('users'):
            self.createUsersTable()
            self.save()
        command = 'SELECT email, password FROM users WHERE email = "{0}"'\
                  .format(email)
        c.execute(command)
        selectedVal = c.fetchone()
        if selectedVal is None:
            return False
        if email == selectedVal[0] and password == selectedVal[1]:
            return True
        return False

    def changePassword(self, email, password):
        '''
        CHECKS IF userName AND password MATCH THOSE FOUND IN DATABASE
        '''
        c = self.openDB()
        if not self.isInDB('users'):
            self.createUsersTable()
            self.save()
        command = 'SELECT email, password FROM users WHERE email = "{0}"'\
                  .format(email)
        c.execute(command)
        selectedVal = c.fetchone()
        if selectedVal is None:
            return False
        if email == selectedVal[0]:
            command = 'UPDATE users SET password=? WHERE email = ?'
            c.execute(command, (password, email))
            return True

        return False
    # ========================   ids FXNS ==========================

    def getIDs(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT projects
        AND CORRESPONDING ids
        '''
        c = self.openDB()
        if not self.isInDB('ids'):
            self.createProjectIDTable()
            self.save()
            # print("IDS table is in db.")
            # self.table('ids')
            # print("--------------------")
        # print(self.db)
        command = 'SELECT * FROM ids'
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def getPname(self, projectId):
        return self.getIDs().get(projectId, None)

    def findID(self, projectId):
        '''
        CHECKS IF uuid IS UNIQUE
        '''
        if not self.isInDB('ids'):
            self.createProjectIDTable()
            self.save()
        return projectId in self.getIDs()

    def createProject(self, projectName, email):
        '''
        ADDS project TO IDs table
        '''
        if not self.isInDB('ids'):
            self.createProjectIDTable()
            self.save()
        id = str(uuid.uuid4())
        while self.findID(id):  # probably not necessary but might as well
            id = str(uuid.uuid4())
        print(id)
        row = (id, projectName)
        self.insertRow('ids', row)
        self.save()
        self.createPermission(id, email, True)
        return True

    # ==================== permissions FXNS ==========================

    def getPermissions(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT projects
        AND CORRESPONDING ids
        '''
        if not self.isInDB('permissions'):
            self.createPermissionsTable()
            self.save()
        c = self.openDB()
        command = 'SELECT id, email FROM permissions'
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def findProjects(self, email):
        '''
        Returns all of the projects that the email has permission to access
        '''
        c = self.openDB()
        command = 'SELECT id,email FROM permissions WHERE email= "{0}"'\
                  .format(email)
        print(command)
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def createPermission(self, projectId, email, new=False):
        '''
        ADDS permission TO permissions table
        '''
        if not self.isInDB('permissions'):
            self.createPermissionsTable()
            self.save()
        if new or self.findID(projectId):
            row = (projectId, email)
            self.insertRow('permissions', row)
            # self.createPermission()
            return True
        return False

    def getCollaborators(self, projectId):
        '''
        Returns a list of emails who are associated with a project
        '''
        pass

    def addCollaborator(self, projectId, email):
        '''
        Adds an email address as a collaborator on a project
        '''
        pass

    def getProjects(self,email):
        '''
        Returns a list of tuples for each project
        '''
        d1=self.findProjects(email)
        d2=self.getIDs()
        retlist=[]
        #print(d1)
        #print(d2)
        for key in d1:
            if key in d2:
                retlist.append((key,d2[key]))
        return retlist

    # ==================== files FXNS ==========================

    def getFiles(self,pid):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT projects
        AND CORRESPONDING ids
        '''
        if not self.isInDB('files'):
            self.createFilesTable()
            self.save()
        # c = self.openDB()
        # command = 'SELECT id, email FROM permissions'
        # c.execute(command)
        # selectedVal = c.fetchall()
        # return dict(selectedVal)

    def addFile(self, filename, projectId):
        '''
        Adds a new file given projectId
        '''
        pass

    def getFilename(self, fileId):
        '''
        Returns the filename given a file idea
        '''
        pass

    def getCode(self, fileId):
        '''
        Returns the code stored in a file given the fileId
        '''
        pass
