"""Handlers for phonetic label functionality"""
import unicodedata

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
    """Create a new phonetic label

    We are normalizing all labels with NFC to handle the potential duplicates.
    Refer to https://unicode.org/reports/tr15/ for details about how this works.
    """

    raw_label = labelInfo['phoneticLabel']
    NFC_normalized_label = unicodedata.normalize("NFC", raw_label)
    current_label = Label(
        label=NFC_normalized_label
    )

    db.session.add(current_label)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Duplicate label {} provided".format(raw_label), 400
    else:
        result = LabelSchema().dump(current_label).data
        return result, 201