# Setup Guide: Python + PostgreSQL

This stage and later ones need Python and PostgreSQL installed on your machine. This
guide is for someone installing them for the first time.

## Python

Python runs Django. Target version: `{{PYTHON_VERSION}}`.

1. Install from https://www.python.org/downloads/ (or your OS package manager).
2. Verify: `python3 --version`
3. Create a virtual environment in the project root: `python3 -m venv .venv`
4. Activate it: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install django djangorestframework psycopg[binary] django-environ`

## PostgreSQL

PostgreSQL is the database. The app uses array and JSON fields that need it.

1. Install from https://www.postgresql.org/download/ (or your OS package manager).
2. Verify: `psql --version`
3. Create the database: `createdb {{DB_NAME}}`
4. Point Django at it through `DATABASE_URL` in `.env` (see `.env.example` from stage 05).

## Verify the toolchain

From the project root with the venv active:

```bash
python manage.py makemigrations
python manage.py migrate
```

If both run without errors, Python and PostgreSQL are set up correctly.
