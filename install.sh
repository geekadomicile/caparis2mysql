#!/bin/bash

# Create dir
mkdir downloads

# Install dependencies
sudo pip install pymysql
sudo pip install jupyterlab
sudo pip install python-decouple
sudo pip install dj-database-url
sudo pip install unipath
sudo pip install python-dateutil

# Repair dir and file permissions
find * -type d -print0 | xargs -0 chmod 0755 # for directories
find . -type f -print0 | xargs -0 chmod 0644 # for files
find ./run.py -type f -print0 | xargs -0 chmod 0744 # for files
find ./setup.py -type f -print0 | xargs -0 chmod 0744 # for files

# Setup database
./setup.py

# Uncomment while debugging
find . -type f -print0 | xargs -0 chmod 0744 # for files
