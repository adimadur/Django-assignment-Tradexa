# Django Distributed Insert Assignment

This project simulates a distributed system where `Users`, `Products`, and `Orders` are stored in **separate SQLite databases** and inserted concurrently using **Python threads**.

## Features
- 3 databases: `users.db`, `products.db`, `orders.db`
- Separate Django models for each
- Custom database router to route models to correct DB
- Threaded insertions using Python's `threading` module
- All validation handled in application logic

## Setup Instructions

```bash
# Setup virtual environment
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Apply migrations to each database
python manage.py migrate --database=users
python manage.py migrate --database=products
python manage.py migrate --database=orders

# Run the threaded insert command
python manage.py insert_data
```

## Run via bat file (automated)
Just double click on `run_project.bat` file in your root folder and all the commands are executed one by one. No need to manually type.