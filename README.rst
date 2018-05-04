Persephone-web-API v0.0.1 (beta version)
========================================

This is a web API for the the `persephone library <https://github.com/oadams/persephone>`_

This is a REST API that will provide the ability to interact with the Persephone transcription tools from over the network.

This API is based on the [OpenAPI 2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) (formerly known as Swagger) standard which specifies API endpoints via API description files. The API specification for this project can be found in a YAML file located in the repository at `./swagger/api_spec.yaml`

This file will show you all the endpoints that are supported but an easier way to get familiarity with the API is to use the API explorer frontend provided by the project. See the API explorer section of this README to get started with exploring the API.

Installation
------------

Currently you will need to set up a virtualenvironment and install package requirements.
You can do this as follows:

.. code:: sh

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

At this point you should have the packages required to run this API server.

Usage
-----

This server uses the Flask framework to service API endpoints.

Make sure you are in the active virtualenvironment and run the transcription server as follows:

.. code:: sh

	python3 transcription_API_server.py

This will start up a web server that will service the endpoints defined by the API.

Test that this server is functional by pointing your browser at the URL that pages are being served from.

API explorer
------------

Since this uses [OpenAPI 2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) (formerly known as Swagger) API specification we have tooling that will help you to explore the API.
This tooling creates and hosts a web frontend that shows you the various API endpoints and provides you forms to test these endpoints from your browser.
Load up the API explorer page by navigating to `/v0.1/ui/` (Note that the version prefix will depend on the version of the API being served).

If you find yourself needing to construct more complex web requests we would recommend you look into a tool such as [Postman](https://www.getpostman.com/) for ease of API testing.
