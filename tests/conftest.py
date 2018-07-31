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
    tmpdir.mkdir('test_uploads')
    app.config['BASE_UPLOAD_DIRECTORY'] = os.path.join(str(tmpdir), 'test_uploads')
    tmpdir.mkdir('corpus')
    app.config['CORPUS_PATH'] = os.path.join(str(tmpdir), 'corpus')

    from persephone_api.upload_config import configure_uploads
    configure_uploads(app)
    with app.test_client() as c:
        yield c

import wave
import struct

@pytest.fixture
def upload_audio(client):
    """Fixture for convenience in sending requests to the audio endpoint"""
    import io
    def _make_audio(audio_data, filename: str, framerate: float=44100.00, duration: float=1):
        """Create a file with appropriate WAV magic bytes and encoding

        :audio_data: raw frame data to be placed into the wav file
        :filename: the filename that will be uploaded
        :framerate: hertz
        :duration: seconds this file will go for
        """
        #WAV_MAGIC_BYTES = b'RIFF....WAVE'
        amp = 8000.0 # amplitude
        wav_data = io.BytesIO()
        wav_file = wave.open(wav_data, "wb")
        # wav params
        nchannels = 1
        sampwidth = 2
        framerate = int(framerate)
        nframes = int(framerate*duration)
        comptype = "NONE"
        compname = "not compressed"
        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        # write the contents
        for s in audio_data:
            wav_file.writeframes(struct.pack('h', int(s*amp/2)))
        wav_file.close()

        # Seek to start of the audio stream data
        wav_data.seek(0)

        data = {'audioFile': (wav_data, filename)}
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