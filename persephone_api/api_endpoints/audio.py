"""
API endpoints for /audio
This deals with the API access for audio files uploading/downloading.
"""
from pathlib import Path

import flask
import flask_uploads

from ..error_response import error_information
from ..extensions import db
from ..db_models import Audio, FileMetaData
from ..upload_config import audio_files, uploads_url_base
from ..serialization import AudioSchema

def create_audio(filepath: Path, data: bytes, base_path: Path=None) -> Audio:
    """Helper function to create the database rows and associated files
    for an Audio item

    filepath: Relative Path to the audio file on disk
    data: the data contained in this audio file, if an empty bytes array is passed in
          no data is written to `filepath` otherwise this data is written to the file
          path that was passed in as the first parameter.
          base_path: The path to the storage for audio files, if this not provided
          it will default to the upload file destination found in the app config
          `config['UPLOADED_AUDIO_DEST']`

    Returns the ORM object that corresponds to this audio file
    """
    if not base_path:
        base_path = Path(flask.current_app.config['UPLOADED_AUDIO_DEST'])
    storage_location = base_path / filepath
    if data: # We got data so we have to write this out the the filename
        with filepath.open('wb') as audio_file_data:
            audio_file_data.write(data)
    filename = str(filepath)
    file_url = uploads_url_base + 'audio_uploads/' + filename
    metadata = FileMetaData(path=file_url, name=filename)
    current_file = Audio(file_info=metadata, url=file_url)
    db.session.add(current_file)
    db.session.commit()
    return current_file


def post(audioFile):
    """handle POST request for audio file"""
    try:
        filename = audio_files.save(audioFile)
    except flask_uploads.UploadNotAllowed:
        return error_information(
            status=415,
            title="Invalid file format for audio upload",
            detail="Invalid file format for audio upload, must be an audio file."
                   " Got filename {} , allowed extensions are {}".format(audioFile.filename, audio_files.extensions),
        )
    else:
        # We already write out the file using the flask uploads helper
        # so no need to write it again, hence the empty data passed in below
        # which is handled in a special case in the create_audio function.
        current_file = create_audio(filename, b'')

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

def search(pageNumber=1, pageSize=20):
    """Search audio files"""
    paginated_results = Audio.query.paginate(page=pageNumber, per_page=pageSize, error_out=True)
    json_results = [AudioSchema().dump(audio).data for audio in paginated_results.items]
    return json_results, 200
