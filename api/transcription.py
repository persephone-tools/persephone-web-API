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
    print("Got {}".format(transcriptionFile))
    try:
        filename = text_files.save(transcriptionFile)
    except flask_uploads.UploadNotAllowed:
        return "Invalid upload format, must be a text file", 415
    else:
        file_url = uploads_url_base + 'transcription_uploads/' + filename
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
    print("Got transcription file ID {}".format(transcription))
    return "Get transcription info not implemented", 501
