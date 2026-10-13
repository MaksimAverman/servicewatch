import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import scheduler, storage
from app.db import Base


@pytest.fixture
def session_factory():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def fake_check(url):
    return {
        "status_code": 200,
        "response_time_ms": 1.0,
        "is_up": "down" not in url,
        "error": None,
    }


def test_run_all_checks_stores_one_check_per_target(session_factory, monkeypatch):
    monkeypatch.setattr(scheduler, "check_url", fake_check)
    with session_factory() as db:
        storage.add_target(db, "https://up.example.com/")
        storage.add_target(db, "https://down.example.com/")

    assert scheduler.run_all_checks(session_factory) == 2

    with session_factory() as db:
        checks = storage.list_checks(db)
    assert [c.target_id for c in checks] == [1, 2]
    assert [c.is_up for c in checks] == [True, False]


def test_run_all_checks_with_no_targets(session_factory):
    assert scheduler.run_all_checks(session_factory) == 0
