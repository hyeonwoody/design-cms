# Design CMS

UI/UX 디자이너가 디자인 토큰, 팔레트, 컴포넌트, 스택 호환성 데이터를 관리하는 콘텐츠
관리 시스템(CMS)입니다. **Wagtail**(CMS 관리자) + **Django REST Framework**(API) +
**PostgreSQL** 기반으로 만들어졌습니다. 프런트엔드는 각 기능을 탭으로 구성하고 API에서
발행된 데이터를 사용합니다. 디자인 토큰은 Figma에서 가져올 수 있습니다.

> 상태: **동작하는 애플리케이션**. 프로젝트 구조·설정·라우팅에 더해 도메인 모델,
> REST API, Wagtail 스니펫 기반 CMS, 탭 UI, 팔레트 시드, Figma 토큰 임포트가 구현되어
> 있습니다. 단계별 진행 내역은 `stages/`와 `CLAUDE.md`를 참고하세요.

## 스택

Python 3.11 | Django 5.x | Wagtail 6.x | Django REST Framework | PostgreSQL 16 |
WhiteNoise | Gunicorn

## 폴더 구조

```
design-cms/
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── settings/  (base.py, dev.py, prod.py)
│   ├── urls.py    (django-admin, wagtail 관리자, api, 페이지)
│   ├── wsgi.py / asgi.py
├── apps/
│   ├── home/      (Wagtail 페이지)
│   ├── core/      (탭 UI 셸, References)
│   ├── catalog/   (Palette, Token  -> Wagtail 스니펫)
│   ├── library/   (Component, Scenario)
│   └── compat/    (Stack, UIKit, Compatibility)
├── templates/     (base.html + core/index.html)
├── static/        (css/js)
└── fixtures/      (시드 데이터: palettes.json)
```

`stages/`, `design-system/`, `shared/`, `setup/` 폴더는 빌드를 안내하는 MWP
워크스페이스입니다. `CLAUDE.md`에서 시작하세요.

## 로컬 실행

```bash
docker-compose up -d db          # 도커로 PostgreSQL 실행 (design_cms DB 자동 생성)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env             # 기본값이 이미 도커 DB를 가리킵니다
python manage.py migrate
python manage.py seed_palettes   # 참조 팔레트와 토큰 적재
python manage.py createsuperuser
python manage.py runserver
```

명령 대신 픽스처로 시드하려면: `python manage.py loaddata palettes`.

데이터베이스는 도커에서 실행되고(`docker-compose.yml` 참고), 앱은 venv에서 로컬로
실행됩니다. DB는 `docker-compose down`으로 중지합니다(데이터는 `pgdata` 볼륨에 유지됨).

- 프런트엔드 셸: http://localhost:8000/
- Wagtail CMS: http://localhost:8000/admin/
- Django 관리자: http://localhost:8000/django-admin/
- API: http://localhost:8000/api/

## 라우트

| 경로 | 용도 |
|------|------|
| `/` | 탭 프런트엔드(apps.core), 매칭되지 않으면 Wagtail 페이지로 폴백 |
| `/admin/` | Wagtail CMS (디자이너가 토큰을 편집하는 곳) |
| `/django-admin/` | Django 관리자 |
| `/api/` | 탭이 사용하는 DRF API |
| `/documents/` | Wagtail 문서 |
