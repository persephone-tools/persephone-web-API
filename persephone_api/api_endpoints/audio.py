"""
API endpoints for /audio
This deals with the API access for audio files uploading/downloading.
"""
import flask_uploads

from ..extensions import db
from ..db_models import Audio, FileMetaData
from ..upload_config import audio_files, uploads_url_base
from ..serialization import AudioSchema

def post(audioFile):
    """handle POST request for audio file"""
    try:
        filename = audio_files.save(audioFile)
    except flask_uploads.UploadNotAllowed:
        error = {
            "status": 415,
            "reason": "Invalid file format for upload",
            "errorMessage": "Invalid file format for upload, must be an audio file",
            "userErrorMessage": "Invalid file format for upload, must be an audio file",
        }
        return error, 415
    else:
        file_url = uploads_url_base + 'audio_uploads/' + filename
        metadata = FileMetaData(path=file_url, name=filename)
        current_file = Audio(file_info=metadata, url=file_url)
        db.session.add(current_file)
        db.session.commit()

    result = AudioSchema().dump(current_file).data
    return result, 201


def get(audioID):
    """Handle GET request for audio file information.
    Note that this does not return the audio file directly but
    rather a JSON object with the relevant information.
    This allows the flexibility of file storage being handled
    by another service that is outside this API service."""
    audio_info = Audio.query.get_or_404(audioID)
    result = AudioSchema().dump(audio_info).data
    return result, 200

def search():
    """Search audio files"""
    results = Audio.query.all()
    json_results = [AudioSchema().dump(audio).data for audio in results]
    return json_results, 200
