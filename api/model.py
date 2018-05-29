"""
API endpoints for /model
This deals with the API access for model definitions and metadata
"""

from . import db
from .db_models import TranscriptionModel
from .serialization import TranscriptionModelSchema

def search():
    """Handle request to search over all models"""
    results = []
    for row in db.session.query(TranscriptionModel):
        serialized = TranscriptionModelSchema().dump(row).data
        results.append(serialized)
    return results, 200

def post():
    raise NotImplementedError
