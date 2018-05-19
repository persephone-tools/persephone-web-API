"""
API endpoints for /utterance
"""
import sqlalchemy

from . import db
from .db_models import Utterance
from .serialization import AudioSchema, TranscriptionSchema

def get(utteranceID):
    """GET request, find utterance by ID"""
    existing_utterance = Utterance.query.get_or_404(utteranceID)
    result = {
        "id" : existing_utterance.id,
        "audio" : AudioSchema().dump(existing_utterance.audio).data,
        "transcription" : TranscriptionSchema().dump(existing_utterance.transcription).data,
    }
    return result, 200

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

def search():
    """Search available utterances"""
    results = Utterance.query.all()
    json_results = []
    for ut in results:
        json_results.append({
            "id" : ut.id,
            "audio" : AudioSchema().dump(ut.audio).data,
            "transcription" : TranscriptionSchema().dump(ut.transcription).data,
        })
    return json_results, 200