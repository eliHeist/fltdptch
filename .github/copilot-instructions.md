# Copilot instructions (fltdptch)

## Big picture
- This repo is a Django monolith with three first-party apps registered centrally in `fltdptch/appsConfig.py`:
  - `accounts/`: custom auth user model (`AUTH_USER_MODEL = "accounts.User"`).
  - `flights/`: domain models (Flight/Aircraft/Booking/Reconfirmation) and migrations.
  - `frontend/`: server-rendered UI pages (class-based views + templates).
- App URL mounting is also centralized: `fltdptch/urls.py` delegates to `getAppUrls()` in `fltdptch/appsConfig.py`.
  - If you add a new Django app or change its mount path/namespace, update `app_configs` there.

## Data model & conventions
- Custom user model is `accounts.models.User` (email is `USERNAME_FIELD`). User display helpers: `get_full_name()`, `get_name()`, `get_initials()`.
- `accounts.models.UserProfile` is created automatically in `UserManager.create_user()` and accessed via `user.profile`.
- Flights domain models are split across files under `flights/models/` (e.g. `Flight.py`, `Reconfirmation.py`).
  - When adding a new model module, export it from `flights/models/__init__.py` so `from flights.models import ...` continues to work.

## Request/response patterns (how pages work)
- UI endpoints live in `frontend/views/*.py` and are wired in `frontend/urls.py`.
- Views typically:
  - subclass `LoginRequiredMixin, View`
  - implement `get()` to gather query params (often `date`) via `django.utils.dateparse.parse_date`
  - implement `post()` with a simple `action` switch (e.g. `edit-counters`, `dispatch-flight`) and then `redirect(...)` back to the page.
  - Example pattern: `frontend/views/flights.py` (`action` + helper methods `_edit_counters`, `_dispatch_flight`).

## Templates & UI components
- Server-rendered templates live under `templates/` and app templates under `<app>/templates/`.
- The project uses `django-cotton` + `django-template-partials` (see `TEMPLATES[0]["OPTIONS"]` in `fltdptch/settings.py`).
  - Prefer Cotton components in templates (e.g. `<c-card>`, `<c-table>`, `<c-tabs>` as in `templates/frontend/analytics/base.html`).
  - Avoid inventing new design tokens/colors; reuse the existing component set under `templates/cotton/`.

## Static assets (Vite)
- Frontend assets are managed with Vite in `fltdptch/assets/static/` (see `fltdptch/assets/static/package.json`).
  - Build output is expected in `fltdptch/assets/static/dist/` which is included in `STATICFILES_DIRS`.
  - If you change JS/CSS tooling, update that Vite project and keep Django’s `STATICFILES_DIRS` consistent.

## Local dev configuration (env vars)
- Settings are driven by environment variables via `django-environ` (`environ.Env.read_env()` in `fltdptch/settings.py`).
- Required env vars include at least:
  - `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `INTERNAL_IPS`
  - DB: `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`
  - Email: `EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`, `TO_EMAILS`
- Note: `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` are set `True` in settings; for plain HTTP localhost flows you may need HTTPS or an explicit local override.

## Common commands
- Run migrations: `python manage.py migrate`
- Create admin user: `python manage.py createsuperuser`
- Run server: `python manage.py runserver`
- Run tests (basic): `python manage.py test`

## Dependency management
- Python deps are declared in `pyproject.toml` and compiled into `requirements.txt` using uv (`uv pip compile pyproject.toml -o requirements.txt`).
  - If you edit dependencies in `pyproject.toml`, regenerate `requirements.txt` the same way.
