"""
API endpoints for /transcription
This deals with the API access for transcription files uploading/downloading.
"""
import flask_uploads

from . import db
from .db_models import Transcription
from .upload_config import text_files, uploads_url_base
from .serialization import TranscriptionSchema


def post(transcriptionFile):
    """handle POST request for transcription file"""
    try:
        filename = text_files.save(transcriptionFile)
    except flask_uploads.UploadNotAllowed:
        return "Invalid upload format, must be a text file", 415
    else:
        file_url = uploads_url_base + 'text_uploads/' + filename
        current_file = Transcription(filename=filename, url=file_url)
        db.session.add(current_file)
        db.session.commit()

    result = TranscriptionSchema().dump(current_file).data
    return result, 201

def get(transcriptionID):
    """Handle GET request for transcription file information.
    Note that this does not return the transcription file directly but
    rather a JSON object with the relevant information.
    This allows the flexibility of file storage being handled
    by another service that is outside this API service."""
    results = []
    transcription = Transcription.query.get_or_404(transcriptionID)
    result = TranscriptionSchema().dump(transcription).data
    return result, 200


def search():
    """Search transcription files"""
    results = Transcription.query.all()
    json_results = [TranscriptionSchema().dump(transcription).data for transcription in results]
    return json_results, 200
