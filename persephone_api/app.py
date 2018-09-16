import os

import connexion
from connexion.resolver import RestyResolver
import flask_uploads

from . import api_endpoints

from .extensions import db
from .settings import ProdConfig
from .upload_config import configure_uploads

from flask_cors import CORS

def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.
    :param config_object: The configuration object to use.
    """
    # Create the API endpoints from YAML specification
    connexion_app = connexion.FlaskApp(__name__, specification_dir='.')
    register_swagger_api(connexion_app)

    # fetch underlying flask app from the connexion app
    app = connexion_app.app
    app.config.from_object(config_object)

    register_extensions(app)
    configure_uploads(app, base_upload_path=os.path.join(os.getcwd(), 'user_uploads'))

    if config_object.ENABLE_CORS:
        CORS(app)

    return app

def register_swagger_api(connexion_flask_app) -> None:
    """Take a connexion FlaskApp and register swagger API"""
    connexion_flask_app.add_api('api_spec.yaml', resolver=RestyResolver('persephone_api.api_endpoints'))

def register_extensions(app) -> None:
    """Register Flask extensions."""
    db.init_app(app)
    return None
