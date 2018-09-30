"""Handlers for phonetic label functionality"""

import sqlalchemy

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

    raw_label = labelInfo['phoneticLabel']
    current_label = Label(
        label=raw_label
    )

    db.session.add(current_label)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Duplicate label {} provided".format(raw_label), 400
    else:
        result = LabelSchema().dump(current_label).data
        return result, 201