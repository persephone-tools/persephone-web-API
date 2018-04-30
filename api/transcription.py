"""
API endpoints for /transcription
This deals with the API access for transcription files uploading/downloading.
"""
import flask_uploads

from .upload_config import text_files, uploads_url_base

from .db_models import Transcription

from . import db

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

    result = {
        "id": current_file.id,
        "fileURL": current_file.url,
        "fileName" : current_file.filename,
    }
    return result, 201

def get(transcriptionID):
    """Handle GET request for transcription file information.
    Note that this does not return the transcription file directly but
    rather a JSON object with the relevant information.
    This allows the flexibility of file storage being handled
    by another service that is outside this API service."""
    results = []
    for row in Transcription.query.filter(Transcription.id==transcriptionID):
        results.append(row)
    if results:
        if len(results) != 1:
            pass # TODO: This indicates a problem with the primary keys in the database
        transcription_info = results[0]
        result = {
            "id": transcription_info.id,
            "fileURL": transcription_info.url,
            "fileName" : transcription_info.filename,
        }
        return result, 200
    return "Transcription with ID {} not found".format(transcriptionID), 404
