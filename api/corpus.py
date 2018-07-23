"""
API endpoints for /corpus
This deals with the API for corpus model definitions and metadata
"""
import logging
import os
import uuid
import zipfile

from pathlib import Path

import sqlalchemy

from .db_models import DBcorpus, TestingDataSet, TrainingDataSet, ValidationDataSet
from . import db
from .serialization import CorpusSchema

from swagger.flask_app import connexion_app, app

logger = logging.getLogger(__name__)

def create_prefix_file(prefix_information, filepath: Path):
    """Create a persephone formatted prefix file"""
    raise NotImplementedError


def create_corpus_file_structure(corpus: DBcorpus, corpus_path: Path) -> None:
    """Create the needed file structure on disk for a persephone.Corpus
    object to be created

    :corpus: The DBcorpus object specifying how the persephone.Corpus must
             be created.
    :corpus_path: path to corpus
    """
    if corpus_path.exists():
        raise FileExistsError("Corpus already exists at path {}".format(corpus_path))
    else:
        corpus_path.mkdir()

    train_prefixes_path = corpus_path / "train_prefixes.txt"
    test_prefixes_path = corpus_path / "test_prefixes.txt"
    valid_prefixes_path = corpus_path / "valid_prefixes.txt"
    create_prefix_file(corpus.training, train_prefixes_path)
    create_prefix_file(corpus.testing, test_prefixes_path)
    create_prefix_file(corpus.validation, valid_prefixes_path)
    raise NotImplementedError
    # mkdir:
    #   label
    #   wav
    #   feat

def search():
    """Handle request for all available DBcorpus"""
    results = []
    for row in db.session.query(DBcorpus):
        serialized = CorpusSchema().dump(row).data
        results.append(serialized)
    return results, 200


def get(corpusID):
    """Get a DBcorpus by its ID"""
    existing_corpus = DBcorpus.query.get_or_404(corpusID)
    result = CorpusSchema().dump(existing_corpus).data
    return result, 200


def post(corpusInfo):
    """Create a DBcorpus"""
    current_corpus = DBcorpus(name=corpusInfo['name'])
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

    #Saving Corpus as UUIDs to remove name collision issues
    corpus_uuid = uuid.uuid1()
    corpus_path = Path(app.config['CORPUS_PATH']) / str(corpus_uuid)
    create_corpus_file_structure(current_corpus, corpus_path)
    current_corpus.filesystem_path = corpus_uuid
    db.session.add(current_corpus)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return "Invalid corpus provided", 400
    else:
        result = CorpusSchema().dump(current_corpus).data
        return result, 201

def preprocess(corpusID):
    """Preprocess a corpus"""
    raise NotImplementedError

def create_from_zip(zippedFile):
    if zippedFile.mimetype != 'application/zip':
        logger.info("Non zip mimetype from request, got {}".format(zippedFile.mimetype))
        return "File type must be zip", 415
    if not zipfile.is_zipfile(zippedFile):
        logger.info("Zip file corrupted")
        return "File type must be zip", 415
    print("Create corpus from zip file")
    return "Create corpus from zip not implemented", 501