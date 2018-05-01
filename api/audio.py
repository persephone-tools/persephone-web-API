"""
API endpoints for /audio
This deals with the API access for audio files uploading/downloading.
"""
import flask_uploads

from .upload_config import audio_files, uploads_url_base

from .db_models import Audio

from . import db

def post(audioFile):
    """handle POST request for audio file"""
    try:
        filename = audio_files.save(audioFile)
    except flask_uploads.UploadNotAllowed:
        return "Invalid upload format, must be an audio file", 415
    else:
        file_url = uploads_url_base + 'audio_uploads/' + filename
        current_file = Audio(filename=filename, url=file_url)
        db.session.add(current_file)
        db.session.commit()

    result = {
        "id": current_file.id,
        "fileURL": current_file.url,
        "fileName" : current_file.filename,
    }
    return result, 201


def get(audioID):
    """Handle GET request for audio file information.
    Note that this does not return the audio file directly but
    rather a JSON object with the relevant information.
    This allows the flexibility of file storage being handled
    by another service that is outside this API service."""
    results = []
    for row in Audio.query.filter(Audio.id==audioID):
        results.append(row)
    if results:
        if len(results) != 1:
            pass # TODO: This indicates a problem with the primary keys in the database
        audio_info = results[0]
        result = {
            "id": audio_info.id,
            "fileURL": audio_info.url,
            "fileName" : audio_info.filename,
        }
        return result, 200

    return "Audio with ID {} not found".format(audioID), 404
