import os

import connexion
from connexion.resolver import RestyResolver
import pytest

import api

app = connexion.FlaskApp(__name__)
app.add_api('../swagger/api_spec.yaml', resolver=RestyResolver('api'))

# fetch underlying flask app from the connexion app
flask_app = app.app

# configure the DB
# in-memory sqlite DB for testing
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from api import db
db.init_app(flask_app)

# create DB tables
with flask_app.app_context():
    db.create_all()

# configure upload paths
flask_app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #max 64 MB file upload
flask_app.config['BASE_UPLOAD_DIRECTORY'] = os.path.join(os.getcwd(), 'test_uploads')

from api.upload_config import configure_uploads
configure_uploads(flask_app)

flask_app.config['DEBUG'] = True
flask_app.config['TESTING'] = True

@pytest.fixture
def client():
    """Create a test client to send requests to"""
    with flask_app.test_client() as c:
        yield c

