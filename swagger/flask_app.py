""" Define the endpoints that this API can handle via the swagger/OpenAPI YAML file"""

import connexion
from connexion.resolver import RestyResolver

# Create the API endpoints from YAML specification
connexion_app = connexion.FlaskApp(__name__, specification_dir='.')

# fetch underlying flask app from the connexion app
app = connexion_app.app