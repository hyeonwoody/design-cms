# Design CMS

A content management system for UI/UX designers to manage design tokens, palettes,
components, and stack compatibility data. Built on **Wagtail** (CMS admin) +
**Django REST Framework** (API) + **PostgreSQL**. The front end organizes each
feature as a tab and consumes published data from the API. Design tokens can be
imported from Figma.

> Status: **skeleton**. Project structure, settings, routing, and empty apps are in
> place. Domain models, the API, the Wagtail snippets/CMS surface, and the Figma
> import are added stage by stage (see `stages/` and `CLAUDE.md`).

## Stack

Python 3.11 | Django 5.x | Wagtail 6.x | Django REST Framework | PostgreSQL 16 |
WhiteNoise | Gunicorn

## Layout

```
design-cms/
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── settings/  (base.py, dev.py, prod.py)
│   ├── urls.py    (django-admin, wagtail admin, api, pages)
│   ├── wsgi.py / asgi.py
├── apps/
│   ├── home/      (Wagtail pages)
│   ├── core/      (tabbed UI shell, References)
│   ├── catalog/   (Palette, Token  -> Wagtail snippets)
│   ├── library/   (Component, Scenario)
│   └── compat/    (Stack, UIKit, Compatibility)
├── templates/     (base.html + core/index.html)
├── static/        (css/js)
└── fixtures/      (seed data, added later)
```

The `stages/`, `design-system/`, `shared/`, and `setup/` folders are the MWP
workspace that guides the build. Start at `CLAUDE.md`.

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then set SECRET_KEY and DATABASE_URL
createdb design_cms             # PostgreSQL must be running
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Front-end shell: http://localhost:8000/
- Wagtail CMS: http://localhost:8000/admin/
- Django admin: http://localhost:8000/django-admin/
- API: http://localhost:8000/api/

## Routes

| Path | Purpose |
|------|---------|
| `/` | Tabbed front end (apps.core), Wagtail page fallback |
| `/admin/` | Wagtail CMS (designers edit tokens here) |
| `/django-admin/` | Django admin |
| `/api/` | DRF API the tabs consume |
| `/documents/` | Wagtail documents |
