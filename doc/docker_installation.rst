Docker Installation
+++++++++++++++++++

First, install Docker for Mac from Docker_. Once installed use the Preferences menu, General tab to set the number of CPUs to 4 and the Memory at least 12 GB. To get the docker image for OpSim4, do::

	docker pull lsst/opsim4

This will pull the latest version of the image down. Be warned, however, that this image may contain unvetted features and may not work properly. The best thing to do is grab a versioned image. The list of versions, include latest, can be found at the OpSimVersions_ docker page. A versioned image is retrieved by doing the following::

	docker pull lsst/opsim4:version

Where, ``version`` is a tag listed in the referenced page. While the image is retrieved, fetch the provided script for running an OpSim4 container by doing::

	curl -OL https://raw.githubusercontent.com/lsst-sims/sims_ocs/master/docker/run/run_opsim4.sh

Place the script in a location that is visible from your ``$PATH``. The script needs to be edited to map local directory on your machine to ones in the container. Anything in the script with ``changeme`` needs to be replaced. To run the container, do::

	run_opsim4 <container name>

where ``container name`` is any name you want to give to the container. The script defaults to *latest* for the version. If you have a tagged image, use the following method::

	run_opsim4 -t <version name> <container name>

The container is designed to start with the LSST stack environment, so to setup OpSim4 do::

	setup ts_scheduler
	setup sims_ocs

The simulator will not run just yet, however. The sky brightness model data needs to be downloaded. Follow the instructions :ref:`here<skymodel-data>` to get things going. While the data is downloading, you can reenter the container to continue the setup process. This action is completed by doing the following::

	docker exec -it <container name> /home/opsim/startup.sh

You can now follow the instructions in the :ref:`database installation<installation-database>` section and the :ref:`running OpSim4<running-opsim4>` part to setup the rest of the simulator. Please ignore all other parts above this section as well as the ``drun`` in front of the OpSim4 execution examples. The container already is setup properly and does not require the use of the ``drun`` wrapper script. Only when the sky brightness data is done downloading will the simulator function properly.

.. _Docker: https://www.docker.com/products/docker
.. _OpSimDocker: https://hub.docker.com/r/lsst/opsim4/
.. _OpSimVersions: https://hub.docker.com/r/lsst/opsim4/tags/