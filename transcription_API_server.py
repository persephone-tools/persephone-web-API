import connexion
from connexion.resolver import RestyResolver

import api

app = connexion.FlaskApp(__name__, specification_dir='swagger/')
app.add_api('api_spec.yaml', resolver=RestyResolver('api'))
app.run(port=8080)

