#!/bin/sh
# this script for delete the database and create empty database
rm -r */__pycache__/
rm -r */migrations/__pycache__
rm -r */migrations/0*.py
rm db.sqlite3
echo "db.sqlite3 deleted\n"
python manage.py makemigrations
python manage.py migrate