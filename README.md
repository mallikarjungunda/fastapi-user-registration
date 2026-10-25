# FastAPI User Registration

A small user-registration REST API built with FastAPI, SQLModel, and SQLite.
It supports creating, listing, retrieving, updating, and deleting users. New
passwords are hashed with `pwdlib` before they are stored.

## Requirements

- Python 3.10 or later
- `pip`

## Installation

From the repository root, create a virtual environment and install the
development dependencies (which include the runtime requirements):

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements-dev.txt
```

To install only the runtime dependencies, use `requirements.txt` instead.

## Run the application

Start the development server from the repository root:

```bash
./.venv/bin/python -m uvicorn app.main:app --reload
```

By default, the API is available at <http://127.0.0.1:8000>. If that port is
already in use, specify another port, for example:

```bash
./.venv/bin/python -m uvicorn app.main:app --reload --port 8001
```

The root endpoint returns a simple greeting. Interactive API documentation is
available at `/docs`, ReDoc at `/redoc`, and the generated OpenAPI schema at
`/openapi.json`.

## API endpoints

| Method | Path | Description | Success response |
| --- | --- | --- | --- |
| `GET` | `/` | Service greeting | `200` |
| `POST` | `/users` | Register a user | `201` |
| `GET` | `/users` | List users | `200` |
| `GET` | `/users/{user_id}` | Get one user | `200` |
| `PATCH` | `/users/{user_id}` | Update a user's name | `200` |
| `DELETE` | `/users/{user_id}` | Delete a user | `204` |

### Register a user

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H 'Content-Type: application/json' \
  -d '{"name":"Ada Lovelace","email":"ada@example.com","password":"a-long-test-password"}'
```

`name` must be 1–100 characters and contain a non-whitespace character.
`email` must be valid. `password` must be 12–128 characters. Extra request
fields are rejected. Emails are stored in lowercase, names are trimmed, and
the response never includes a password or password hash. Registering an email
that already exists (case-insensitively) returns `409 Conflict`.

### List users

```bash
curl 'http://127.0.0.1:8000/users?offset=0&limit=20'
```

`offset` defaults to `0` and must be non-negative. `limit` defaults to `20` and
must be between `1` and `100`.

### Get, update, or delete a user

Replace `1` with the user's ID:

```bash
curl http://127.0.0.1:8000/users/1

curl -X PATCH http://127.0.0.1:8000/users/1 \
  -H 'Content-Type: application/json' \
  -d '{"name":"Ada Byron"}'

curl -X DELETE http://127.0.0.1:8000/users/1
```

The update request requires a valid `name`; extra fields are rejected. Requests
for a user ID that does not exist return `404 Not Found`.

## Database

The application uses SQLite at `./users.db`, relative to the process working
directory. Tables are created automatically at application startup. The
database persists between runs and is ignored by Git; avoid using real or
sensitive user data in local development.

## Tests

Install test dependencies with `requirements-dev.txt`, then run all tests and
measure application coverage:

```bash
./.venv/bin/python -m pytest --cov=app --cov-report=term-missing
```

The suite includes unit tests and HTTP-level functional tests. Functional API
scenarios use Gherkin with `pytest-bdd`; they are in
`tests/functional/features/`, with Python step definitions alongside them.
Run only those scenarios with:

```bash
./.venv/bin/python -m pytest tests/functional
```

Tests use an isolated temporary SQLite database and do not use the local
`users.db`.

## Postman

Import [`postman/fastapi-user-registration.postman_collection.json`](postman/fastapi-user-registration.postman_collection.json)
into Postman. The collection exercises the API endpoints and includes response
assertions. It defaults to `http://127.0.0.1:8000`; change its `baseUrl`
collection variable if the server uses another port. Run the collection in
order for the registration request to set the user ID and email used by later
requests. See [`postman/README.md`](postman/README.md) for details.

## Project layout

```text
app/
  main.py              FastAPI application and startup lifecycle
  database.py          SQLite engine, table creation, and session dependency
  models.py            SQLModel database models
  schemas.py           Request and response validation schemas
  security.py          Password hashing and verification helpers
  routers/users.py     User API routes
tests/
  functional/          Gherkin API scenarios and step definitions
  test_*.py            Unit and API tests
postman/               Postman collection and usage notes
openspec/               OpenSpec configuration
```
