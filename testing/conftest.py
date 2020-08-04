"""
This file defines some fixtures for testing flask app
"""
import pytest
from web.app import create_app

@pytest.fixture
def app():
    """ Create a flask app object."""
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    """A test client for the flask app."""
    return app.test_client()
