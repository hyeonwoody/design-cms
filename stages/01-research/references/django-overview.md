# Django Overview

One-page orientation for what Django + DRF give this project. Use it to decide what
belongs in the database, the API, and the admin during research.

## What Django provides

- **Models + ORM:** Python classes map to database tables. Schema changes are tracked as migrations.
- **MVT:** Model-View-Template. Views render templates server-side. This project uses MVT for the tabbed pages.
- **Admin:** An auto-generated CRUD interface over your models. This project uses it as the token CMS (no custom admin UI needed).

## What DRF adds

- **Serializers:** Convert model instances to/from JSON.
- **ViewSets + Routers:** Define API endpoints with minimal code.
- The front-end tabs fetch published data from the API; the admin edits it.

## What this means for research

Anything a designer edits (palettes, tokens, components, scenarios, compatibility,
references) should be a **model** so it lives in the admin and the API. Anything
fixed (spacing scale, layout, contrast thresholds) is a template/code constant.

Official docs: https://docs.djangoproject.com/ and https://www.django-rest-framework.org/
