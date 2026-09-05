# Contributing

This is currently a solo portfolio project under active development, so the workflow here is intentionally lightweight. That said, issues, suggestions, and PRs are welcome.

## Reporting a bug or suggesting a change

Open an issue with:
- A clear title
- What's happening vs. what you expected
- Steps to reproduce (for bugs)

Check existing issues first to avoid duplicates.

## Making a change

1. **Comment on the relevant issue** before starting work, so effort isn't duplicated.
2. **Fork** the repo and create a branch off `main`:
   ```bash
   git checkout -b fix/short-description
   ```
   Use `fix/` for bugs, `feat/` for new features, `docs/` for documentation.
3. **Set up locally:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   alembic upgrade head
   ```
4. **Follow the existing architecture** — router → service → repository. Routers handle HTTP only; services own business logic and auth; repositories own DB access only. Domain exceptions are defined in `app/core/exceptions.py` and mapped to HTTP responses in `app/main.py`.
5. **Add or update tests** for any behavior change, and run:
   ```bash
   pytest
   ```
6. **Commit clearly:**
   ```
   fix: brief summary

   Longer explanation if needed.

   Fixes #<issue-number>
   ```
7. **Open a PR** against `main`, describing what changed, why, and how it was tested.

## Scope

Please keep PRs focused on a single issue/change — avoid bundling unrelated refactors, even small ones, into the same PR.
