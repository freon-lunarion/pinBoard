#!/bin/sh
# this script for delete the database and create empty database
rm -r */__pycache__/
rm -r */migrations/__pycache__
rm -r */migrations/0*.py
rm db.sqlite3
echo "db.sqlite3 deleted\n"

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata sample/users.json
echo "user001, user002, user003, user004, user005, user006, user007, user008 and user009] added with 'abc123' as default password\n"
python manage.py createsuperuser
python manage.py loaddata sample/contents.json