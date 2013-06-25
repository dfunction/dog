import sqlite3 as sql
import datetime
from hashlib import sha512
from SimpleLogger import SimpleLogger

class DB:
    def __init__(self, fileName):
        self.fileName = fileName
        self._log = SimpleLogger("db.log")
        self._log.initialize()
        self.log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self._createEmailsTable()
        self._createUrlsTable()
    
    def _createEmailsTable(self):
        con = sql.connect(self.fileName)
        with con:
            cur = con.cursor()
            cur.execute("create table if not exists Emails(hash text);")
    
    def _createUrlsTable(self):
        con = sql.connect(self.fileName)
        with con:
            cur = con.cursor()
            cur.execute("create table if not exists Urls(hash text);")
    
    def _get_hash(self, message):
        return sha512(message).hexdigest()
    
    def addUrl(self, url):
        strHash = self._get_hash(url)
        con = sql.connect(self.fileName)
        with con:
            cur = con.cursor()
            cur.execute("select hash from Urls where hash=?", [strHash])
            if cur.fetchone() == None:
                cur.execute("insert into Urls values(?)", [strHash])
                self.log("Urls: inserted hash of " + url)
            else:
                self.log("Urls: " + url + " already in database ")
                return False
        return True
    
    def addEmail(self, email):
        strHash = self._get_hash(email)
        con = sql.connect(self.fileName)
        with con:
            cur = con.cursor()
            cur.execute("select hash from Emails where hash=?", [strHash])
            if cur.fetchone() == None:
                cur.execute("insert into Emails values(?)", [strHash])
                self.log("Emails: inserted hash of " + email)
            else:
                self.log("Emails: " + email + " already in database ")
                return False
        return True
    
    def close(self):
        self._log.finalize()
    
    def log(self, message):
        print message
        self._log.log(message)