"""
API endpoints for /transcription
This deals with the API access for transcription files uploading/downloading.
"""
import flask_uploads

from ..extensions import db
from ..db_models import Transcription, FileMetaData
from ..upload_config import text_files, uploads_url_base
from ..serialization import TranscriptionSchema

def post():
    """Create a transcription from a POST request that contains the
    transcription information in a UTF-8 encoded string"""
    raise NotImplementedError

def from_file(transcriptionFile):
    """handle POST request for transcription file"""
    try:
        filename = text_files.save(transcriptionFile)
    except flask_uploads.UploadNotAllowed:
        return "Invalid upload format, must be a text file", 415
    else:
        file_url = uploads_url_base + 'text_uploads/' + filename
        metadata = FileMetaData(path=file_url, name=filename)
        current_transcription = Transcription(file_info=metadata, url=file_url, name=filename)
        db.session.add(current_transcription)
        db.session.commit()

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


def search():
    """Search transcription files"""
    results = Transcription.query.all()
    json_results = [TranscriptionSchema().dump(transcription).data for transcription in results]
    return json_results, 200
