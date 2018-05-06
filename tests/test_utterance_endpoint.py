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
