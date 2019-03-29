"""
API endpoints for /transcription
This deals with the API access for transcription files uploading/downloading.
"""
import os
from pathlib import Path
import uuid

import flask
import flask_uploads

from ..error_response import error_information
from ..extensions import db
from ..db_models import Transcription, FileMetaData
from ..serialization import TranscriptionSchema
from ..unicode_handling import normalize
from ..upload_config import text_files, uploads_url_base


def create_transcription(filepath: Path, data: str, *, base_path: Path=None,
                         transcription_name: str=None) -> Transcription:
    """Creates the transcription rows in the database,
    returns the ORM object that corresponds to this transcription

    Args:
        filepath: The relative path to this file
        data: the data contained in this transcription
        base_path: The path to the storage for transcription files, if this not provided
          it will default to the upload file destination found in the app config
          `config['UPLOADED_TEXT_DEST']`
    """
    if not base_path:
        base_path = Path(flask.current_app.config['UPLOADED_TEXT_DEST'])
    if not base_path.is_dir():
        base_path.mkdir()
    normalized_text = normalize(data)
    storage_location = base_path / filepath
    with storage_location.open('w') as transcription_storage:
        transcription_storage.write(normalized_text)
    filename = str(filepath)
    file_url = uploads_url_base + 'text_uploads/' + filename
    file_metadata = FileMetaData(path=file_url, name=str(storage_location))

    # If no optional name was provided we will just use the file name for
    # naming this transcription
    if not transcription_name:
        transcription_name = filename

    current_transcription = Transcription(
        url=file_url,
        name=transcription_name,
        text=normalized_text,
        file_info=file_metadata,
    )
    db.session.add(current_transcription)
    db.session.commit()
    return current_transcription

def post(body):
    """Create a transcription from a POST request that contains the
    transcription information in a UTF-8 encoded string"""
    text = body['text']
    prefix = uuid.uuid1()
    filename = str(prefix) + '-' + body.get('filename', '')
    optional_args = {}
    try:
        optional_args['transcription_name'] = body['name']
    except KeyError:
        pass
    current_transcription = create_transcription(filename, text, **optional_args)
    result = TranscriptionSchema().dump(current_transcription).data
    return result, 201

def from_file(transcriptionFile):
    """handle POST request for transcription file"""
    try:
        filename = text_files.save(transcriptionFile)
    except flask_uploads.UploadNotAllowed:
        return error_information(
            status=415,
            title="Invalid file format for transcription upload",
            detail="Invalid file format for transcription upload, must be a text file"
                   " Got filename {} , allowed extensions are {}".format(transcriptionFile.filename, text_files.extensions),
        )
    else:
        # We re-open here because the passed in file is a generator that
        # is expended by the save above, there may be a better way of dealing
        # with this in the future
        with open(text_files.path(filename), 'r') as tf:
            raw_data = tf.read()
        file_path = Path(filename)
        current_transcription = create_transcription(file_path, raw_data)

    result = TranscriptionSchema().dump(current_transcription).data
    return result, 201

def get(transcriptionID):
    """Handle GET request for transcription file information.
    Note that this does not return the transcription file directly but
    rather a JSON object with the relevant information.
    This allows the flexibility of file storage being handled
    by another service that is outside this API service."""
    transcription = Transcription.query.get_or_404(transcriptionID)
    result = TranscriptionSchema().dump(transcription).data
    return result, 200


def search(pageNumber=1, pageSize=20):
    """Search transcription files"""
    paginated_results = Transcription.query.paginate(page=pageNumber, per_page=pageSize, error_out=True)
    json_results = [TranscriptionSchema().dump(transcription).data for transcription in paginated_results.items]
    return json_results, 200
