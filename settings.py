#!/usr/bin/env python
# coding: utf-8

from decouple import config
from unipath import Path
from dj_database_url import parse as db_url

BASE_DIR = Path(__file__).parent

DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Paris'

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='mysql://myuser:mypassword@myhost/mydatabase',
        cast=db_url
    )
}

HEADER_LINE_NUMBER = config('HEADER_LINE_NUMBER', default=0, cast=int)

SETUP_SQL_SCRIPT = BASE_DIR.child(config('SETUP_SQL_SCRIPT', default='setup.sql'))

# Warning : Update .sql file accordingly
TABLE_RELEVE_NAME = config('TABLE_RELEVE_NAME', default='releve')
