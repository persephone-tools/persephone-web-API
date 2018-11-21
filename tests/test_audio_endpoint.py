def test_invalid_file_upload(init_database, client):
    """Test that accidentally uploading a text file (such as a phonemes file)
    triggers an error"""
    import io
    data = {'audioFile': (io.BytesIO(b"this is not a wav file"), 'accidental.phonemes')}
    response = client.post(
        ('/v0.1/audio'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 415

    import json
    wav_response_data = json.loads(response.data.decode('utf8'))
    assert wav_response_data['status'] == 415


def test_audio_uploads_endpoint(init_database, client):
    """Test audio upload endpoint works"""
    import io
    WAV_MAGIC_BYTES = b'RIFF....WAVE'
    data = {'audioFile': (io.BytesIO(WAV_MAGIC_BYTES), 'test_wav_file.wav')}
    response = client.post(
        ('/v0.1/audio'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201

    import json
    wav_response_data = json.loads(response.data.decode('utf8'))
    assert wav_response_data['id']

def test_audio_search_endpoint(init_database, client):
    """Test that the audio search endpoint works with no parameters provided"""
    import io
    WAV_MAGIC_BYTES = b'RIFF....WAVE'
    data = {'audioFile': (io.BytesIO(WAV_MAGIC_BYTES), 'test_wav_file.wav')}
    response = client.post(
        ('/v0.1/audio'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201

    import json
    wav_response_data = json.loads(response.data.decode('utf8'))
    assert wav_response_data['id']
    wav_id = wav_response_data['id']
    response = client.get(
        '/v0.1/audio',
    )
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf8'))
    assert response_data[0]['id'] == wav_id


def test_audio_pagination(init_database, client):
    """Test that we can get pagination of results"""
    import io
    WAV_MAGIC_BYTES = b'RIFF....WAVE'
    for t in range(10):
        filename = 'test_wav_file_{}.wav'.format(t)
        data = {'audioFile': (io.BytesIO(WAV_MAGIC_BYTES), filename)}
        response = client.post(
            ('/v0.1/audio'),
            data=data,
            content_type='multipart/form-data'
        )
        assert response.status_code == 201

    response = client.get(
        '/v0.1/audio?pageSize=6&pageNumber=1',
    )
    assert response.status_code == 200
    import json
    response_data = json.loads(response.data.decode('utf8'))
    assert len(response_data) == 6

    response = client.get(
        '/v0.1/audio?pageSize=6&pageNumber=2',
    )
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf8'))
    assert len(response_data) == 4 # only 4 items remaining