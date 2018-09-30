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

    assert response

    data = {
        "phoneticLabel": "b",
    }

    response = client.post(
        '/v0.1/label',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response
    assert response.status_code == 201

    response = client.get(
        '/v0.1/label',
    )

    assert response
    assert response.status_code == 200

    label_response_data = json.loads(response.data.decode('utf8'))
    assert len(label_response_data) == 2

    labels = set(item['label'] for item in label_response_data)
    assert labels == {"a", "b"}


def test_label_uniqueness(client):
    """Test that adding the exact same label more than once doesn't add duplicate entries"""
    import json
    data = {
        "phoneticLabel": "dup",
    }

    response = client.post(
        '/v0.1/label',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201

    # Duplicate should return 4xx code
    response = client.post(
        '/v0.1/label',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert 400 <= response.status_code < 500
