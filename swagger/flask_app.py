""" Create a connexion FlaskApp to handle the swagger/OpenAPI
YAML specified API.

Note that the regular Flask application is found at `connexion_app.app`
and is exposed as `app`"""

import connexion

# Create the API endpoints from YAML specification
connexion_app = connexion.FlaskApp(__name__, specification_dir='.')

# fetch underlying flask app from the connexion app
app = connexion_app.app