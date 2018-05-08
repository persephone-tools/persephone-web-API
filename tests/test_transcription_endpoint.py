def test_transcription_uploads_endpoint(client):
    """Test transcription upload endpoint works"""
    import io
    phonemes = "ɖ ɯ ɕ i k v̩"
    data = {'transcriptionFile': (io.BytesIO(phonemes.encode('utf-8')), 'test_transcription_file.phonemes')}
    response = client.post(
        ('/v0.1/transcription'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201

    import json
    transcription_response_data = json.loads(response.data.decode('utf8'))
    assert transcription_response_data['id']
