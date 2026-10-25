from fastapi.testclient import TestClient

from app import main


def test_root_returns_greeting(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}


def test_startup_creates_tables(monkeypatch):
    calls = []
    monkeypatch.setattr(main, "create_tables", lambda: calls.append(True))

    with TestClient(main.app) as client:
        assert client.get("/").status_code == 200

    assert calls == [True]
