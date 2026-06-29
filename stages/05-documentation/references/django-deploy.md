# Django Deploy and Run Checklist

What the README and architecture docs must cover so `{{PROJECT_NAME}}` runs for a
reviewer (or interviewer) from a clean checkout. Use this when writing stage 05.

## Local run (document in README)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then fill in secrets
python manage.py migrate
python manage.py loaddata palettes scenarios compatibility references
python manage.py createsuperuser
python manage.py runserver
```

## Environment variables (document in .env.example)

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Django secret |
| `DEBUG` | `True` locally, `False` in production |
| `DATABASE_URL` | PostgreSQL connection for `{{DB_NAME}}` |
| `ALLOWED_HOSTS` | Comma-separated hostnames |
| `FIGMA_ACCESS_TOKEN` | Token for the Figma import (placeholder `{{FIGMA_ACCESS_TOKEN}}`) |

## Production notes

- Settings split: `config/settings/base.py` + `prod.py`.
- Static files served by WhiteNoise; run `collectstatic` on deploy.
- Run under Gunicorn: `gunicorn config.wsgi`.
- Set `DEBUG=False` and a real `SECRET_KEY` and `ALLOWED_HOSTS`.

## Architecture doc must include

The ERD (from stage 03), the route/tab map (from stage 02), and the Figma import flow.

Reference: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
