def test_backend(client):
    """Test information about the transcriber library on the backend is provided"""
    response = client.get('/v0.1/backend')
    assert response.status_code == 200

def test_label_support(client):
    """Test endpoint that supplies information about supported label types."""
    response = client.get('/v0.1/backend/labelTypes')
    assert response.status_code == 200

def test_feature_support(client):
    """Test endpoint that supplies information about supported feature types."""
    response = client.get('/v0.1/backend/featureTypes')
    assert response.status_code == 200

def test_accepted_filetypes(client):
    """Test the accepted file types endpoint"""
    import json

    response = client.get('/v0.1/backend/acceptedFiles')
    assert response.status_code == 200

    accepted_files_response_data = json.loads(response.data.decode('utf8'))
    assert "audio" in accepted_files_response_data
    assert "transcription" in accepted_files_response_data
    assert "wav" in accepted_files_response_data["audio"]
