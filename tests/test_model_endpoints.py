def test_invalid_min_max_steps(client):
    data = {
        "corpusID": 1,
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

def test_invalid_epoch_steps(client):
    import json
    data = {
        "corpusID": 1,
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
        "corpusID": 1,
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


def test_invalid_early_stopping(client):
    import json
    data = {
        "corpusID": 1,
        "earlyStoppingSteps": -1,
        "name": "Bad maximum epoch"
    }

    response = client.post(
        '/v0.1/model',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 400