"""Tests for label related functionality"""

def test_label_creation(client):
    """Test that we can create a label"""
    import json
    data = {
        "phoneticLabel": "a",
    }

    response = client.post(
        '/v0.1/label',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    assert response
    assert response.status_code == 201

def test_label_listing(client):
    """Test that we can create some labels then list all of the available ones"""
    import json
    data = {
        "phoneticLabel": "a",
    }

    response = client.post(
        '/v0.1/label',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 201

    data = {
        "phoneticLabel": "b",
    }

    response = client.post(
        '/v0.1/label',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201

    response = client.get(
        '/v0.1/label',
    )

    assert response
