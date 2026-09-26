# Multi-Tenant Event Booking & Ticketing Platform

A production-style backend for an event booking and ticketing system (think BookMyShow), built as a deep dive into backend architecture, authentication security, database design, testing, containerization, and CI/CD — not just "make the CRUD work," but "make it the way a real system would need to work."

This is a work-in-progress portfolio project. The goal isn't to ship every feature fast; it is to build the foundational layers — authentication, authorization, error handling, data access, testing, containerization, and CI — correctly before building the remaining features on top of them.

---

## Why this project

Most tutorial-style CRUD APIs stop at "it works." This project focuses on the engineering concerns that are usually skipped:

- **Secure, rotating refresh tokens** with reuse detection — not just a long-lived JWT.
- **Strict layered architecture** (router → service → repository) so business logic never leaks into HTTP handlers or SQL leaks into services.
- **Centralized, typed exception handling** instead of scattered `try/except` blocks and silent failures.
- **Migration-first schema management** with Alembic, so the database's history is reviewable rather than reconstructed from a live database.
- **Automated testing** with unit and integration tests using Pytest and FastAPI `TestClient`.
- **Redis-backed rate limiting** to protect authentication endpoints from excessive requests.
- **Dockerized local development** using Docker Compose for PostgreSQL and Redis.
- **Automated code quality checks** using Ruff.
- **CI pipeline with GitHub Actions** to automatically lint and test changes before they are merged into the protected `main` branch.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Database | PostgreSQL |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Authentication | JWT (access + rotating refresh tokens) |
| JWT Library | `python-jose` |
| Password Hashing | `pwdlib` / Argon2 |
| Cache / Rate Limiting | Redis |
| Testing | Pytest + FastAPI `TestClient` |
| Linting | Ruff |
| Containerization | Docker |
| Local Orchestration | Docker Compose |
| CI | GitHub Actions |
| Planned | Celery, payment integration |

---

## Architecture

The codebase follows a strict layered pattern. Each layer has exactly one responsibility.

```text
Router
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL
```

### Responsibilities

**Router**

- Handles HTTP concerns.
- Parses requests.
- Extracts authentication information.
- Calls service-layer functions.
- Returns HTTP responses.
- Does not contain business logic or direct database access.

**Service**

- Owns business logic.
- Handles authentication and token verification.
- Coordinates operations across repositories.
- Does not directly manage HTTP responses.

**Repository**

- Owns database access.
- Executes SQLAlchemy queries.
- Handles persistence-related operations.
- Does not contain business rules.

**Exceptions**

- Domain-specific exceptions can be raised from service and repository layers.
- Global exception handlers in `main.py` translate them into HTTP responses.

```text
                         ┌──────────────┐
                         │   PostgreSQL │
                         └──────▲───────┘
                                │
                         ┌──────┴───────┐
                         │  Repository  │
                         └──────▲───────┘
                                │
                         ┌──────┴───────┐
                         │    Service   │
                         └──────▲───────┘
                                │
                         ┌──────┴───────┐
                         │    Router    │
                         └──────▲───────┘
                                │
                             Request
```

This means a service function never returns an HTTP status code, and a router never directly touches SQLAlchemy.

---

## Project Structure

```text
app/
├── core/                 # config, security, DB session, exceptions, logging
├── models/               # SQLAlchemy ORM models
├── schemas/              # Pydantic request/response schemas
├── repository/           # Database access layer
├── services/             # Business logic layer
├── router/               # FastAPI route definitions
└── dependencies/         # Reusable FastAPI dependencies

alembic/
└── versions/             # Database migration history

tests/
├── unit/                 # Unit tests
└── integration/          # Integration/API tests

.github/
└── workflows/            # GitHub Actions CI workflows

Dockerfile                # Application container definition
docker-compose.yaml       # Local multi-container development environment
pyproject.toml            # Ruff/project tooling configuration
requirements.txt          # Python dependencies
```

---

# Authentication & Token Security

This is the part of the project that received the most deliberate attention.

## Access Tokens

Access tokens are short-lived JWTs that are signed and verified server-side.

They contain the user's identity through the `sub` claim and are not persisted in the database.

## Refresh Tokens — Rotation with Reuse Detection

Rather than using a single long-lived refresh token, the project implements **refresh token rotation with family-based reuse detection**.

- Every refresh token belongs to a **token family** identified by `family_id`.
- The family is created when the user logs in.
- Each refresh operation invalidates the current refresh token.
- A new refresh token is issued with the same `family_id`.
- If an already-used or revoked refresh token is presented again, the system treats it as potential token theft.
- The entire token family is revoked when reuse is detected.

