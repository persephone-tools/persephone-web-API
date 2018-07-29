import os

import connexion
from connexion.resolver import RestyResolver
import pytest

import api

# API version prefix
API_VERSION = "v0.1"

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

flask_app.config['DEBUG'] = True
flask_app.config['TESTING'] = True

@pytest.fixture
def client(tmpdir):
    """Create a test client to send requests to"""
    flask_app.config['BASE_UPLOAD_DIRECTORY'] = os.path.join(str(tmpdir), 'test_uploads')
    flask_app.config['CORPUS_PATH'] = os.path.join(str(tmpdir), 'corpus')

    from api.upload_config import configure_uploads
    configure_uploads(flask_app)
    with flask_app.test_client() as c:
        yield c


@pytest.fixture
def upload_audio(client):
    """Fixture for convenience in sending requests to the audio endpoint"""
    import io
    def _make_audio(audio_data, filename):
        """Create a file with appropriate WAV magic bytes and encoding"""
        WAV_MAGIC_BYTES = b'RIFF....WAVE'
        data = {'audioFile': (io.BytesIO(WAV_MAGIC_BYTES+audio_data.encode('utf-8')),
                             filename)
        }
        return client.post(
            ('/{}/audio'.format(API_VERSION)),
            data=data,
            content_type='multipart/form-data'
        )

    return _make_audio

@pytest.fixture
def upload_transcription(client):
    """Fixture for convenience in sending requests to the transcription endpoint"""
    import io
    def _make_transcription(transcription_data, filename):
        """Create a file with appropriate encoding"""
        data = {'transcriptionFile': (io.BytesIO(transcription_data.encode('utf-8')), filename)}
        return client.post(
            ('/{}/transcription'.format(API_VERSION)),
            data=data,
            content_type='multipart/form-data'
        )

    return _make_transcription