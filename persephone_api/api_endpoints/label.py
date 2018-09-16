"""Handlers for phonetic label functionality"""

from ..extensions import db
from ..db_models import Label
from ..serialization import LabelSchema

def search():
    """Handle request for all available labels"""
    results = Label.query.all()
    json_results = [LabelSchema().dump(label).data for label in results]
    return json_results, 200

def post(labelInfo):
    """Create a new phonetic label"""

    current_label = Label(
        label=labelInfo['phoneticLabel']
    )

    db.session.add(current_label)
    db.session.commit()

    result = LabelSchema().dump(current_label).data
    return result, 201