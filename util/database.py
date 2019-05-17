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
    #========================HELPER FXNS=======================
    def openDB(self):
        '''
        OPENS DB_FILE AND RETURNS A CURSOR FOR IT
        '''
        self.db = sqlite3.connect(self.DB_FILE) # open if file exists, otherwise create
        return self.db.cursor()

    def createUsersTable(self):
        '''
        CREATES A 2 COLUMN USERS table if it doesnt already exist. Will be replaced by oauth.
        '''
        c = self.openDB()
        if not self.isInDB('USERS'):
            command = 'CREATE TABLE "{0}"({1}, {2});'.format('USERS', 'email TEXT', 'password TEXT')
            c.execute(command)

    def createProjectIDTable(self):
        '''
        CREATES A 2 COLUMN id table if it doesnt already exist
        '''
        c = self.openDB()
        if not self.isInDB('IDS'):
            command = 'CREATE TABLE "{0}"({1}, {2});'.format('IDS', 'id TEXT', 'email TEXT')
            c.execute(command)

    def createPermissionsTable(self):
        '''
        CREATES A 2 COLUMN permissions table if it doesnt already exist
        '''
        c = self.openDB()
        if not self.isInDB('PERMISSIONS'):
            command = 'CREATE TABLE "{0}"({1}, {2});'.format('PERMISSIONS', 'id TEXT', 'email TEXT')
            c.execute(command)

    def insertRow(self, tableName, data):
       '''
         APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
         @tableName is the name the table being written to
         @data is a tuple containing data to be entered
         must be 2 columns big
       '''
       c = self.openDB()
       command = 'INSERT INTO "{0}" VALUES {1}'
       c.execute(command.format(tableName, data))

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


    def save(self):
        '''
        COMMITS CHANGES TO DATABASE AND CLOSES THE FILE
        '''
        self.db.commit()
        self.db.close()
    #========================HELPER FXNS=======================



    #==========================================================
    #======================== DB FXNS =========================
    #==========================================================

    #======================= USER FXNS ========================
    def getUsers(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT users AND CORRESPONDING PASSWORDS
        '''
        c = self.openDB()
        command = 'SELECT email, password FROM USERS'
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)


    def registerUser(self, email, password):
        '''
        ADDS user TO USERS table
        '''
        c = self.openDB()
        # userName is already in database -- do not continue to add
        if self.findUser(email):
            return False
        # userName not in database -- continue to add
        else:
            row = (email, password)
            self.insertRow('USERS', row)
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
        command = 'SELECT email, password FROM USERS WHERE email = "{0}"'.format(email)
        c.execute(command)
        selectedVal = c.fetchone()
        if selectedVal == None:
            return False
        if email == selectedVal[0] and password == selectedVal[1]:
            return True
        return False

    #========================   IDS FXNS ==========================

    def getIDs(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT projects AND CORRESPONDING ids
        '''
        c = self.openDB()
        command = 'SELECT id, name FROM IDS'
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def findID(self, uuid):
        '''
        CHECKS IF uuid IS UNIQUE
        '''
        return uuid in self.getIDs()

    def createProject(self, projectName,email):
        '''
        ADDS project TO IDs table
        '''
        c = self.openDB()
        id=str(uuid.uuid4())
        while self.findID(id): #probably not necessary but might as well
            id=str(uuid.uuid4())
        row = (id, email)
        self.insertRow('IDS', row)
        self.createPermission(uuid, email)
        return True

    #==================== PERMISSIONS FXNS ==========================

    def getPermissions(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT projects AND CORRESPONDING ids
        '''
        c = self.openDB()
        command = 'SELECT id, email FROM PERMISSIONS'
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def findProjects(self, email):
        '''
        Returns all of the projects that the email has permission to access
        '''
        c = self.openDB()
        command = 'SELECT id, email FROM PERMISSIONS WHERE email={0}'.format(email)
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def createPermission(self, uuid, email):
        '''
        ADDS permission TO PERMISSIONS table
        '''
        c = self.openDB()
        if self.findID(uuid):
            row = (uuid, email)
            self.insertRow('PERMISSIONS', row)
            #self.createPermission()
            return True
        return False
