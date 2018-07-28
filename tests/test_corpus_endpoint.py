def test_corpus_creation(upload_audio, upload_transcription):
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