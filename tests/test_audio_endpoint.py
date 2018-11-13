def test_invalid_file_upload(client):
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


def test_audio_uploads_endpoint(client):
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
