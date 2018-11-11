"""Test corpus API endpoints"""

def test_corpus_creation(client, upload_audio, upload_transcription, create_utterance, create_sine):
    """Test that we are able to create a corpus object via the API"""
    import json

    # Create mock audio uploads
    response = upload_audio(create_sine(note="A"), filename="a.wav")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_a = wav_response_data['id']

    response = upload_audio(create_sine(note="B"), filename="b.wav")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_b = wav_response_data['id']

    response = upload_audio(create_sine(note="C"), filename="c.wav")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_c = wav_response_data['id']

    # Create mock transcription uploads
    response = upload_transcription("A", filename="a.phonemes")
    assert response.status_code == 201
    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id_a = transcription_response_data['id']

    response = upload_transcription("B", filename="b.phonemes")
    assert response.status_code == 201
    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id_b = transcription_response_data['id']

    response = upload_transcription("C", filename="c.phonemes")
    assert response.status_code == 201
    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id_c = transcription_response_data['id']

    response = create_utterance(wav_id_a, transcription_id_a)
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    utterance_id_a = utterance_response_data['id']

    response = create_utterance(wav_id_b, transcription_id_b)
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    utterance_id_b = utterance_response_data['id']

    response = create_utterance(wav_id_c, transcription_id_c)
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    utterance_id_c = utterance_response_data['id']

    data = {
        "name": "Test Corpus",
        "labelType": "phonemes",
        "featureType": "fbank",
        "preprocessed": "false",
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

    corpus_response_data = json.loads(response.data.decode('utf8'))
    assert corpus_response_data['partition']
