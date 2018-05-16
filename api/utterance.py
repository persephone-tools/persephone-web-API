"""
API endpoints for /utterance
"""
import sqlalchemy

from . import db
from .db_models import Utterance
from .serialization import AudioSchema, TranscriptionSchema

def post(utteranceInfo):
    """POST request"""
    audioId = utteranceInfo['audioId']
    transcriptionId = utteranceInfo['transcriptionId']
    existing_utterance = Utterance.query.filter_by(audio_id=audioId, transcription_id=transcriptionId).first()
    if existing_utterance:
        return "Utterance already exists", 409
    try:
        current_utterance = Utterance(audio_id=audioId, transcription_id=transcriptionId)
        db.session.add(current_utterance)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Invalid ID provided", 400
    else:
        result = {
            "id" : current_utterance.id,
            "audio" : AudioSchema().dump(current_utterance.audio).data,
            "transcription" : TranscriptionSchema().dump(current_utterance.transcription).data,
        }
        return result, 201
