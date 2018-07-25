
# This is a very quick and dirty to populate some initial data via calling the API.
# Note that for now ID's are hardcoded in later steps.
# TODO: process response data IDs
# Upload WAV files
echo "*** uploading WAV files ***"
curl -X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' --form audioFile=@crdo-NRU_F4_ACCOMP_PFV.1.wav 'http://127.0.0.1:8080/v0.1/audio'
curl -X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' --form audioFile=@crdo-NRU_F4_ACCOMP_PFV.3.wav 'http://127.0.0.1:8080/v0.1/audio'
curl -X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' --form audioFile=@crdo-NRU_F4_ACCOMP_PFV.7.wav 'http://127.0.0.1:8080/v0.1/audio'
# Upload transcriptions
echo "*** uploading transcription files ***"
curl -X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' --form transcriptionFile=@crdo-NRU_F4_ACCOMP_PFV.1.phonemes 'http://127.0.0.1:8080/v0.1/transcription'
curl -X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' --form transcriptionFile=@crdo-NRU_F4_ACCOMP_PFV.3.phonemes 'http://127.0.0.1:8080/v0.1/transcription'
curl -X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' --form transcriptionFile=@crdo-NRU_F4_ACCOMP_PFV.7.phonemes 'http://127.0.0.1:8080/v0.1/transcription'
# Create Utterances
echo "*** specifying utterances ***"
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   "audioId": 1,
   "transcriptionId": 1
 }' 'http://127.0.0.1:8080/v0.1/utterance'
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   "audioId": 2,
   "transcriptionId": 2
 }' 'http://127.0.0.1:8080/v0.1/utterance'
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{
   "audioId": 3, 
   "transcriptionId": 3 
 }' 'http://127.0.0.1:8080/v0.1/utterance'

# Create corpus
echo "*** creating corpus ***"
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/problem+json' -d '{
   "name": "Test Corpus", 
   "feature_type": "fbank",
   "testing": [
     1
   ],
   "training": [
     2
   ],
   "validation": [
     3
   ]
 }' 'http://127.0.0.1:8080/v0.1/corpus'
