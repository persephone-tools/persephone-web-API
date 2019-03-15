"""Configuration for the flask_uploads extension that handles file uploading"""
import os

import flask_uploads

audio_files = flask_uploads.UploadSet(name="audio", extensions=("wav", "wave", "mp3"))
text_files =  flask_uploads.UploadSet(name="text", extensions=("txt", "phonemes", "phonemes_and_tones"))
compressed_files = flask_uploads.UploadSet(name="compressed", extensions=("zip",))

# URL of files being served by this app
uploads_url_base = 'uploads/'

def configure_uploads(flask_app, base_upload_path=None) -> None:
    """Configure flask_uploads and upload paths"""
    flask_app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #max 64 MB file upload
    if base_upload_path:
        flask_app.config['BASE_UPLOAD_DIRECTORY'] = base_upload_path
    else:
        flask_app.config['BASE_UPLOAD_DIRECTORY'] = os.path.join(flask_app.instance_path, 'user_uploads')
    flask_app.config['UPLOADED_AUDIO_DEST'] = os.path.join(flask_app.config['BASE_UPLOAD_DIRECTORY'], 'audio_uploads')
    flask_app.config['UPLOADED_TEXT_DEST'] = os.path.join(flask_app.config['BASE_UPLOAD_DIRECTORY'], 'text_uploads')
    flask_app.config['UPLOADED_COMPRESSED_DEST'] = os.path.join(flask_app.config['BASE_UPLOAD_DIRECTORY'], 'compressed_uploads')
    flask_app.config['UPLOADED_FILES_URL'] = uploads_url_base
    flask_uploads.configure_uploads(
        flask_app,
        (audio_files, text_files, compressed_files)
    )
    return None
