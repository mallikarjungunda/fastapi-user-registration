# Instructions for Claude

Follow the repository-wide guidance in [`AGENTS.md`](AGENTS.md) for project
structure, setup, coding conventions, validation, and OpenSpec workflow.

The application is a FastAPI service with entry point `app.main:app`. Install
dependencies from `requirements.txt` and run it with
`python -m uvicorn app.main:app --reload`. Its SQLite database is created as
`users.db` in the current working directory and must remain uncommitted.

When changing user registration or persistence, keep `app/models.py`,
`app/schemas.py`, and `app/routers/users.py` consistent. Preserve password
hashing and ensure responses never expose password data. Validate changes
using the commands and isolated-database guidance in `AGENTS.md`.
