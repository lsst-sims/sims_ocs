============
Installation
============

.. warning::

	The current installation requires multiple repositories and a mixture of environments. It also only works on a Linux operating system. It has been tested only CentOS 7.

.. note::

	If performing the installation on a virtual machine, it needs the following minimum requirements:

		* Memory: 10 GB (minimum)
		* Number of processors: 3 (4 recommended)
		* Network: Bridged adapter

General Installation Notes
--------------------------

Due to the heavy use of repositories for this installation, the instructions will assume you have created a ``git`` directory in your ``$HOME`` directory. This will be referenced as ``gitdir``. The individual repository installation instructions will give further advice on directory names. This is intended to make the usage "easier". Also, all instructions are based around using the code, not developing it.

SAL Installation
----------------

The SAL (Software Abstraction Layer) is a wrapper around the DDS (Data Distribution Service) layer and provides binding to Python. This requires the OpenSplice and SAL repositories from Telescope and Site. Inside the ``gitdir`` create a directory called ``ts``. Go into this directory and run the following::

	git clone https://github.com/lsst-ts/ts_opensplice.git
	git clone https://github.com/lsst-ts/ts_sal.git

In the SAL clone, there is a user guide that documents installation and setup of SAL. Its location is ``gitdir/ts/ts_sal/SAL_User_Guide.pdf``. Follow section 1 and the main part of section 2. Sub-sections (those colored blue) 2.1 and 2.2 are redundant as we've already installed the SAL. Sub-section 2.3 is replaced by the following documentation that is specific to this SOCS/Scheduler setup.

Build Scheduler Topic Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a ``$HOME/dds`` directory and copy the ``gitdir/ts/ts_sal/setup.env`` to it. Also, create a ``$HOME/dds/lib`` directory for later. The following variables need to be edited in ``setup.env`` to reflect your setup::

	export LSST_SDK_INSTALL=$HOME/git/ts/ts_sal
	export OSPL_HOME=$HOME/git/ts/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux

All other variables can remain the same. Once the edits are complete, do::

	source $HOME/dds/setup.env

The configuration should complete without errors. Go back to ``gitdir/ts/ts_sal`` and do the following::

	git checkout -t origin/feature/scheduler_xml_devel
	cd test
	salgenerator scheduler validate
	salgenerator scheduler sal cpp
	salgenerator scheduler sal python

Once the build is complete, the topic and supporting library need to be copied via the following::

	cp scheduler/cpp/src/SALPY_scheduler.so $HOME/dds/lib
	cp scheduler/cpp/libsacpp_scheduler_types.so $HOME/dds/lib

Scheduler and SOCS Source Code
------------------------------

The Scheduler repository should also be cloned to ``gitdir/ts`` via the following::

	git clone https://github.com/lsst-ts/ts_scheduler.git

The SOCS repository should be cloned into the ``gitdir``. Create a directory there called ``lsst-sims``, go into that and run the following::

	git clone https://github.com/lsst-sims/sims_ocs.git

Conda Installation
~~~~~~~~~~~~~~~~~~

The SOCS and Scheduler installation require a set of Python modules. It is recommended to install a clean version of Python via a mechanism like 
`Miniconda <http://conda.pydata.org/miniconda.html>`_. A configuration module is also necessary from the LSST Stack for SOCS, so this will need to be setup as well. Going forward, all the prerequisites will be installed via the conda mechanism.

Install miniconda from the above link. It is assumed that the ``bin`` directory from the installation will make it into the ``$PATH`` somehow. This is one of the few places where the user gets to choose how to do this. After the installation, it's a good idea to update it, so do the following::

	conda update conda

Next, create a Conda environment and activate it::

	conda create -n opsim4 python=2
	source activate opsim4

Next, add the LSST Conda package channel by doing the following::

    conda config --add channels http://conda.lsst.codes/sims

In order to run the Operations Simulator (SOCS/Scheduler), the following need to be installed::

	conda install lsst-sims-skybrightness lsst-pex-config enum34 pytz mysql-python requests sqlalchemy

If one wishes to develop the code, being able to run the unit tests, check style compliance and generate the documentation is a must. To do this, these packages need to be installed::

	conda install mock sphinx sphinx_rtd_theme flake8 coverage

There is one package that is required for the documentation but is not available via the conda packaging system. To get this package, do::

	pip install rst

Once the above is complete, setup the environment by doing::

	source eups-setups.sh

**NOTE**: If you are using CSH, you'll need the full path to the appropriate setup file (``eups-setups.csh``). To get this, execute the following command and a helpful message will tell you where to look::

	eups

With the environment setup, we need to declare and setup the SOCS and Scheduler packages so they can be used. Declare the Scheduler::

	cd gitdir/ts/ts_scheduler
	eups declare ts_scheduler git -r . -c

To declare and setup SOCS, do::

	cd gitdir/lsst-sims/sims_ocs
	eups declare sims_ocs git -r . -c
	setup sims_ocs
	python setup.py develop

**NOTE**: The declaration steps only need to be done once. After that, when returning to the same conda environment, do::

	source eups-setups.sh
	setup sims_ocs


Sky Brightness Model Data
-------------------------

In the previous, the pre-calculated sky brightness model was installed, but it does not come with the data required to run. The required data is ~65 GB in size, so create a directory for it. The instructions will assume one was created as ``$HOME/sky_brightness_data``. After running the ``setup sims_ocs`` command, change to this directory and execute the following::

	$SIMS_SKYBRIGHTNESS_PRE_DIR/data/data_down.sh -o 

While this set is completing, the instructions may continue to be followed, but OpSim will not function correctly until the data is done downloading.

.. _installation-database:

Database Setup
--------------

SOCS provides two mechanisms for simulation information storage: MySQL or SQLite. A script, ``manage_db`` has been created to help setup the necessary simulation related items for either case. In the case of MySQL, it is assumed that a running instance is already present and you have a ``.my.cnf`` file in ``$HOME`` that contains the connection information for a non-privileged user. It's also assumed you know the root password to the database as this will be required during setup. To see the options available::

	manage_db -h

The installation will cover a SQLite storage option. The following assumes a ``$HOME/run_local`` directory with an ``output`` sub-directory already available. To create the SQLite setup, run the following::

	manage_db -c --type=sqlite --save-dir=$HOME/run_local/output

This process creates in ``$HOME/run_local/output`` a ``<hostname>_session.db`` file where ``<hostname>`` is the name of your computer. If you have a DNS provided hostname and would like to have a more "normal" name, add the ``$OPSIM_HOSTNAME`` environmental variable to the session before running the above command. The script also creates a configuration file in ``$HOME/.config`` called ``opsim4`` and it contains the database setup information. This will allow you to not have to provide that information to the main simulation driver script.

If you wish to clear out your database and start over, but begin at the next run number from 
where you left off, this task can be accomplished. The ``-s`` flag to the ``manage_db`` will adjust the starting point for the run numbers. You will need the last run number generated and then pass that number incremented by one to the flag. For MySQL, this will set the base point for the autoincremented sessionId column in the Session table. For SQLite, the run number is written into the configuration file for later use when running the simulation.