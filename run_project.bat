@echo off
echo Activating virtual environment...
call .\.venv\Scripts\activate

cd assignment

echo Deleting old databases...
del users.db
del products.db
del orders.db

echo Running migrations...
python manage.py migrate --database=users
python manage.py migrate --database=products
python manage.py migrate --database=orders

echo Running threaded insert command...
python manage.py insert_data

pause
