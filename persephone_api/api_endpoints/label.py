"""Handlers for phonetic label functionality"""
import sqlalchemy

from ..error_response import error_information
from ..extensions import db
from ..db_models import Label
from ..serialization import LabelSchema
from ..unicode_handling import normalize

def search():
    """Handle request for all available labels"""
    results = Label.query.all()
    json_results = [LabelSchema().dump(label).data for label in results]
    return json_results, 200

def post(labelInfo):
    """Create a new phonetic label

    This will be stored in a normalized form in the database.
    Refer to https://unicode.org/reports/tr15/ for details about how this works.
    """

    raw_label = labelInfo['phoneticLabel']
    current_label = Label(
        label=normalize(raw_label)
    )

    db.session.add(current_label)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return error_information(
            status=400,
            title="Duplicate label provided",
            detail="Can't create the label {} as it already exists in the database. "
                    "Note that because we use NFC Unicode normalization 2 identical labels can come up as duplicates "
                    "if specified with different unicode codepoints".format(raw_label),
        )
    else:
        result = LabelSchema().dump(current_label).data
        return result, 201