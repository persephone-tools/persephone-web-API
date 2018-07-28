def test_corpus_creation(client, upload_audio, upload_transcription):
    """Test that we are able to create a corpus object via the API"""
    import json

    # Create mock audio uploads
    response = upload_audio("audio a", filename="a.wav")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_a = wav_response_data['id']

    response = upload_audio("audio b", filename="b.wav")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_b = wav_response_data['id']

    response = upload_audio("audio c", filename="c.wav")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_c = wav_response_data['id']

    # Create mock transcription uploads
    response = upload_transcription("a", filename="a.phonemes")
    assert response.status_code == 201
    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id_a = transcription_response_data['id']

    response = upload_transcription("b", filename="b.phonemes")
    assert response.status_code == 201
    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id_b = transcription_response_data['id']

    response = upload_transcription("c", filename="c.phonemes")
    assert response.status_code == 201
    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id_c = transcription_response_data['id']

    data = {
        "audioId": wav_id_a,
        "transcriptionId": transcription_id_a
    }

    response = client.post(
        '/v0.1/utterance',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    utterance_id_a = utterance_response_data['id']

    data = {
        "audioId": wav_id_b,
        "transcriptionId": transcription_id_b
    }

    response = client.post(
        '/v0.1/utterance',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    utterance_id_b = utterance_response_data['id']

    data = {
        "audioId": wav_id_c,
        "transcriptionId": transcription_id_c
    }

    response = client.post(
        '/v0.1/utterance',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    utterance_id_c = utterance_response_data['id']

    data = {
        "name": "Test Corpus",
        "label_type": "phonemes",
        "feature_type": "fbank",
        "testing": [
            utterance_id_a
        ],
        "training": [
            utterance_id_b
        ],
        "validation": [
            utterance_id_c
        ]
    }

    response = client.post(
        '/v0.1/corpus',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 201