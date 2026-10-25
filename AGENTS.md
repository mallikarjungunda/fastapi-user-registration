# Agent guidance

## Project overview

This repository contains a small FastAPI user-registration API. The application
entry point is `app.main:app`; user endpoints are in `app/routers/users.py`.
The API uses SQLModel with SQLite, Pydantic request/response schemas, and
`pwdlib` for password hashing.

## Setup and running

- Install dependencies with `python -m pip install -r requirements.txt`.
- Start the development server with `python -m uvicorn app.main:app --reload`.
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

- Run `python -m compileall -q app` for a quick syntax check.
- Exercise changed API behavior with FastAPI's `TestClient` and a temporary
  working directory/database so checks do not alter the developer's
  `users.db`.
- There is currently no checked-in automated test suite or test configuration;
  do not claim tests passed unless they were actually run.

## Specification workflow

OpenSpec is initialized with the `spec-driven` schema. For significant feature
or behavior changes, use the repository's OpenSpec skills under
`.github/skills/openspec-*` to propose, apply, and archive a change. Keep
specifications consistent with the implemented API.
