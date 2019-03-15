def test_invalid_file_upload(init_database, client):
    """Test that accidentally uploading a text file (such as a phonemes file)
    triggers an error, this endpoint needs a compressed file type uploaded to it."""
    import io
    data = {'utterancesFile': (io.BytesIO(b"this is not a compressed file"), 'accidental.phonemes')}
    response = client.post(
        ('/v0.1/bulk_data/utterances'),
        data=data,
        content_type='multipart/form-data'
    )
    assert response.status_code == 415

    import json
    upload_response_data = json.loads(response.data.decode('utf8'))
    assert upload_response_data['status'] == 415
