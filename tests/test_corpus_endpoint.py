import math
def create_sine(note: str="A", seconds: float=1, framerate: float=44100.00) -> list:
    """Create a sine wave representing the frequency of a piano note 
    in octave 4 using the A440 tuning"""
    note_to_freq = {
        "C": 261.63,
        "C♯": 277.18, "D♭": 277.18,
        "D": 293.66,
        "E♭": 311.13, "D♯": 311.13,
        "E": 329.63,
        "F": 349.23,
        "F♯": 369.99, "G♭": 369.99, 
        "G": 392.00,
        "A♭": 415.30, "G♯": 415.30,
        "A": 440.00,
        "B♭": 466.16, "A♯": 466.16,
        "B": 493.88,
    }
    datasize = int(seconds * framerate)
    freq = note_to_freq[note]
    sine_list=[]
    for x in range(datasize):
        sine_list.append(math.sin(2*math.pi * freq * ( x/framerate)))
    return sine_list


def test_corpus_creation(client, upload_audio, upload_transcription):
    """Test that we are able to create a corpus object via the API"""
    import json

    # Create mock audio uploads
    response = upload_audio(create_sine(note="A"), filename="a.wav")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_a = wav_response_data['id']

    response = upload_audio(create_sine(note="B"), filename="b.wav")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_b = wav_response_data['id']

    response = upload_audio(create_sine(note="C"), filename="c.wav")
    assert response.status_code == 201
    wav_response_data = json.loads(response.data.decode('utf8'))
    wav_id_c = wav_response_data['id']

    # Create mock transcription uploads
    response = upload_transcription("A", filename="a.phonemes")
    assert response.status_code == 201
    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id_a = transcription_response_data['id']

    response = upload_transcription("B", filename="b.phonemes")
    assert response.status_code == 201
    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id_b = transcription_response_data['id']

    response = upload_transcription("C", filename="c.phonemes")
    assert response.status_code == 201
    transcription_response_data = json.loads(response.data.decode('utf8'))
    transcription_id_c = transcription_response_data['id']

    data = {
        "audioId": wav_id_a,
        "transcriptionId": transcription_id_a
    }

    response = client.post(
        '/v0.1/utterance',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    utterance_id_a = utterance_response_data['id']

    data = {
        "audioId": wav_id_b,
        "transcriptionId": transcription_id_b
    }

    response = client.post(
        '/v0.1/utterance',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    utterance_id_b = utterance_response_data['id']

    data = {
        "audioId": wav_id_c,
        "transcriptionId": transcription_id_c
    }

    response = client.post(
        '/v0.1/utterance',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    utterance_response_data = json.loads(response.data.decode('utf8'))
    utterance_id_c = utterance_response_data['id']

    data = {
        "name": "Test Corpus",
        "label_type": "phonemes",
        "feature_type": "fbank",
        "preprocessed": "false",
        "testing": [
            utterance_id_a
        ],
        "training": [
            utterance_id_b
        ],
        "validation": [
            utterance_id_c
        ]
    }

    response = client.post(
        '/v0.1/corpus',
        data=json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

    assert response.status_code == 201