API specification
=================

This project uses the OpenAPI v2 specification to define the API endpoints in an easily parsable [YAML](https://en.wikipedia.org/wiki/YAML) file.

API specification
^^^^^^^^^^^^^^^^^
The API specification is the single source of truth for how this web API will work.

This file is located at [persephone_api/api_spec.yaml](https://github.com/persephone-tools/persephone-web-API/blob/master/persephone_api/api_spec.yaml)

The project uses the [connexion library](https://github.com/zalando/connexion/) to directly create the URL routing for the underlying [Flask](http://flask.pocoo.org/) application that powers the API service.
As such the only URL routes that can be assumed to exist are defined in that API specification file.

If there are any discrepancies between what the API specification file states and what actually happens this should be treated as a bug. We would appreciate that you open an issue on the projects [issue tracker](https://github.com/persephone-tools/persephone-web-API/issues/new) including some details on the input you gave along with the exact output you got so we can more quickly identify the source of the issue.

Code generation
^^^^^^^^^^^^^^^
By providing a machine-parsable API interface we are aiming to make it easier for developers to consume this API.

The [Persephone Web Frontend](https://github.com/persephone-tools/persephone-frontend) uses this API specification to generate code.
This ensures that the interfaces are correct and also has reduced the time it has taken to create.

If you are interested in code-generation for this API we recommend having a look at [openapi-generator](https://github.com/OpenAPITools/openapi-generator)