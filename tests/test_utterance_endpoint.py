def test_utterace_missing_IDs(client):
    """Test that using missing transcription/audio ID's will error out."""
    
    invalid_id = 99999

    data = {
        "audioId": invalid_id,
        "transcriptionId": invalid_id
    }

    import json

    response = client.post(
        '/v0.1/utterance',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400

def test_duplicate_utterance(client):
    """Test that if the same files are used that a duplicate utterance is not created"""
    import io
    import json

    # Create audio wav entry
    WAV_MAGIC_BYTES = b'RIFF....WAVE'
    data = {'audioFile': (io.BytesIO(WAV_MAGIC_BYTES), 'test_wav_file.wav')}
    response = client.post(
        ('/v0.1/audio'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201

    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id = wav_response_data['id']
    assert wav_id

    # Create transcription entry
    phonemes = "ɖ ɯ ɕ i k v̩"
    data = {'transcriptionFile': (io.BytesIO(phonemes.encode('utf-8')), 'test_transcription_file.phonemes')}
    response = client.post(
        ('/v0.1/transcription/fromFile'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 201

    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id = transcription_response_data['id']
    assert transcription_response_data['id']

    data = {
        "audioId": wav_id,
        "transcriptionId": transcription_id
    }

    response = client.post(
        '/v0.1/utterance',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    initial_utterance_id = utterance_response_data['id']
    assert initial_utterance_id


    # Duplicate utterance creation attempt
    response = client.post(
        '/v0.1/utterance',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 409
