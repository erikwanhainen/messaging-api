import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app.db import engine, get_session
from app.models import Message

# TODO: Use a separate test enviroment database


@pytest.fixture
def client(db_session):
    def override_get_session():
        return db_session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def create_message(db_session):
    def _create_message(recipient: str, content: str, read: bool = False):
        message = Message(recipient=recipient, content=content, read=read)
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        return message

    return _create_message
