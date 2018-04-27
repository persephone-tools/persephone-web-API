import flask_uploads
import os

audio_files = flask_uploads.UploadSet(name="audio", extensions=("wav", "wave", "mp3"))
text_files =  flask_uploads.UploadSet(name="text", extensions=("txt"))
base_upload_path = os.path.join(os.getcwd(), 'user_uploads')

def configure_uploads(flask_app):
    flask_app.config['UPLOADED_AUDIO_DEST'] = os.path.join(base_upload_path, 'audio_uploads')
    flask_app.config['UPLOADED_TEXT_DEST'] = os.path.join(base_upload_path, 'text_uploads')
    flask_uploads.configure_uploads(flask_app, (audio_files, text_files))
