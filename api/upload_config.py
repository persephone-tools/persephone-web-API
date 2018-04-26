import flask_uploads

audio_files = flask_uploads.UploadSet(name="audio", extensions=("wav", "wave", "mp3"))

def configure_uploads(flask_app):
    flask_app.config['UPLOADED_AUDIO_DEST'] = '/var/uploads'
    flask_uploads.configure_uploads(flask_app, (audio_files,))
