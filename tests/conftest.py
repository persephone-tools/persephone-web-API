"""Configration for pytest to run the test suite"""
import os
import pytest

from persephone_api.app import create_app
from persephone_api.settings import TestConfig

app = create_app(TestConfig)

# API version prefix
API_VERSION = "v0.1"

from persephone_api import db
db.init_app(app)

# create DB tables
with app.app_context():
    db.create_all()

# configure upload paths
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #max 64 MB file upload


@pytest.fixture
def client(tmpdir):
    """Create a test client to send requests to"""
    app.config['BASE_UPLOAD_DIRECTORY'] = os.path.join(str(tmpdir), 'test_uploads')
    app.config['CORPUS_PATH'] = os.path.join(str(tmpdir), 'corpus')

    from api.upload_config import configure_uploads
    configure_uploads(app)
    with app.test_client() as c:
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