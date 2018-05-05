import os

import connexion
from connexion.resolver import RestyResolver
import pytest

import api

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('../swagger/api_spec.yaml', resolver=RestyResolver('api'))


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


def test_backend(client):
    """Test information about the transcriber library on the backend is provided"""
    response = client.get('/v0.1/backend')
    assert response.status_code == 200
