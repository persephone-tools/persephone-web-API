Installation
============

We recommend that you use the Docker image for running this project because it handles the system binaries install in a repeatable way.

Docker
^^^^^^

Installing Docker
------------------
First make sure that you have docker installed on your machine.
Here's some steps to do that on Ubuntu:

.. code:: bash

    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update

This will add the docker repository to your package manager lists.
Make sure that the package that is the candidate to be installed is the newly added one and not the ubuntu package via this command:

.. code:: bash

    apt-cache policy docker-ce

If this has worked correctly you'll see an output such as this:

.. code::

    docker-ce:
      Installed: (none)
      Candidate: 18.06.1~ce~3-0~ubuntu
      Version table:
     *** 18.06.1~ce~3-0~ubuntu 500
            500 https://download.docker.com/linux/ubuntu xenial/stable amd64 Packages
            100 /var/lib/dpkg/status
         18.06.0~ce~3-0~ubuntu 500
            500 https://download.docker.com/linux/ubuntu xenial/stable amd64 Packages
         18.03.1~ce-0~ubuntu 500
            500 https://download.docker.com/linux/ubuntu xenial/stable amd64 Packages


Note that there is no package installed but the candidate for installation is from the Docker repository which is what we want.

Now install Docker with this command:

.. code:: bash

    sudo apt-get install -y docker-ce


If the install has been successful then you should be able to see the Docker process running.
Check with this command

.. code:: bash

    sudo systemctl status docker

In a successful case the output should look like this:

.. code::

    ● docker.service - Docker Application Container Engine
       Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
       Active: active (running) since Mon 2018-10-15 16:52:50 AEDT; 25min ago
         Docs: https://docs.docker.com
     Main PID: 9841 (dockerd)
        Tasks: 41
       Memory: 52.4M
          CPU: 9.557s
       CGroup: /system.slice/docker.service
               ├─9841 /usr/bin/dockerd -H fd://
               └─9868 docker-containerd --config /var/run/docker/containerd/containerd.toml

If you wish to not use `sudo` to invoke Docker, add your user to the Docker group with the following command:

.. code:: bash

    sudo usermod -aG docker ${USER}

Note that you may have to log out and back in again for this to work

Then verify that the install has been successful via running a real container:

.. code:: bash

    docker run hello-world


Running this container
-----------------------

To run this project with the docker container you will have to do the following
Build the container:

.. code:: bash

    docker build -t persephone-web-api:dev .

Run it:

.. code:: bash

    docker run -p 8080:8080/tcp persephone-web-api:dev


If this has succeeded you should be able to access the API at the port you just specified.

Direct install
^^^^^^^^^^^^^^

The upstream Persephone package requires some binaries to be installed and available on the path.
You will need to make sure that these are installed first.

System packages
---------------

There are some 3rd party requirements that have to be installed in order for the upstream Persephone library to function.
These packages can be found in the file `"bootstrap.sh" <https://github.com/persephone-tools/persephone-web-API/blob/master/bootstrap.sh>`_.

Required:

* `sox <https://en.wikipedia.org/wiki/SoX>`_
* `ffmpeg <https://ffmpeg.org/>`_

Optional

* `Kaldi <http://kaldi-asr.org/>`_ (for pitch features support)

The web API application
-----------------------

The web API itself is a python application which requires Python 3.5.
We have not currently tested this package with other implementations such as PyPy.

Currently you will need to set up a virtualenvironment and install package requirements.
The easiest and most reliable way to do this is as follows:

.. code:: sh

    pipenv install

At this point you should have the packages required to run this API server.

(Note that the Docker image is an automated version of this direct install along with installation of system binaries)

Usage
-----

This server uses the Flask framework to service API endpoints.

Make sure you are in the active virtualenvironment and run the transcription server as follows:

.. code:: sh

	python3 transcription_API_server.py

This will start up a web server that will service the endpoints defined by the API.

Test that this server is functional by pointing your browser at the URL that pages are being served from.
