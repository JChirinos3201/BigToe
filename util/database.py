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
            command = 'CREATE TABLE "{0}"({1}, {2});'.format('USERS', 'username TEXT', 'password TEXT')
            c.execute(command)


    def insertRow(self, tableName, data):
       '''
         APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
         @tableName is the name the table being written to
         @data is a tuple containing data to be entered
         must be 3 columns big
       '''
       c = self.openDB()
       command = 'INSERT INTO "{0}" VALUES(?, ?, ?, ?)'
       c.execute(command.format(tableName), data)


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

    #======================== DB FXNS =========================

    def getUsers(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT users AND CORRESPONDING PASSWORDS
        '''
        c = self.openDB()
        command = 'SELECT username, password FROM USERS'
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)


    def registerUser(self, username, password):
        '''
        ADDS user TO USERS table. Upon registration, user inputs wanted currency
        '''
        c = self.openDB()
        # userName is already in database -- do not continue to add
        if self.findUser(username):
            return False
        # userName not in database -- continue to add
        else:
            row = (username, password)
            self.insertRow('USERS', row)
            return True

    def findUser(self, username):
        '''
        CHECKS IF userName IS UNIQUE
        '''
        return username in self.getUsers()

    def verifyUser(self, username, password):
        '''
        CHECKS IF userName AND password MATCH THOSE FOUND IN DATABASE
        '''
        c = self.openDB()
        command = 'SELECT username, password FROM USERS WHERE username = "{0}"'.format(username)
        c.execute(command)
        selectedVal = c.fetchone()
        if selectedVal == None:
            return False
        if userName == selectedVal[0] and password == selectedVal[1]:
            return True
return False
