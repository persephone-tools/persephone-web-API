def test_backend(client):
    """Test information about the transcriber library on the backend is provided"""
    response = client.get('/v0.1/backend')
    assert response.status_code == 200

def test_label_support(client):
    """Test endpoint that supplies information about supported label types."""
    response = client.get('/v0.1/backend/labelTypes')
    assert response.status_code == 200
