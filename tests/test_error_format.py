"""Tests for the error reporting message format"""

def validate_error_fields(decoded_response_data):
    """Validate that the error API fields are present"""
    assert "detail" in decoded_response_data
    assert "type" in decoded_response_data
    assert "status" in decoded_response_data

def test_audio_uploads_endpoint(client):
    """Test audio upload endpoint works"""
    import io
    WAV_MAGIC_BYTES = b'RIFF....WAVE'
    data = {'badName': (io.BytesIO(WAV_MAGIC_BYTES), 'test_wav_file.wav')}
    response = client.post(
        ('/v0.1/audio'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 400
    import json
    wav_response_data = json.loads(response.data.decode('utf8'))
    validate_error_fields(wav_response_data)