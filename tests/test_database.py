from sqlmodel import SQLModel, create_engine

from app import database
from app.models import User


def test_create_tables_uses_configured_engine(tmp_path, monkeypatch):
    engine = create_engine(f"sqlite:///{tmp_path / 'tables.db'}")
    monkeypatch.setattr(database, "engine", engine)

    database.create_tables()

    assert User.__tablename__ in SQLModel.metadata.tables
    with engine.connect() as connection:
        table_names = connection.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).scalars()
        assert User.__tablename__ in table_names
    engine.dispose()


def test_get_session_yields_and_closes_session(monkeypatch):
    engine = object()
    context = None

    class SessionContext:
        def __init__(self, configured_engine):
            assert configured_engine is engine
            self.closed = False

        def __enter__(self):
            return "test-session"

        def __exit__(self, *exc_info):
            self.closed = True

    def create_session(configured_engine):
        nonlocal context
        context = SessionContext(configured_engine)
        return context

    monkeypatch.setattr(database, "engine", engine)
    monkeypatch.setattr(database, "Session", create_session)

    session_generator = database.get_session()
    session = next(session_generator)

    assert session == "test-session"
    session_generator.close()
    assert context.closed
