# MCK Church App — Environment Setup

## Folder layout expected

```
mck-church-app/
├── docker-compose.yml
├── .env                    (copy from .env.example, fill in real values)
├── backend/                (your existing mck-backend, Django)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── apps/
│       ├── accounts/
│       ├── church/
│       ├── groups/         ← NEW app, add apps_groups_models.py here as models.py
│       ├── events/
│       ├── membership/
│       ├── giving/
│       ├── pastoral/
│       ├── content/
│       ├── chatbot/
│       └── notifications/
└── admin-panel/             (Vue 3 admin)
    ├── Dockerfile
    └── (vite project)
```

Move `docker-compose.yml`, `.env.example`, `backend/Dockerfile`,
`backend/requirements.txt`, and `admin-panel/Dockerfile` into that layout
alongside your existing `mck-backend` code. Rename
`apps_groups_models.py` to `apps/groups/models.py` once you create the new
`groups` app (`python manage.py startapp groups`), then register it in
`INSTALLED_APPS` and wire `Group`/`GroupStage`/`GroupMembership` into the
Django admin and DRF serializers the same way `Department` already is.

## First run

```bash
cp .env.example .env          # then fill in real secrets
docker compose build
docker compose up -d
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_roles
docker compose exec backend python manage.py createsuperuser
```

- Backend API: http://localhost:8000
- Django admin: http://localhost:8000/admin
- Vue admin panel: http://localhost:5173
- Mailhog (dev email inbox): http://localhost:8025
- Postgres: localhost:5432 (creds from `.env`)

## Flutter (not containerized)

Run natively against the backend:
```bash
flutter run --dart-define=API_BASE_URL=http://localhost:8000
# Android emulator can't see "localhost" on the host machine — use:
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

## Day-to-day

```bash
docker compose up -d              # start everything
docker compose logs -f backend    # tail backend logs
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
docker compose down                # stop everything (data persists in volumes)
docker compose down -v             # stop AND wipe volumes (fresh DB)
```

## What's in this drop

| File | Purpose |
|---|---|
| `docker-compose.yml` | Postgres, Redis, Django backend, Celery worker + beat, Vue admin, Mailhog |
| `backend/Dockerfile` | Python 3.12 image for Django |
| `backend/requirements.txt` | Django + DRF + Celery + Google OAuth + M-Pesa deps |
| `admin-panel/Dockerfile` | Node/Vite image for the Vue admin panel |
| `.env.example` | All env vars the compose file expects |
| `SCHEMA.md` | Full ERD + rationale, including the generalized `Group` model |
| `apps_groups_models.py` | Ready-to-drop-in Django models for the new `groups` app |

See `SCHEMA.md` for the data model and the reasoning behind folding
Youth/JCTM into one generic `Group` concept tied to `Branch`.# mck-church-app
