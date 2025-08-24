import pytest

from testcontainers.postgres import PostgresContainer

from sqlalchemy import create_engine, Engine
from booking.adapters.gateways.repositories.sql_entities.sql_base import BaseModel
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from booking.app import app
from booking.adapters.dependencies.get_session import get_db_url


@pytest.fixture(scope="session")
def postgres_container():
    postgres = PostgresContainer(
        image="postgres:17.6-alpine",
        port=5432,
    )

    postgres.start()
    yield postgres

    postgres.stop()


def get_test_db_url(postgres_container: PostgresContainer) -> str:
    return postgres_container.get_connection_url()


@pytest.fixture(scope="session")
def test_engine(postgres_container: PostgresContainer):
    connection_url = postgres_container.get_connection_url()
    engine = create_engine(
        connection_url,
        pool_size=1,
        max_overflow=0,
        pool_pre_ping=True,
    )
    BaseModel.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="session")
def test_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_client(postgres_container: PostgresContainer, test_engine: Engine):
    app.dependency_overrides[get_db_url] = lambda: get_test_db_url(postgres_container)

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
