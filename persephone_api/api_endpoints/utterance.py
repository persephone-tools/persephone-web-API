"""
API endpoints for /utterance
"""
import sqlalchemy

from .. import db
from ..db_models import DBUtterance
from ..serialization import UtteranceSchema

def get(utteranceID):
    """GET request, find utterance by ID"""
    existing_utterance = DBUtterance.query.get_or_404(utteranceID)
    result = UtteranceSchema().dump(existing_utterance).data
    return result, 200

def post(utteranceInfo):
    """POST request"""
    audioId = utteranceInfo['audioId']
    transcriptionId = utteranceInfo['transcriptionId']
    existing_utterance = DBUtterance.query.filter_by(audio_id=audioId, transcription_id=transcriptionId).first()
    if existing_utterance:
        return "Utterance already exists", 409
    try:
        current_utterance = DBUtterance(audio_id=audioId, transcription_id=transcriptionId)
        db.session.add(current_utterance)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Invalid ID provided", 400
    else:
        result = UtteranceSchema().dump(current_utterance).data
        return result, 201

def search():
    """Search available utterances"""
    results = DBUtterance.query.all()
    json_results = []
    for ut in results:
        json_results.append(
            UtteranceSchema().dump(ut).data
        )
    return json_results, 200