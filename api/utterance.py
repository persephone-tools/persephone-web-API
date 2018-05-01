"""
API endpoints for /utterance
"""
from .db_models import Utterance

from . import db

from .serialization import AudioSchema, TranscriptionSchema

def post(utteranceInfo):
    """POST request"""
    audioId = utteranceInfo['audioId']
    transcriptionId = utteranceInfo['transcriptionId']
    print("Got audioId {} transcriptionId {}".format(audioId, transcriptionId))
    # TODO check that ID's for audio and transcription exist

    current_utterance = Utterance(audio_id=audioId, transcription_id=transcriptionId)
    db.session.add(current_utterance)
    db.session.commit()

    result = {
        "id" : current_utterance.id,
        "audio" : AudioSchema().dump(current_utterance.audio).data,
        "transcription" : TranscriptionSchema().dump(current_utterance.transcription).data,
    }
    return result, 201
