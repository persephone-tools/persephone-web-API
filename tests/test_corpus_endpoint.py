def test_corpus_creation(upload_audio):
    """Test that we are able to create a corpus object via the API"""
    import json

    # Create mock audio uploads
    response = upload_audio("audio a")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_a = wav_response_data['id']

    response = upload_audio("audio b")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_b = wav_response_data['id']

    response = upload_audio("audio c")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_c = wav_response_data['id']