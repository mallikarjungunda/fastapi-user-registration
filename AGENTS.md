# Agent guidance

## Project overview

This repository contains a small FastAPI user-registration API. The application
entry point is `app.main:app`; user endpoints are in `app/routers/users.py`.
The API uses SQLModel with SQLite, Pydantic request/response schemas, and
`pwdlib` for password hashing.

## Setup and running

- Install runtime and test dependencies with
  `./.venv/bin/python -m pip install -r requirements-dev.txt`.
- Start the development server with
  `./.venv/bin/python -m uvicorn app.main:app --reload`.
- The root endpoint is `GET /`; FastAPI's interactive docs are at `/docs`.
- SQLite uses `./users.db` relative to the process working directory. Startup
  creates tables automatically. Do not commit the database or other local data.

## Code conventions

- Keep route handlers in `app/routers/`, database configuration and session
  dependencies in `app/database.py`, SQLModel tables in `app/models.py`, and
  API validation/serialization models in `app/schemas.py`.
- Keep the SQLModel `User` fields aligned with the fields used by routes and
  schemas when changing the user data model.
- Use request and response models for API boundaries. Never return password
  hashes or plaintext passwords in API responses.
- Hash passwords with the existing helpers in `app/security.py`; do not store
  plaintext passwords.
- Follow the existing FastAPI/SQLModel patterns and make narrow, focused
  changes.

## Validation

- Run `./.venv/bin/python -m compileall -q app` for a quick syntax check.
- Run `./.venv/bin/python -m pytest --cov=app --cov-report=term-missing`
  for tests and coverage.
- Run `./.venv/bin/python -m pytest tests/functional` for HTTP-level API
  functional tests written with Gherkin and pytest-bdd. Scenarios are in
  `tests/functional/features/`; step definitions are grouped by API area.
- Import `postman/fastapi-user-registration.postman_collection.json` into
  Postman to run the API requests and response assertions.
- API tests use an isolated temporary SQLite database; do not alter the
  developer's `users.db` during validation.

## Specification workflow

OpenSpec is initialized with the `spec-driven` schema. For significant feature
or behavior changes, use the repository's OpenSpec skills under
`.github/skills/openspec-*` to propose, apply, and archive a change. Keep
specifications consistent with the implemented API.
