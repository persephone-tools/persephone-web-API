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
        error = {
            "status": 400,
            "reason": "Duplicate label provided",
            "errorMessage": "Can't create the label {} as it already exists in the database. "
                            "Note that because we use NFC Unicode normalization 2 identical labels can come up as duplicates "
                            "if specified with different unicode codepoints".format(raw_label),
            "userErrorMessage": "Can't create the label {} as it already exists in the database. "
                                "Note that because we use NFC Unicode normalization 2 identical labels can come up as duplicates "
                                "if specified with different unicode codepoints".format(raw_label),
        }

        return error, 400
    else:
        result = LabelSchema().dump(current_label).data
        return result, 201