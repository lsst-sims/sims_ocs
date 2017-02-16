FROM lsst/opsim4:base
MAINTAINER Michael Reuter <mareuter@lsst.org>

ARG SOCS_VERSION
ARG	SCHED_VERSION 
ARG	CONFUI_VERSION
ARG	USER
ENV USER ${USER:-opsim}
#HOME /home/opsim

# Create user and group
RUN groupadd opsim && adduser -m -g opsim -s /bin/bash opsim

USER opsim
WORKDIR /home/opsim

RUN mkdir dds repos stack && \
    cd dds && \
    curl -Ok ftp://ftp.noao.edu/pub/lsst/mareuter/sched_stuff/scheduler_ddslibs.tar.gz && \
    tar zxvf scheduler_ddslibs.tar.gz && \
    rm scheduler_ddslibs.tar.gz && \
    cd ../ && \
    cd repos && \
    git clone https://github.com/lsst-ts/ts_opensplice.git && \
    git clone https://github.com/lsst-ts/ts_scheduler.git && \
    git clone https://github.com/lsst/sims_utils.git && \
    git clone https://github.com/lsst/sims_skybrightness_pre.git && \
    git clone https://github.com/lsst-sims/sims_ocs.git && \
    git clone https://github.com/lsst-sims/opsim4_config_ui.git && \
    git clone https://github.com/lsst-sims/opsim4_tools.git && \
    cd ../ && \
    cd stack && \
    curl -OL https://raw.githubusercontent.com/lsst/lsst/master/scripts/newinstall.sh && \
	bash newinstall.sh -b && \
	bash -c "source loadLSST.bash && \
	eups distrib install sims_utils -t sims && \
	eups distrib install pex_config -t sims && \
	conda update -y conda && \
	conda update -y pyqt fontconfig sqlalchemy && \
	conda install -y mysql-python pandas && \
    cd ../ && \
    eups declare sims_utils git -r ./repos/sims_utils -c && \
    eups declare sims_skybrightness_pre git -r ./repos/sims_skybrightness_pre -c && \
    eups declare ts_scheduler git -r ./repos/ts_scheduler -c && \
    eups declare sims_ocs git -r ./repos/sims_ocs -c && \
    eups declare opsim4_config_ui git -r ./repos/opsim4_config_ui -c && \
    setup sims_ocs git && \
    cd repos && \
    cd sims_utils && \
    scons && \
    cd ../ && \
    cd sims_skybrightness_pre && \
    scons && \
    cd ../ && \
    cd sims_ocs && \
    git checkout $SOCS_VERSION && \
    scons && \
    cd ../ && \
    cd ts_scheduler && \
    git checkout $SCHED_VERSION && \
    scons && \
    cd .. && \
    setup opsim4_config_ui git && \
    cd opsim4_config_ui && \
    git checkout $CONFUI_VERSION && \
    scons && \
    cd .. && \
    python -c 'import matplotlib.pyplot' && \
    rm -rfv /home/opsim/stack/Linux64/miniconda2/*/pkgs"

# Create a UUID file for Qt's DBUS
USER root
RUN bash -c "source /home/opsim/stack/loadLSST.bash && \
    dbus-uuidgen > /etc/machine-id"
USER opsim

WORKDIR /home/opsim

ENV NDDS_DISCOVERY_PEERS=builtin.shmem:// \
    OPENSPLICE_LOC=${HOME}/repos/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux \
    OSPL_URI=file://${OPENSPLICE_LOC}/etc/config/ospl.xml \
    SCHED_TOPIC_LIB=${HOME}/dds/lib \
    LD_LIBRARY_PATH=${OPENSPLICE_LOC}/lib:${SCHED_TOPIC_LIB}:${LD_LIBRARY_PATH} \
    PYTHONPATH=${SCHED_TOPIC_LIB}:${PYTHONPATH} \
    SIMS_SKYBRIGHTNESS_DATA=${HOME}/sky_brightness_data

ADD ./startup.sh /home/opsim/startup.sh
ADD ./.opsim4_profile /home/opsim/.opsim4_profile
CMD ["/bin/bash", "/home/opsim/startup.sh"]
