# Postman collection

Import `fastapi-user-registration.postman_collection.json` into Postman. Start
the API from the repository root:

```bash
./.venv/bin/python -m uvicorn app.main:app --reload
```

The collection defaults to `http://127.0.0.1:8000`. If the app is running on a
different port, edit the collection's `baseUrl` variable (for example,
`http://127.0.0.1:8001`).

Run the collection in order to exercise all endpoints and assertions. The
registration request generates a unique email and stores the created `userId`;
subsequent user requests use that variable. The duplicate-email request must
run after registration. The collection uses the app's configured SQLite
database, so requests create and delete a test user there.

Covered endpoints include the root greeting, OpenAPI document, Swagger UI,
ReDoc, user registration/list/get/update/delete, invalid registration,
duplicate email, invalid pagination, and missing-user errors.
