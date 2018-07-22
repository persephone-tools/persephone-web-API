""" Define the endpoints that this API can handle via the swagger/OpenAPI YAML file"""

import connexion
from connexion.resolver import RestyResolver

# Create the API endpoints from YAML specification
app = connexion.FlaskApp(__name__, specification_dir='.')
app.add_api('api_spec.yaml', resolver=RestyResolver('api'))