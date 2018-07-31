import os

from flask import send_from_directory

from persephone_api.upload_config import configure_uploads
from persephone_api.app import create_app
from persephone_api.settings import DevConfig

app = create_app(DevConfig)

@app.route('/')
def index():
    return """Access to the API is via the API versioned path prefix
<a href="/{version}">/{version}</a>. The API explorer tool can be found at
<a href="/{version}/ui/">/{version}/ui/</a>, this is the best place to explore the API.
""".format(version="v0.1")

from persephone_api import db
db.init_app(app)

# create DB tables
with app.app_context():
    db.create_all()

# configure upload paths
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #max 64 MB file upload
app.config['BASE_UPLOAD_DIRECTORY'] = os.path.join(os.getcwd(), 'user_uploads')
configure_uploads(app)

# persephone paths
# Persephone related files stored here
app.config['FILE_STORAGE_BASE'] = os.path.join(os.getcwd(), 'persephone_file_storage')
# Corpus directories stored here
app.config['CORPUS_PATH'] = os.path.join(app.config['FILE_STORAGE_BASE'], 'corpus')
if os.path.isdir(app.config['CORPUS_PATH']):
    print("Corpus storage directory {} already exists, not creating".format(app.config['CORPUS_PATH']))
else:
    os.makedirs(app.config['CORPUS_PATH'])


@app.route('/uploads/<path:path>')
def uploaded_file(path):
    """Serve uploaded files for development purposes
    Note this is for development only, serve these files with Apache/nginx in production environments.
    """
    return send_from_directory(app.config['BASE_UPLOAD_DIRECTORY'],
                               path)

app.run(port=8080)

