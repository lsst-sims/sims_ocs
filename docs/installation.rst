============
Installation
============

.. warning::

	The current installation is not for the faint of heart as it requires multiple repositories and a mixture of environments. It also only works on a RHEL 7 type environment.

General Installation Notes
--------------------------

Due to the heavy use of repositiories for this installation, the instructions will assume you have created a ``git`` directory in your ``$HOME`` directory. This will be referenced as ``gitdir``. The individual repository installation instructions will give further advice on directory names. This is intended to make the usage "easier". Also, all instructions are based around using the code, not developing it.

SAL Installation
----------------

The SAL (Software Abstraction Layer) is a wrapper around the DDS layer and provides binding to Python. This requires the OpenSplice and SAL repositories from Telescope and Site. Inside the ``gitdir`` create a directory called ``ts``. Go into this directory and run the following::

	git clone https://stash.lsstcorp.org/scm/ts/ts_opensplice.git
	git clone https://stash.lsstcorp.org/scm/ts/ts_sal.git

Build Scheduler Topic Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are prerequisites that need to be installed to build the topic library. They can be installed via the ``yum install`` command. They are::
	
	g++
	make
	cmake
	ncurses-libs
	xterm
	xorg-x11-fonts-misc
	java-1.7.0-openjdk-devel
	boost-python
	boost-python-devel
	maven
	python-devel
	swig
	tk-devel

Create a ``$HOME/dds`` directory and copy the ``gitdir/ts/ts_sal/setup.env`` to it. Also, create a ``$HOME/dds/lib`` directory for later. The following variables need to be edited in ``setup.env`` to reflect your setup::

	export LSST_SDK_INSTALL=$HOME/git/ts/ts_sal
	export OSPL_HOME=$HOME/git/ts/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux

All other variables can remain the same. Once the edits are complete, do::

	source $HOME/dds/setup.env

The configuration should complete without errors. Go back to ``gitdir/ts/ts_sal`` and do the following::

	git co -t origin/feature/scheduler_xml_devel
	cd test
	salgenerator scheduler validate
	salgenerator scheduler sal cpp
	salgenerator scheduler sal python

Once the build is complete, the topic and supporting library need to be copied via the following::

	cp scheduler/cpp/src/SALPY_scheduler.so $HOME/dds/lib
	cp scheduler/cpp/libsacpp_scheduler_types.so $HOME/dds/lib

There are firewall rules that need to be applied in order for the DDS communications to work directly. Please see a developer for these.

Scheduler Installation
----------------------

The Scheduler repository should also be cloned to ``gitdir/ts`` via the following::

	git clone https://stash.lsstcorp.org/scm/ts/ts_scheduler.git

SOCS Installation
-----------------

The SOCS repository should be cloned into the ``gitdir``. Create a directory there called ``lsst-sims``, go into that and run the following::

	git clone https://github.com/lsst-sims/sims_ocs.git

The SOCS installation requires a set of Python modules. It is recommended to install a clean version of Python via a mechanism like 
`Miniconda <http://conda.pydata.org/miniconda.html>`_. A configuration module is also necessary from the LSST Stack, so this will need to be setup as well.

Conda Installation
~~~~~~~~~~~~~~~~~~

Install miniconda from the above link. It is assumed that the ``bin`` directory from the installation will make it into the ``$PATH`` somehow. This is one of the few places where the user gets to choose how to do this. Next, create a Conda environment and activate it::

	conda create -n opsim4_py2 python=2
	source activate opsim4_py2

LSST Stack Installation
~~~~~~~~~~~~~~~~~~~~~~~

To install the LSST Stack (this really is only a skeleton setup and not the full stack!), do the following:

  .. code-block:: bash

    mkdir -p $HOME/lsst
    cd $HOME/lsst
    curl -O https://sw.lsstcorp.org/eupspkg/newinstall.sh
    # script below will ask some questions. Answer no to the python since we are using 
    # the miniconda installation.
    bash newinstall.sh
    source loadLSST.bash

Once this is completed, install the necessary configuration module::

	eups distrib install pex-config

SOCS Setup
~~~~~~~~~~

Once the above is completed, you will need to install the Python modules from ``gitdir/lsst-sims/sims_ocs/requirements.txt``. Not all the modules are avaiable via ``conda install`` so you'll have to resort to ``pip install`` when necessary. With all the modules installed, do the following (while in ``gitdir/lsst-sims/sims_ocs``)::

	eups declare -r . -t $USER sims_ocs
	setup sims_ocs -t $USER
	python setup.py develop

The last setup is necessary even if you aren't developing the code. It creates the version information module for the code.

Database Setup
--------------

SOCS provides two mechanisms for simulation information storage: MySQL or SQLite. A script, ``manage_db`` has been create to help setup the necessary simulation related items for either case. In the case of MySQL, it is assumed that a running instance is already present and you have a ``.my.cnf`` file in ``$HOME`` that contains the connection information for a non-privileged user. It's also assumed you know the root password to the database as this will be required during setup. To see the options available::

	manage_db -h

The installation will cover a SQLite storage option. The following assumes a ``$HOME/run_local`` directory with ``log`` and ``output`` sub-directories are already available. To create the SQLite setup, run the following::

	manage_db -c --type=sqlite --save-dir=$HOME/run_local/output

This process creates in ``$HOME/run_local/output`` a ``<hostname>_session.db`` file where ``<hostname>`` is the name of your computer. If you have a DNS provided hostname and would like to have a more "normal" name, add the ``$OPSIM_HOSTNAME`` environmental variable to the session before running the above command. The script also creates a configuration file in ``$HOME/.config`` called ``opsim4`` and it contains the database setup information. This will allow you to not have to provide that information to the main simulation driver script.