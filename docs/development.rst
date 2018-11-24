Development
===========

If you are working on the project we recommend the development environment with Vagrant as a fast way to get up and running with the same environment as the other developers.

Development environment automation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is a Vagrantfile for automating the build and install of the development environment.
This is recommended as it is likely the easiest way to get set up with a development environment as packages will be correctly installed.

To get Vagrant: https://www.vagrantup.com/

To start and provisions the vagrant environment:

.. code:: sh

    vagrant up

Once that has installed you can access via ssh:

.. code:: sh

    vagrant ssh

The code resides at the `/vagrant` directory, set up the environment via pipenv:

.. code:: sh

    cd /vagrant
    pipenv install
    pipenv shell
    python transcription_api_server.py

If all has worked you should be able to point your browser at 127.0.0.1:8080 and you will see the page being served.


Development server usage
-------------------------

This server uses the Flask framework to service API endpoints.

Make sure you are in the active virtualenvironment and run the transcription server as follows:

.. code:: sh

	python3 transcription_API_server.py

This will start up a development web server that will service the endpoints defined by the API.

Test that this server is functional by pointing your browser at the URL that pages are being served from.
