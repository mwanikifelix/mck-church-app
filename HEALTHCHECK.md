# Health Check Report — mck-church-app

**Date:** 2026-10-09
**Commit checked:** `ba3bdf5` ("structured") on `main`, in sync with `origin/main`
**Scope:** Git hygiene, general health, Django backend, Vue admin panel, Flutter mobile

Legend: 🔴 blocking/critical · 🟡 warning · 🔵 info

---

## 🔴 Critical

### 1. Real secrets are committed to a PUBLIC GitHub repository
- `backend/.env` and `admin-panel/.env` are **tracked in git** and the remote
  (`https://github.com/mwanikifelix/mck-church-app`) is reachable without auth
  (HTTP 200) — i.e. the repo is **public**.
- Committed secrets include: `DJANGO_SECRET_KEY`, `DB_PASSWORD`, `MPESA_CONSUMER_KEY/SECRET`,
  `MPESA_PASSKEY`, `MPESA_PAYBILL_NUMBER`, `FCM_SERVER_KEY`, Google OAuth client ID.
- The root `.gitignore` is **empty (0 bytes)**, and neither `backend/` nor `admin-panel/`
  has its own `.gitignore` — that's why the `.env` files got committed.

**Do now:**
1. Rotate every credential in `backend/.env` (DB password, Django secret key, M-Pesa keys, FCM key).
2. `git rm --cached backend/.env admin-panel/.env`, add a proper root `.gitignore`, commit.
3. Note: removing from a public repo does NOT erase history — rotation is mandatory.
   Optionally rewrite history (e.g. `git filter-repo`) and force-push.

### 2. `admin-panel/node_modules/` is committed to git (8,164 of 8,612 tracked files)
- `git ls-files admin-panel/node_modules` → 8,164 files. This bloats the repo (`.git` = 18 MB),
  causes constant merge conflicts, and hides real changes.
- Fix: `git rm -r --cached admin-panel/node_modules` + ignore it in `.gitignore`.
  (`mobile/build/` is correctly ignored by `mobile/.gitignore`; the empty `backend/tests/`
  directory is not tracked at all.)

### 3. Admin panel production build is broken
```
npm run build  →  ✗ Could not resolve "../services/church-profile.service"
                  from "src/views/AboutContentView.vue"
```
- `src/views/AboutContentView.vue:185` imports `../services/church-profile.service`,
  but **that file does not exist** in `src/services/` (15 other services do).
- The view calls `churchProfileService.get()` and `.update(profile)`.
- The backend endpoint it needs **does exist**: `GET/PATCH /api/membership/church-profile/`
  (`backend/apps/membership/urls.py:18` → `ChurchProfileView`).
- Fix: create `src/services/church-profile.service.js` with
  `get: () => api.get("/membership/church-profile/")` and
  `update: (data) => api.patch("/membership/church-profile/", data)`
  following the pattern of `src/services/about.service.js`.
- Note: `npm run dev` (used in docker-compose) only breaks when this view is opened —
  the missing module fails lazily, so the bug is easy to miss in dev.

---

## 🟡 Warnings

### 4. No production Django settings
- `backend/config/settings/prod.py` is **empty (0 bytes)**.
- `manage.py`, `wsgi.py`, `asgi.py`, and `celery.py` all default to `config.settings.dev`
  — so a production deploy would silently run with `DEBUG=True`-style dev settings unless
  `DJANGO_SETTINGS_MODULE` is explicitly overridden.
- Also `config/settings/` has no `__init__.py` (works via PEP 420 namespace packages,
  but non-standard for Django).

### 5. Zero backend tests
- Every `backend/apps/*/tests/` package contains only `__init__.py`.
  `manage.py test` → "Ran 0 tests / Found 0 test(s)". 16 Django apps, no coverage.

### 6. Stray/junk files tracked in git
- `admin-panel/vite.config.js.timestamp-1790612684103-0c61ef266fa79.mjs`
  (leftover from a crashed Vite dev server)
- `mobile/pubspec.yaml.backup`
- Fix: `git rm --cached` both + ignore patterns `*.timestamp-*.mjs`, `*.backup`.

### 7. Broken README ending
- `README.md` last line is corrupted:
  `...concept tied to Branch.# mck-church-app` (stray appended heading).
- README also describes files that don't exist (`.env.example`, `apps_groups_models.py`)
  and says Postgres is on port 5432 in one place while docker-compose maps **5433**.
- `SETUP.md` §1.6 similarly says `psql -p 5432 -U mck_user` — compose actually uses
  port **5433**, user `admin`.

### 8. Weak hardcoded dev credentials in `docker-compose.yml`
- Postgres `admin/CHANGE_ME_DEV_DB_PASSWORD`, pgAdmin `admin@mck.church/admin123`. Acceptable for local
  dev only; make sure these never carry to any shared/staging environment.

### 9. Local backend venv was broken (now repaired during this check)
- `backend/.venv` had been created with Python **3.13.14**, which was since removed from
  the system (`/usr/bin/python3` → 3.14), leaving the venv unable to import anything
  (`ModuleNotFoundError: No module named 'django'`).
- **Action taken during this check (with your approval):** recreated `backend/.venv`
  with the system Python 3.14 and reinstalled `requirements.txt`. All Django checks
  now pass under it.

---

## 🔵 Info / passing

- **Django:** `manage.py check` → 0 issues. `manage.py makemigrations --check --dry-run`
  → no pending migrations (harmless warning: DB host `postgres` unreachable outside Docker).
- **Flutter:** `flutter analyze` → *No issues found!* · `flutter test` → 1/1 passed.
- **Git:** working tree clean, branch `main` in sync with `origin/main`.
- **Docker:** compose file is coherent (ports 8000/5173/5433/6380/91/8025 deliberately
  avoid the icmfs stack), Dockerfiles for backend/admin look sound; `docker/nginx/nginx.conf`
  exists but nginx is not wired into compose (noted as "no nginx in front yet").
- **API contract spot-check:** admin panel's `VITE_API_BASE_URL=http://localhost:8000/api`
  matches `backend/config/urls.py` prefixes; the only mismatch found is the missing
  service file in item 3.

---

## Recommended action order

1. **Rotate secrets + untrack `.env` files + real `.gitignore`** (items 1–2) — do first, before any other commits.
2. **Create `church-profile.service.js`** and re-run `npm run build` (item 3).
3. Untrack `node_modules` and the stray files (items 2, 6).
4. Fill in `prod.py` and set `DJANGO_SETTINGS_MODULE` in compose/prod deploys (item 4).
5. Fix README/SETUP inaccuracies (item 7).
6. Start adding backend tests for the 16 apps (item 5).

*Environment note: checks ran with Python 3.14, Node 20.20.2, Flutter 3.32.8, Docker 29.7.2.*
