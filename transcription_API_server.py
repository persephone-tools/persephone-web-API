import connexion
from connexion.resolver import RestyResolver

import api

app = connexion.FlaskApp(__name__, specification_dir='swagger/')
app.add_api('api_spec.yaml', resolver=RestyResolver('api'))


@app.route('/')
def index():
    return """Access to the API is via the API versioned path prefix
<a href="/{0}">/{0}</a>. The API explorer tool can be found at
<a href="/{0}/ui/">/{0}/ui/</a>, this is the best place to explore the API.
""".format("v0.1")

app.run(port=8080)

