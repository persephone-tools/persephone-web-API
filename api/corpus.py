"""
API endpoints for /corpus
This deals with the API for corpus model definitions and metadata
"""
import logging
import os
from shutil import copyfile
import uuid
import zipfile

from pathlib import Path

import sqlalchemy

from .db_models import DBcorpus, TestingDataSet, TrainingDataSet, ValidationDataSet
from . import db
from .serialization import CorpusSchema

from swagger.flask_app import connexion_app, app

logger = logging.getLogger(__name__)

def strip_unsafe_characters(filename: str):
    """Clean out potentially unsafe characters for filesystem operations
    see: https://www.owasp.org/index.php/Testing_for_Path_Traversal_(OWASP-AZ-001)
    """
    return "".join([c for c in filename if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()

def create_prefixes(prefix_information, base_path: Path, prefix_name: str) -> set:
    """Create a persephone formatted prefix file.
    Assumes that "label" and "wav" directories exist

    :prefix_information: Data about training splits
    :base_path: Base path of this corpus
    :prefix_name: Name of current data split, must be one of:
                  "train_prefixes.txt", "test_prefixes", "validation_prefixes"
    """
    prefixes = set()
    count = 0
    for data in prefix_information:
        count += 1
        print("data.utterance", data.utterance)
        label_filename = data.utterance.transcription.filename

        # using the prefix of the label file to specify the prefix
        prefix, extension = os.path.splitext(label_filename)
        cleaned_prefix = strip_unsafe_characters(prefix)
        prefixes.add(cleaned_prefix)

        # copy transcription to "/label" directory
        label_src_path = audio_src_path = os.path.join(app.config['UPLOADED_TEXT_DEST'], label_filename)
        label_dest_path = base_path / "label" / (cleaned_prefix+extension)
        copyfile(label_src_path, str(label_dest_path))

        # copy audio to "/wav" directory
        audio_filename = data.utterance.audio.filename
        audio_src_path = os.path.join(app.config['UPLOADED_AUDIO_DEST'], audio_filename)
        audio_dest_path = base_path / "wav" / (cleaned_prefix+".wav")
        copyfile(audio_src_path, str(audio_dest_path))

    if len(prefixes) != count:
        raise ValueError("Duplicate prefix found")

    prefix_file_path = base_path / prefix_name
    with prefix_file_path.open(mode='w') as pf:
        for prefix in prefixes:
            pf.write(prefix)
            pf.write(os.linesep)
    return prefixes

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

    wav_path = corpus_path / "wav"
    wav_path.mkdir()
    label_path = corpus_path / "label"
    label_path.mkdir()

    # Create prefix files as required for specifying data splits in
    # persephone.Corpus creation
    create_prefixes(corpus.training, corpus_path, "train_prefixes.txt")
    create_prefixes(corpus.testing, corpus_path, "test_prefixes.txt")
    create_prefixes(corpus.validation, corpus_path, "valid_prefixes.txt")
    raise NotImplementedError


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