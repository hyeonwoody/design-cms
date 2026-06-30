# Setup Guide: Python + PostgreSQL

This stage and later ones need Python and a PostgreSQL database. Python runs on your
machine in a virtual environment; PostgreSQL runs in Docker. This guide is for someone
setting both up for the first time.

## Python

Python runs Django. Target version: `{{PYTHON_VERSION}}`.

1. Install from https://www.python.org/downloads/ (or your OS package manager).
2. Verify: `python3 --version`
3. Create a virtual environment in the project root: `python3 -m venv .venv`
4. Activate it: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)
5. Install dependencies: `pip install -r requirements.txt`

## PostgreSQL (via Docker)

PostgreSQL is the database. The app uses array and JSON fields that need it. This
project runs Postgres in Docker, so you do not install it on your machine. The `db`
service in `docker-compose.yml` creates the `design_cms` database automatically.

1. Install Docker: https://docs.docker.com/get-docker/
2. Start the database: `docker-compose up -d db` (from the project root)
3. Verify it is healthy: `docker-compose ps` (the `db` service shows "healthy")
4. No `createdb` step is needed; the container already holds `design_cms`. Django
   connects through `DATABASE_URL` in `.env`
   (`postgres://postgres:postgres@localhost:5432/design_cms`).

Note: only one Postgres can bind host port 5432. If another project's container (for
example `design_poc_db`) is running, stop it first: `docker stop design_poc_db`.

## Verify the toolchain

From the project root with the venv active:

```bash
python manage.py makemigrations
python manage.py migrate
```

If both run without errors, Python and PostgreSQL are set up correctly.
