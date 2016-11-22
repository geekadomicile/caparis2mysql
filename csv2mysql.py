#!/usr/bin/env python

# Run with no args for usage instructions
#
# Notes:
#  - will probably insert duplicate records if you load the same file twice
#  - assumes that the number of fields in the header row is the same
#    as the number of columns in the rest of the file and in the database
#  - assumes the column order is the same in the file and in the database
#
# Speed: ~ 1s/MB
#

from settings import *
import sys
import pymysql
import csv
from inspect import getargspec
from unicodedata import normalize

def main(csvfile, table):

    try:
        conn = getconn()
    except pymysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)

    cursor = conn.cursor()

    loadcsv(cursor, table, csvfile)

    cursor.close()
    conn.close()

def getconn():
    conn = pymysql.connect( host     = DATABASES['default']['HOST'],
                            port     = DATABASES['default']['PORT'],
                            user     = DATABASES['default']['USER'],
                            passwd   = DATABASES['default']['PASSWORD'],
                            db       = DATABASES['default']['NAME'])
    return conn

def loadcsv(cursor, table, filename):
    """
    Open a csv file and load it into a sql table.
    Assumptions:
     - the HEADER_LINE_NUMBER is a header
    """

    f = csv.reader(open(filename), delimiter=';')

    for i in range(HEADER_LINE_NUMBER):
        header = f.next()
    numfields = len(header)

    buildUpdateTableQuery(cursor, table, header)

    query = buildInsertQuery(table, numfields)

    for line in f:
        vals = nullify(line)
        cursor.execute(query, vals)

    return

def buildUpdateTableQuery(cursor, table, header):
    string = header[3].decode('latin-1')
    encoded_str = normalize('NFKD', string).encode('ascii','ignore')
    print(camelCase(encoded_str))

    query = ("create table if not exists %s (id int(12) unsigned not null auto_increment, primary key (id)) engine=InnoDB" % table)
    cursor.execute(query)
    result = cursor.fetchone()

    return

def buildInsertQuery(table, numfields):
    """
    Create a query string with the given table name and the right
    number of format placeholders.
    example:
    >>> buildInsertCmd("foo", 3)
    'insert into foo values (%s, %s, %s)'
    """
    assert(numfields > 0)
    placeholders = (numfields-1) * "%s, " + "%s"
    query = ("insert into %s" % table) + (" values (%s)" % placeholders)
    return query

def nullify(L):
    """Convert empty strings in the given list to None."""

    # helper function
    def f(x):
        if(x == ""):
            return None
        else:
            return x

    return [f(x) for x in L]

def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalpha())
    return output[0].lower() + output[1:]

if __name__ == '__main__':
    # commandline execution

    args = sys.argv[1:]
    mainArgsLen = len(getargspec(main).args)

    if(len(args) < mainArgsLen):
        print "error: " + str(len(args)) + " out of " + str(mainArgsLen) + " arguments: csvfile table"
        sys.exit(1)

    main(*args)
