"""Handlers for phonetic label functionality"""

from ..extensions import db
from ..db_models import Label
from ..serialization import LabelSchema

def search():
    """Handle request for all available labels"""
    raise NotImplementedError

def post(labelInfo):
    """Create a new phonetic label"""

    current_label = Label(
        label=labelInfo['phoneticLabel']
    )

    db.session.add(current_label)
    db.session.commit()

    result = LabelSchema().dump(current_label).data
    return result, 201