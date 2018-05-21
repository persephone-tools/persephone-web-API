"""
This file shows how you can interact with the Persephone API with the requests library.
See http://docs.python-requests.org/en/master/ for requests library documentation.
"""
import requests

API_VERSION  = "v0.1"
# Where the API is being served from
URL_BASE = "http://127.0.0.1:8080/{}/".format(API_VERSION)

# upload an audio file
files = {'audioFile': open('crdo-NRU_F4_ACCOMP_PFV.1.wav', 'rb')}

audio_url = URL_BASE + "audio"
r = requests.post(audio_url, files=files)

print(r.text)
audio_results = r.json()
audio_id = audio_results['id']
print("File uploaded has an id of {}".format(audio_id))


# upload a transcription
files = {'transcriptionFile': open('crdo-NRU_F4_ACCOMP_PFV.1.phonemes', 'rb')}

transcription_url = URL_BASE + "transcription"
r = requests.post(transcription_url, files=files)
print(r.text)
transcription_results = r.json()
transcription_id = transcription_results['id']
print("transcription uploaded has an id of {}".format(transcription_id))


# create an utterance from the audio file and transcription uploaded before
