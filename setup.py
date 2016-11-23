#!/usr/bin/env python

from settings import *
import sys
from inspect import getargspec
from sqlTools import *
import pymysql

def main(sqlScript = SETUP_SQL_SCRIPT):
    try:
        conn = getconn()
    except pymysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)

    cursor = conn.cursor()

    if DEBUG:
        query = "DROP TABLE releve"
        try:
            cursor.execute(query)
        except pymysql.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            if(e.args[0] == 1051):
                print "This error isn't important, setup will continue."

    query = loadSqlScript(sqlScript)
    cursor.execute(query)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    # commandline execution

    args = sys.argv[1:]
    mainArgsLen = len(getargspec(main).args)

    main(*args)
