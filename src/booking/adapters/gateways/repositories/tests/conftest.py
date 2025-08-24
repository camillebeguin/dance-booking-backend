import pytest

from testcontainers.postgres import PostgresContainer

from sqlalchemy import create_engine
from booking.adapters.gateways.repositories.sql_entities.sql_base import BaseModel
from sqlalchemy.orm import Session


@pytest.fixture(scope="session")
def postgres_container():
    postgres = PostgresContainer(
        image="postgres:17.6-alpine",
        port=5432,
    )

    postgres.start()
    yield postgres

    postgres.stop()


@pytest.fixture(scope="session")
def test_engine(postgres_container):
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
