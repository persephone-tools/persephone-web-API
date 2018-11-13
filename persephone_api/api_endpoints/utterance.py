"""
API endpoints for /utterance
"""
import sqlalchemy

from ..extensions import db
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
        error = {
            "status": 409,
            "reason": "This utterance already exists",
            "errorMessage": "This utterance with audio id {} and transcription ID of {}"
                            " already exists and has id {}".format(audioId, transcriptionId, existing_utterance),
            "userErrorMessage": "This utterance with audio id {} and transcription ID of {}"
                                " already exists and has id {}".format(audioId, transcriptionId, existing_utterance),
        }
        return "Utterance already exists", 409
    try:
        current_utterance = DBUtterance(audio_id=audioId, transcription_id=transcriptionId)
        db.session.add(current_utterance)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        error = {
            "status": 400,
            "reason": "Database error",
            "errorMessage": "Database error",
            "userErrorMessage": "Database error",
        }
        return error, 400
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