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
import csv
from inspect import getargspec
import re
from sqlTools import *
from dateutil.parser import parse
import hashlib

def main(*csvfile):

    try:
        conn = getconn()
    except pymysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit (1)

    cursor = conn.cursor()

    for f in csvfile:
        loadcsv(cursor, TABLE_RELEVE_NAME, f)

    cursor.close()
    conn.commit()
    conn.close()

def loadcsv(cursor, table, filename):
    """
    Open a csv file and load it into a sql table.
    Assumptions:
     - the HEADER_LINE_NUMBER is a header
    """
    f = csv.reader(open(filename), delimiter=';')

    for i in range(HEADER_LINE_NUMBER):
        header = f.next()
    # remove last char
    header = header[:-1]
    numfields = len(header)

    query = buildInsertQuery(table, numfields)

    for line in f:
        # Normalize vals
        line = line[:-1]
        vals = normalizeDate(normalizeDecimalMark(nullifyAndDecode(line)))
        vals = padArguments(vals,numfields)
        vals = addHash(vals)
        cursor.execute(query, vals)

    return

def buildInsertQuery(table, numfields):
    """
    Create a query string with the given table name and the right
    number of format placeholders (including id set to default and hash columns).
    example:
    >>> buildInsertQuery("foo", 3)
    'insert into foo values (%s, %s, %s)'
    """
    assert(numfields > 0)
    placeholders = (numfields-1) * "%s, " + "%s"
    query = ("insert ignore into %s" % table) + (" values (default, %s, %%s)" % placeholders)
    return query

def nullifyAndDecode(L):
    """Decode and Convert empty strings in the given list to NULL."""

    # helper function
    def f(x):
        if(x == ""):
            return None
        else:
            return x.decode('latin-1')

    return [f(x) for x in L]

def padArguments(L, numfields):
    """Extend List to numfields length."""
    return L + [None] * (numfields - len(L))

def addHash(L):
    """Add unique hash of itself."""
    return L + [u'' + hashlib.sha224(str(L)).hexdigest()]

def normalizeDate(L):
    """Convert DD/MM/YYYY in YYYY-MM-DD."""
    pattern = re.compile("^[0-3][0-9]/[0-1][0-9]/[0-9]{4}$")

    # helper function
    def f(pattern, x):
        if(x and pattern.match(x)):
            return parse(x, dayfirst=True)
        else:
            return x

    return [f(pattern, x) for x in L]

def normalizeDecimalMark(L):
    """Convert decimal mark ',' in '.'"""
    decmark_reg = re.compile('(?<=\d),(?=\d)')

    # helper function
    def f(decmark_reg, x):
        if(x):
            return decmark_reg.sub('.',x)
        else:
            return x

    return [f(decmark_reg, x) for x in L]

if __name__ == '__main__':
    # commandline execution

    args = sys.argv[1:]
    mainArgsLen = len(getargspec(main).args)

    if(len(args) < mainArgsLen):
        print "error: " + str(len(args)) + " out of " + str(mainArgsLen) + "    Usage: " + sys.argv[0] + "csvfile"
        sys.exit(1)

    main(*args)
