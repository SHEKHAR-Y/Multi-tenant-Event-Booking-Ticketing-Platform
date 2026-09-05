# Multi-Tenant Event Booking & Ticketing Platform

A production-style backend for an event booking and ticketing system (think BookMyShow), built as a deep dive into backend architecture, authentication security, and database design — not just "make the CRUD work," but "make it the way a real system would need to work."

This is a work-in-progress portfolio project. The goal isn't to ship every feature fast; it's to get the foundational layers — auth, error handling, data access — structurally right before building the rest on top of them.

---

## Why this project

Most tutorial-style CRUD APIs stop at "it works." This project is an exercise in the parts that usually get skipped:

- **Secure, rotating refresh tokens** with reuse detection — not just a long-lived JWT.
- **Strict layered architecture** (router → service → repository) so business logic never leaks into HTTP handlers or SQL leaks into services.
- **Centralized, typed exception handling** instead of scattered `try/except` blocks and silent failures.
- **Migration-first schema management** with Alembic, so the database's history is reviewable, not reconstructed from a live DB.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (typed, `Mapped[...]` style) |
| Database | PostgreSQL |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth | JWT (access + rotating refresh tokens), `python-jose` |
| Password hashing | `pwdlib` (Argon2) |
| Testing | Pytest + FastAPI `TestClient` |
| Planned | Docker, Redis, Celery |

---

## Architecture

The codebase follows a strict layered pattern. Each layer has exactly one job:

```
Router          → HTTP concerns only: parses requests, extracts tokens, returns responses.
                  No business logic, no DB access.

Service         → Owns business logic, auth/token verification, orchestration
                  across repositories.

Repository      → Owns DB access only. No business rules, no validation.

Exceptions      → Domain-specific exceptions raised anywhere in service/repository
                  layers, mapped to HTTP responses in ONE place (main.py).
```

```
Request
   │
   ▼
┌─────────┐     ┌─────────┐     ┌────────────┐     ┌──────────────┐
│  Router  │ ──▶ │ Service │ ──▶ │ Repository │ ──▶ │  PostgreSQL  │
└─────────┘     └─────────┘     └────────────┘     └──────────────┘
                     │
                     ▼
             Domain Exceptions
                     │
                     ▼
        Global Exception Handlers (main.py)
                     │
                     ▼
              HTTP Response
```

This means: a service function never returns an HTTP status code, and a router never touches SQLAlchemy directly.

### Project structure

```
app/
├── core/                 # config, security, db session, exceptions, logging
├── models/               # SQLAlchemy ORM models
├── schemas/              # Pydantic request/response schemas
├── repository/           # DB access layer (one repository per entity)
├── services/             # Business logic layer
├── router/               # FastAPI route definitions
└── dependencies/         # Reusable FastAPI dependencies (e.g. current-user resolution)

alembic/
└── versions/             # Migration history
```

---

## Authentication & Token Security

This is the part of the project I spent the most deliberate effort on.

### Access tokens
Short-lived JWTs, signed and verified server-side, carrying the user's identity (`sub`) — stateless, never persisted.

### Refresh tokens — rotation with reuse detection

Rather than a single long-lived refresh token, this project implements **refresh token rotation** with **family-based reuse detection**, the same pattern used by production auth systems (e.g. Auth0):

- Every refresh token belongs to a **token family** (`family_id`), created once at login and carried forward through every subsequent rotation in that session.
- Each time a refresh token is used, it is marked `is_used` and a **new** refresh token is issued in its place, inheriting the same `family_id`.
- If a refresh token that's already been used (or revoked) is presented again, the system treats this as a signal of theft — **the entire token family is revoked immediately**, invalidating that whole session chain.
- Revocation is scoped intentionally:
  - **Reuse detected on one device's session** → revoke only that family (that device/session).
  - **Explicit "log out everywhere" / password change** → revoke all families for that `user_id`.

```
Login
  │
  ▼
new family_id ──┬─▶ refresh_token_v1 (family_id=F1)
                │
        [access token expires]
                │
                ▼
        POST /refresh (token_v1)
                │
        ┌───────┴────────┐
        │ token unused?   │──No──▶ REVOKE entire family F1 (reuse/theft detected)
        └───────┬────────┘
                │ Yes
                ▼
     mark token_v1 as used
                │
                ▼
     issue refresh_token_v2 (same family_id=F1)
     issue new access_token
```

### Why this matters
A stolen refresh token that gets used by an attacker *after* the legitimate client has already rotated it will be detected and the whole session killed — rather than silently granting the attacker persistent access.

---

## Database Schema

Core entities (six tables), designed around real booking-domain constraints rather than a flattened "one big table" model:

- **users** — auth identity, role (`organizer` / `customer` / `admin`)
- **refresh_tokens** — rotation chain, family-scoped, indexed on `family_id` and `user_id`, cascades on user deletion
- **events** — owned by an organizer (`organizer_id` resolved server-side from the JWT — never trusted from client input)
- **seats**, **bookings**, **booking_seats**, **payments** *(in progress)*

Key design decisions:
- `organizer_id` on event creation always comes from the authenticated user's token, never from the request body — preventing a customer from creating events "as" someone else.
- Seat availability is derived from the `seats` table, not a cached counter on `events`, to avoid drift between the source of truth and a denormalized count.
- All foreign keys used in filtering/joins are explicitly indexed (PostgreSQL does **not** auto-index foreign key columns).

---

## Error Handling

Domain exceptions are defined once (`app/core/exceptions.py`) and mapped to HTTP responses in a single place (`app/main.py`), rather than scattered `HTTPException` calls throughout routers/services:

| Exception | HTTP Status |
|---|---|
| `UserNotFound` | 404 |
| `UserAlreadyExists` | 409 |
| `InvalidCredentialError` | 401 |
| `UserNotAuthorized` | 403 |
| `InvalidTokenError` / `TokenExpiredError` | 401 |
| `CustomIntegrityError` | 409 |
| `DatabaseUnavailableError` | 503 |

Repository-layer DB errors (`IntegrityError`, `OperationalError`, etc.) are caught and translated into these domain exceptions via a shared context manager (`handle_db_error`), so services never deal with raw SQLAlchemy exceptions directly.

---

## Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL running locally (or via Docker)

### Setup

```bash
git clone https://github.com/SHEKHAR-Y/Multi-tenant-Event-Booking-Ticketing-Platform.git
cd Multi-tenant-Event-Booking-Ticketing-Platform

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env           # fill in your local DB URL, secret key, etc.

alembic upgrade head           # apply migrations
```

### Run the API

```bash
uvicorn app.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs` (FastAPI's auto-generated Swagger UI).

### Run tests

```bash
pytest
```

---

## Current Status

✅ JWT authentication with rotating refresh tokens + reuse detection
✅ RBAC (organizer / customer roles)
✅ Event creation, scoped to authenticated organizer
✅ Centralized exception handling
✅ Alembic-managed schema history
✅ Integration test coverage on auth flows
🚧 Seat management, bookings, payments
🚧 Multi-tenancy isolation model (organization-level, beyond role-based access)
🚧 Docker Compose setup
🚧 Redis + Celery for async ticket/payment processing

---

## Roadmap

- [ ] Seat inventory + booking with concurrency-safe seat locking
- [ ] Payment integration (mock/sandbox)
- [ ] Redis-backed caching for event listings
- [ ] Celery for async notification/email dispatch
- [ ] Dockerized local dev environment
- [ ] Declarative role-based authorization dependency (replacing inline role checks)

---

## License

MIT
