"""Tests for model related endpoints"""

def test_invalid_min_max_steps(client, create_corpus):
    corpus_id = create_corpus()
    data = {
        "corpusID": corpus_id,
        "maximumEpochs": 10,
        "minimumEpochs": 100,
        "name": "Bad mix max model"
    }

    import json
    response = client.post(
        '/v0.1/model',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400

def test_invalid_epoch_steps(client, create_corpus):
    import json
    corpus_id = create_corpus()
    data = {
        "corpusID": corpus_id,
        "maximumEpochs": 5,
        "minimumEpochs": -1,
        "name": "Bad minimum epoch"
    }

    response = client.post(
        '/v0.1/model',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 400

    data = {
        "corpusID": corpus_id,
        "maximumEpochs": -10,
        "minimumEpochs": 5,
        "name": "Bad maximum epoch"
    }

    response = client.post(
        '/v0.1/model',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 400


def test_invalid_early_stopping(client, create_corpus):
    corpus_id = create_corpus()
    import json
    data = {
        "corpusID": corpus_id,
        "earlyStoppingSteps": -1,
        "name": "Bad maximum epoch"
    }

    response = client.post(
        '/v0.1/model',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 400

def test_invalid_LER(client, create_corpus):
    """Tests that bogus values for maximum error rates are rejected"""
    corpus_id = create_corpus()
    import json

    data = {
        "corpusID": corpus_id,
        "maxTrainingLER": -1,
        "name": "Bad maximum epoch"
    }

    response = client.post(
        '/v0.1/model',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 400

    data = {
        "corpusID": corpus_id,
        "maxValidationLER": -1,
        "name": "Bad maximum epoch"
    }
    response = client.post(
        '/v0.1/model',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 400

def test_create_model(client, create_corpus):
    """Test that we can create a model from the API"""
    import json
    corpus_id = create_corpus()

    model_data = {
        "name": "Test model",
        "beamWidth": 1,
        "corpusID": corpus_id,
        "decodingMergeRepeated": True,
        "earlyStoppingSteps": 1,
        "numberLayers": 2,
        "hiddenSize": 2,
        "maximumEpochs": 2,
        "minimumEpochs": 1,
    }

    response = client.post(
        '/v0.1/model',
        data=json.dumps(model_data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201

