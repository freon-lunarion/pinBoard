#!/bin/sh
# this script for delete the database and create empty database
rm -r */__pycache__/
rm -r */migrations/__pycache__
rm -r */migrations/0*.py
rm db.sqlite3
echo "db.sqlite3 deleted\n"
virtualenv venv
source venv/bin/activate
pip3 install -r requirement.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata sample/users.json
echo "user001, user002, user003 and user004 added with 'abc123' as default password\n"
python3 manage.py createsuperuser