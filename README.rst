Persephone-web-API (beta version)
========================================

This is a web API for the the `persephone library <https://github.com/persephone-tools/persephone>`_

This is a REST API that will provide the ability to interact with the Persephone transcription tools from over the network.

This API is based on the `OpenAPI 2.0 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md>`_ (formerly known as Swagger) standard which specifies API endpoints via API description files.
The API specification for this project can be found in a YAML file located in the repository at `./persephone_api/api_spec.yaml <https://github.com/persephone-tools/persephone-web-API/blob/master/persephone_api/api_spec.yaml>`_

This file will show you all the endpoints that are supported but an easier way to get familiarity with the API is to use the API explorer frontend provided by the project. See the API explorer section of this README to get started with exploring the API.

For more information about the API specification see the `documentation page <https://persephone-web-api.readthedocs.io/en/latest/APIspecification.html>`_.

Installation
------------

You can install this package directly or use Docker.

Because this package depends on various system binaries (such as ffmpeg) being installed as well Python packages we recommend using the Docker container we have created.
However you can also install this directly without a container as well if you wish, see the `installation documentation <https://persephone-web-api.readthedocs.io/en/latest/installation.html>`_ page for more information.


Usage
-----

We have a Docker image that will automate the install and spin up the API server.
A Docker image for this project is available at docker hub at `"persephonetools/api:latest"`

Alternatively you can build the image locally as follows:

```sh
docker build -t persephone-web-api:dev .
```

Then to run it:

```sh
docker run -p 8080:8080/tcp persephone-web-api:dev
```

If you are looking to use the whole stack the easiest way to get started is to use the docker-compose setup found in the `persephone-docker repository <https://github.com/aapeliv/persephone-docker>`_ 
as this will automate the install and setup of this API server along with the `persephone web frontend <https://github.com/persephone-tools/persephone-frontend>`_ that accesses the API.

Documentation
-------------

Documentation can be found `here <https://persephone-web-api.readthedocs.io/en/latest/>`_.


Support
-------

If you find an issue or bug with this code please open an issue on the `issues tracker <https://github.com/persephone-tools/persephone-web-API/issues>`_.
Please use the `discussion mailing list <https://lists.persephone-asr.org/postorius/lists/discuss.lists.persephone-asr.org/>`_ to discuss other questions regarding this project.
