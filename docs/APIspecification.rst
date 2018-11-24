API specification
=================

This project uses the OpenAPI v2 specification to define the API endpoints in an easily parsable [YAML](https://en.wikipedia.org/wiki/YAML) file.


Code generation
^^^^^^^^^^^^^^^
By providing a machine-parsable API interface we are aiming to make it easier for developers to consume this API.

The [Persephone Web Frontend](https://github.com/persephone-tools/persephone-frontend) uses this API specification to generate code.
This ensures that the interfaces are correct and also has reduced the time it has taken to create.

If you are interested in code-generation for your code that interacts with this project we recommend having a look at [openapi-generator](https://github.com/OpenAPITools/openapi-generator)