Revocation is intentionally scoped:

- **Reuse detected on one device/session** → revoke that token family.
- **Log out everywhere / password change** → revoke all token families belonging to the user.

```text
Login
  │
  ▼
Create token family F1
  │
  ▼
Refresh Token V1
  │
  │ Access token expires
  ▼
POST /refresh
  │
  ▼
Is V1 already used?
  │
  ├── Yes ──► Revoke entire family F1
  │
  └── No
       │
       ▼
   Mark V1 as used
       │
       ▼
   Issue V2
   Same family F1
```

### Why this matters

If an attacker obtains a refresh token and attempts to reuse it after the legitimate client has already rotated it, the reuse can be detected and the affected session family can be revoked.

---

# Authorization

The application implements role-based access control with roles including:

- `organizer`
- `customer`
- `admin`

Authorization is enforced through authenticated user context rather than trusting sensitive identity information supplied by the client.

For example, when an organizer creates an event, the `organizer_id` is resolved from the authenticated user's JWT rather than being accepted from the request body.

This prevents a user from attempting to create an event on behalf of another organizer.

---

# Database

The project uses **PostgreSQL** with SQLAlchemy 2.0 and Alembic.

Core entities include:

- `users`
- `refresh_tokens`
- `events`
- `seats`
- `bookings`
- `booking_seats`
- `payments` *(in progress)*

### Key database design decisions

- Foreign keys used for filtering and joins are explicitly indexed.
- `organizer_id` is derived from authenticated user context.
- Seat availability is derived from the seat records rather than relying on a potentially stale cached counter.
- Database schema changes are managed through Alembic migrations.

---

# Error Handling

Domain exceptions are defined centrally and translated into HTTP responses through global exception handlers.

| Exception | HTTP Status |
|---|---:|
| `UserNotFound` | 404 |
| `UserAlreadyExists` | 409 |
| `InvalidCredentialError` | 401 |
| `UserNotAuthorized` | 403 |
| `InvalidTokenError` | 401 |
| `TokenExpiredError` | 401 |
| `CustomIntegrityError` | 409 |
| `DatabaseUnavailableError` | 503 |

Repository-layer database errors such as `IntegrityError` and `OperationalError` are translated into domain-specific exceptions so that service-layer code does not need to work directly with raw SQLAlchemy database exceptions.

---

# Rate Limiting

Redis is used to implement rate limiting for sensitive authentication endpoints.

Current limits include:

| Endpoint | Limit |
|---|---:|
| Login | 5 requests / 3 minutes |
| Register | 15 requests / minute |
| Refresh Token | 10 requests / 24 hours |

The rate limiter uses Redis as the shared counter store.

This provides a centralized rate-limiting mechanism rather than maintaining counters inside individual application processes.

---

# Testing

Testing is implemented using **Pytest** and FastAPI's `TestClient`.

The project contains unit and integration tests covering areas such as:

- Authentication
- JWT validation
- Refresh token rotation
- Refresh token reuse detection
- Repository behavior
- API endpoints
- Rate limiting
- Security-related edge cases

Run the complete test suite with:

```bash
pytest
```

The CI pipeline also runs the complete test suite, including tests that require Redis.

---

# Code Quality & Linting

The project uses **Ruff** for Python linting.

Run Ruff locally:

```bash
ruff check .
```

Ruff configuration is maintained in:

```text
pyproject.toml
```

Project-specific configuration is used where certain linting rules are not applicable to the framework or project conventions.

The goal is not simply to make the linter pass; Ruff is used to identify genuine code-quality issues and potential bugs before code reaches the protected `main` branch.

---

# Docker & Docker Compose

The project uses Docker for containerized local development.

Docker Compose is used to run the application's infrastructure dependencies together:

```text
┌─────────────────────────────┐
│       Docker Compose        │
│                             │
│  ┌─────────────┐            │
│  │ PostgreSQL  │            │
│  └─────────────┘            │
│                             │
│  ┌─────────────┐            │
│  │    Redis    │            │
│  └─────────────┘            │
└─────────────────────────────┘
```

The `docker-compose.yaml` defines the required services and their networking.

### Start the development services

```bash
docker compose up -d
```

### Stop the services

```bash
docker compose down
```

### View running containers

```bash
docker compose ps
```

The application container is built using the project's `Dockerfile`, while PostgreSQL and Redis are provided as separate services.

