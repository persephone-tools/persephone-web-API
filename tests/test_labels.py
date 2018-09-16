"""Tests for label related functionality"""

def test_label_creation(client):
    """Test that we can create a label"""
    import json
    data = {
        "label": "a",
    }

    response = client.post(
        '/v0.1/label',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    assert response
    assert response.status_code == 201
