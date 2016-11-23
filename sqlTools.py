from settings import *
import pymysql

def getconn():
    conn = pymysql.connect( charset  = 'utf8',
                            host     = DATABASES['default']['HOST'],
                            port     = DATABASES['default']['PORT'],
                            user     = DATABASES['default']['USER'],
                            passwd   = DATABASES['default']['PASSWORD'],
                            db       = DATABASES['default']['NAME'])
    return conn

def loadSqlScript(sqlScript):
    f = open(sqlScript)

    query = ''
    for line in f:
        query = query + line
    return query