Docker Compose also provides the internal service networking required for the containers to communicate with each other.

---

# CI / Continuous Integration

The project uses **GitHub Actions** for continuous integration.

The CI pipeline automatically runs when code is pushed or when a pull request is opened or updated.

```text
Push / Pull Request
        │
        ▼
GitHub Actions
        │
        ▼
Setup Python
        │
        ▼
Install Dependencies
        │
        ├───────────────┐
        ▼               ▼
     Ruff Check       Redis
        │               │
        └───────┬───────┘
                ▼
             Pytest
                │
                ▼
          CI Pass / Fail
```

Redis is started as a Docker container during the test job because the rate-limiting tests require a real Redis service.

The CI process:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs dependencies.
4. Starts Redis using Docker Compose.
5. Waits for Redis to become healthy.
6. Runs Ruff.
7. Runs the complete Pytest suite.
8. Cleans up the Redis container.

---

# Branch Protection & Pull Requests

The `main` branch is protected.

Changes are developed on feature/development branches and submitted through pull requests.

```text
Development Branch
        │
        ▼
      Push
        │
        ▼
 GitHub Pull Request
        │
        ▼
 GitHub Actions
        │
        ├── Ruff
        └── Pytest
        │
        ▼
 Required Checks Pass
        │
        ▼
     Code Review
        │
        ▼
   Merge into main
```

Direct pushes to `main` are disabled.

This ensures that changes merged into `main` have passed the required CI checks.

---

# Getting Started

## Prerequisites

- Python 3.12+
- Docker
- Docker Compose
- Git

PostgreSQL and Redis can be run through Docker Compose.

## Clone the Repository

```bash
git clone https://github.com/SHEKHAR-Y/Multi-tenant-Event-Booking-Ticketing-Platform.git

cd Multi-tenant-Event-Booking-Ticketing-Platform
```

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create your local environment file:

```bash
cp .env.example .env
```

Configure the required values in `.env`, including:

- Database URL
- Redis URL
- Secret key
- JWT configuration
- Application configuration

## Start Infrastructure

Start PostgreSQL and Redis:

```bash
docker compose up -d postgres redis
```

Or start all Compose services:

```bash
docker compose up -d
```

## Apply Database Migrations

```bash
alembic upgrade head
```

## Run the API

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

FastAPI provides the interactive Swagger UI automatically.

---

# Development Commands

### Run tests

```bash
pytest
```

### Run Ruff

```bash
ruff check .
```

### Automatically fix supported Ruff issues

```bash
ruff check . --fix
```

### Format code

```bash
ruff format .
```

### Start Docker services

```bash
docker compose up -d
```

### Stop Docker services

```bash
docker compose down
```

### Check Docker services

```bash
docker compose ps
```

### Run migrations

```bash
alembic upgrade head
```

---

# Current Status

### Completed

- [x] JWT authentication
- [x] Short-lived access tokens
- [x] Rotating refresh tokens
- [x] Refresh token reuse detection
- [x] Token family-based revocation
- [x] Role-based access control
- [x] Organizer/customer/admin roles
- [x] Event creation
- [x] Authenticated organizer ownership
- [x] Centralized exception handling
- [x] Alembic database migrations
- [x] PostgreSQL integration
- [x] Redis integration
- [x] Redis-backed rate limiting
- [x] Unit and integration testing with Pytest
- [x] Docker configuration
- [x] Docker Compose local development environment
- [x] Ruff linting
- [x] GitHub Actions CI
- [x] Redis service in CI for Redis-dependent tests
- [x] Protected `main` branch with pull-request workflow

### In Progress

- [ ] Seat management
- [ ] Booking workflow
- [ ] Concurrency-safe seat reservation
- [ ] Payment integration
- [ ] Multi-tenant organization-level isolation
- [ ] Celery-based asynchronous processing
- [ ] Production deployment
- [ ] Production Redis deployment
- [ ] Production observability and monitoring

---

# Roadmap

- [ ] Implement seat inventory management
- [ ] Implement concurrency-safe seat locking
- [ ] Implement complete booking workflow
- [ ] Add payment integration using a sandbox/mock provider
- [ ] Redis-backed caching for event listings
- [ ] Celery for asynchronous notification/email processing
- [ ] Declarative role-based authorization dependencies
- [ ] Implement organization-level multi-tenancy isolation
- [ ] Production deployment
- [ ] Add production logging and monitoring
- [ ] Improve CI/CD pipeline
- [ ] Build and publish production Docker images

---

# License

MIT
