FROM lsst/opsim4:base
MAINTAINER Michael Reuter <mareuter@lsst.org>

ARG SIMS_VERSION
ARG SOCS_VERSION
ARG SCHED_VERSION
ARG CONFUI_VERSION
ARG USER
ENV USER ${USER:-opsim}
ENV HOME /home/opsim

# Create user and group
RUN groupadd opsim && adduser -m -g opsim -s /bin/bash opsim

USER opsim
WORKDIR /home/opsim

RUN mkdir dds && mkdir repos && mkdir run-local && mkdir other-configs && \
    mkdir .config
VOLUME ["/home/opsim/run-local", "/home/opsim/other-configs", "/home/opsim4/.config"]

# Install Conda for python
RUN curl -Ok ftp://ftp.noao.edu/pub/lsst/mareuter/sched_stuff/Miniconda2-latest-Linux-x86_64.sh && bash Miniconda2-latest-Linux-x86_64.sh -b -p miniconda && \
  rm Miniconda2-latest-Linux-x86_64.sh

# Update Conda, set SIMS channel and install dependencies
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    conda config --add channels http://conda.lsst.codes/sims && \
    conda update -y conda && \
    conda install -y enum34 lsst-pex-config lsst-sims-skybrightness mysql-python pandas pytz requests sqlalchemy && \
    rm -rf miniconda/pkgs"

# Create a UUID file for Qt's DBUS
USER root
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    dbus-uuidgen > /etc/machine-id"
USER opsim

# Setup matplotlib's font cache
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    python -c 'import matplotlib.pyplot'"

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

# Declare repos to EUPS
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    source eups-setups.sh && \
    eups declare ts_scheduler git -r ./ts_scheduler -c && \
    eups declare sims_ocs git -r ./sims_ocs -c && \
    eups declare opsim4_config_ui git -r ./opsim4_config_ui -c"

# Setup sims_ocs
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    source eups-setups.sh && setup sims_ocs && \
    cd sims_ocs && \
    git checkout $SOCS_VERSION && \
    python setup.py develop && cd .."

# Setup ts_scheduler
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    source eups-setups.sh && setup ts_scheduler && \
    cd ts_scheduler && \
    git checkout $SCHED_VERSION && \
    cd .."

# Setup opsim4_config_ui
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    source eups-setups.sh && setup opsim4_config_ui && \
    cd opsim4_config_ui && \
    git checkout $CONFUI_VERSION && \
    python setup.py build_rcc && cd .."

WORKDIR /home/opsim

ENV NDDS_DISCOVERY_PEERS=builtin.shmem://
ENV OPENSPLICE_LOC=${HOME}/repos/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux
ENV OSPL_URI=file://${OPENSPLICE_LOC}/etc/config/ospl.xml
ENV SCHED_TOPIC_LIB=${HOME}/dds/lib
ENV LD_LIBRARY_PATH=${OPENSPLICE_LOC}/lib:${SCHED_TOPIC_LIB}:${LD_LIBRARY_PATH}
ENV PYTHONPATH=${SCHED_TOPIC_LIB}:${PYTHONPATH}
ENV PATH=$HOME/miniconda/bin:$PATH

ADD ./startup.sh /home/opsim/startup.sh
CMD ["/bin/bash", "/home/opsim/startup.sh"]
