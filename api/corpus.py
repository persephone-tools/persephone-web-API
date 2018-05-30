"""
API endpoints for /corpus
This deals with the API access corpus model definitions and metadata
"""
import logging
import zipfile

import sqlalchemy

from .db_models import Corpus, TestingDataSet, TrainingDataSet, ValidationDataSet
from . import db
from .serialization import CorpusSchema

logger = logging.getLogger(__name__)

def search():
    """Handle request for all available Corpus"""
    results = []
    for row in db.session.query(Corpus):
        serialized = CorpusSchema().dump(row).data
        results.append(serialized)
    return results, 200


def get(corpusID):
    """Get a Corpus by its ID"""
    existing_corpus = Corpus.query.get_or_404(corpusID)
    result = CorpusSchema().dump(existing_corpus).data
    return result, 200


def post(corpusInfo):
    """Create a Corpus"""
    current_corpus = Corpus(name=corpusInfo['name'])
    db.session.add(current_corpus)
    db.session.flush() # Make sure that current_corpus.id exists before using as key
    training_set_IDs = corpusInfo['training']
    for train_utterance_id in training_set_IDs:
        db.session.add(
            TrainingDataSet(
                corpus_id=current_corpus.id,
                utterance_id=train_utterance_id
            )
        )

    testing_set_IDs = corpusInfo['testing']
    for test_utterance_id in testing_set_IDs:
        db.session.add(
            TestingDataSet(
                corpus_id=current_corpus.id,
                utterance_id=test_utterance_id
            )
        )

    validation_set_IDs = corpusInfo['validation']
    for validation_utterance_id in validation_set_IDs:
        db.session.add(
            ValidationDataSet(
                corpus_id=current_corpus.id,
                utterance_id=validation_utterance_id
            )
        )

    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Invalid corpus provided", 400
    else:
        result = CorpusSchema().dump(current_corpus).data
        return result, 201


def create_from_zip(zippedFile):
    if zippedFile.mimetype != 'application/zip':
        logger.info("Non zip mimetype from request, got {}".format(zippedFile.mimetype))
        return "File type must be zip", 415
    if not zipfile.is_zipfile(zippedFile):
        logger.info("Zip file corrupted")
        return "File type must be zip", 415
    print("Create corpus from zip file")
    return "Create corpus from zip not implemented", 501


def create_file_structure(corpus, path):
    """Create the needed file structure on disk for a persephone.Corpus
    object to be created"""
    raise NotImplementedError
