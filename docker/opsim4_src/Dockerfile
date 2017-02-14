FROM lsst/opsim4:base-src
MAINTAINER Michael Reuter <mareuter@lsst.org>

ARG INSTALL_MINICONDA=Y
ARG SOCS_VERSION
ARG	SCHED_VERSION 
ARG	CONFUI_VERSION
ARG	USER
ENV USER ${USER:-opsim} \
	HOME /home/opsim

# Create user and group
RUN groupadd opsim && adduser -m -g opsim -s /bin/bash opsim

USER opsim
WORKDIR /home/opsim

RUN mkdir dds repos stack

WORKDIR /home/opsim/stack

RUN curl -OL https://raw.githubusercontent.com/lsst/lsst/master/scripts/newinstall.sh && \
		bash newinstall.sh -b && \
		bash -c "source loadLSST.bash && \
		eups distrib install sims_skybrightness -t sims && \
		eups distrib install pex_config && \
		conda update -y conda && \
		conda update -y pyqt && \
		conda install -y enum34 mysql-python pandas pytz requests sqlalchemy && \
		rm -rf miniconda/pkgs && \
		python -c 'import matplotlib.pyplot'"

# Create a UUID file for Qt's DBUS
USER root
RUN bash -c "source /home/opsim/stack/loadLSST.bash && \
    dbus-uuidgen > /etc/machine-id"
USER opsim

# Install Scheduler DDS topic library
WORKDIR /home/opsim/dds
RUN curl -Ok ftp://ftp.noao.edu/pub/lsst/mareuter/sched_stuff/scheduler_ddslibs.tar.gz && \
  tar zxvf scheduler_ddslibs.tar.gz && rm scheduler_ddslibs.tar.gz

# Clone all repos
WORKDIR /home/opsim/repos
RUN git clone https://github.com/lsst-ts/ts_opensplice.git && \
    git clone https://github.com/lsst-ts/ts_scheduler.git && \
    git clone https://github.com/lsst-sims/sims_ocs.git && \
    git clone https://github.com/lsst-sims/opsim4_config_ui.git && \
    git clone https://github.com/lsst-sims/opsim4_tools.git

# Declare repos to EUPS and perform setup
RUN bash -c "source /home/opsim/stack/loadLSST.bash && \
    eups declare ts_scheduler git -r ./ts_scheduler -c && \
    eups declare sims_ocs git -r ./sims_ocs -c && \
    eups declare opsim4_config_ui git -r ./opsim4_config_ui -c && \
    setup sims_ocs && \
    cd sims_ocs && \
    git checkout $SOCS_VERSION && \
    python setup.py develop && \
    cd ../ && \
    setup ts_scheduler && \
    cd ts_scheduler && \
    git checkout $SCHED_VERSION && \
    cd .. && \
    setup opsim4_config_ui && \
    cd opsim4_config_ui && \
    git checkout $CONFUI_VERSION && \
    python setup.py build_rcc && cd .."

WORKDIR /home/opsim

ENV NDDS_DISCOVERY_PEERS=builtin.shmem:// \
    OPENSPLICE_LOC=${HOME}/repos/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux \
    OSPL_URI=file://${OPENSPLICE_LOC}/etc/config/ospl.xml \
    SCHED_TOPIC_LIB=${HOME}/dds/lib \
    LD_LIBRARY_PATH=${OPENSPLICE_LOC}/lib:${SCHED_TOPIC_LIB}:${LD_LIBRARY_PATH} \
    PYTHONPATH=${SCHED_TOPIC_LIB}:${PYTHONPATH} \
    PATH=$HOME/miniconda/bin:$PATH

ADD ./startup.sh /home/opsim/startup.sh
CMD ["/bin/bash", "/home/opsim/startup.sh"]
