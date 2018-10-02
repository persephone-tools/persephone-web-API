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
    assert response.status_code == 201

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

def test_label_NFC_uniqueness(client):
    """Test that unicode characters that are the same according to NFC are
    properly recognized as duplicates at the database level.

    We are using NFC normalization internally, this test may have to change if
    the normalization is changed.

    Refer to https://unicode.org/reports/tr15/ for details about how this works.
    """
    import unicodedata
    single_character_ä = "\u00E4"
    combining_diaeresis_ä = "\u0061\u0308"
    assert unicodedata.normalize("NFC", single_character_ä) == unicodedata.normalize("NFC", combining_diaeresis_ä)

    import json
    data = {
        "phoneticLabel": single_character_ä,
    }
    response = client.post(
        '/v0.1/label',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201

    data = {
        "phoneticLabel": combining_diaeresis_ä,
    }

    # Duplicate as per NFC normalization should return 4xx code
    response = client.post(
        '/v0.1/label',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert 400 <= response.status_code < 500


def test_corpus_labels(client, create_corpus):
    """test that creating a corpus creates the right set of labels"""
    import json
    corpus_id = create_corpus()
    expected_labels = {'A', 'B', 'C'}

    response = client.get(
        '/v0.1/corpus/labels/{}'.format(corpus_id),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200
    label_response_data = json.loads(response.data.decode('utf8'))
    assert label_response_data['corpus']['id'] == corpus_id
    assert set(label_response_data['labels']) == expected_labels