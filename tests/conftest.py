import pytest

from app import app


@pytest.fixture()
def app_created():
    app_created = app
    yield app_created


@pytest.fixture()
def client(app_created):
    return app_created.test_client()
