def test_transcription_invalid_file_upload(client):
    """Test that accidentally uploading a non-text file (such as a wav file)
    triggers an error"""
    import io
    data = {'transcriptionFile': (io.BytesIO(b"Wrong extension/format"), 'badFileFormat.xyz')}
    response = client.post(
        ('/v0.1/transcription/fromFile'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 415

    import json
    wav_response_data = json.loads(response.data.decode('utf8'))
    assert wav_response_data['status'] == 415

def test_transcription_invalid_wav_file_upload(client):
    """Test that accidentally uploading a non-text file (such as a wav file)
    triggers an error"""
    import io
    WAV_MAGIC_BYTES = b'RIFF....WAVE'
    data = {'transcriptionFile': (io.BytesIO(WAV_MAGIC_BYTES), 'accidental_wav_file.wav')}
    response = client.post(
        ('/v0.1/transcription/fromFile'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 415

    import json
    wav_response_data = json.loads(response.data.decode('utf8'))
    assert wav_response_data['status'] == 415



def test_transcription_uploads_endpoint(client):
    """Test transcription upload endpoint works"""
    import io
    phonemes = "ɖ ɯ ɕ i k v̩"
    data = {'transcriptionFile': (io.BytesIO(phonemes.encode('utf-8')), 'test_transcription_file.phonemes')}
    response = client.post(
        ('/v0.1/transcription/fromFile'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201

    import json
    transcription_response_data = json.loads(response.data.decode('utf8'))
    assert transcription_response_data['id']


def test_transcription_pagination(client):
    """Test that we can get pagination of results"""
    import io
    for t in range(10):
        phonemes = "test "+ str(t)
        filename = 'test_transcription_file{}.phonemes'.format(t)
        data = {'transcriptionFile': (io.BytesIO(phonemes.encode('utf-8')), filename)}
        response = client.post(
            ('/v0.1/transcription/fromFile'),
            data=data,
            content_type='multipart/form-data'
        )
        assert response.status_code == 201

    payload = {"pageSize": 6, "pageNumber": 1}
    response = client.get(
        '/v0.1/transcription/',
        data=payload,
    )
    assert response.status_code == 200
    import json
    response_data = json.loads(response.data.decode('utf8'))
    assert len(response_data) == 6

    payload = {"pageSize": 6, "pageNumber": 2}
    response = client.get(
        '/v0.1/transcription/',
        params=payload,
    )
    assert response.status_code == 200
    response_data = json.loads(response.data.decode('utf8'))
    assert len(response_data) == 4 # only 4 items remaining