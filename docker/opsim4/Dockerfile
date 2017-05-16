FROM lsst/opsim4:stack
MAINTAINER Michael Reuter <mareuter@lsst.org>

ARG SOCS_VERSION
ARG	SCHED_VERSION 
ARG	CONFUI_VERSION
ARG	DATELOC_VERSION
ARG	ASTROSKY_VERSION
ARG	OBSMOD_VERSION
#ARG	USER
#ENV USER ${USER:-opsim}
#ENV HOME /home/opsim

# Create user and group
#RUN groupadd opsim && adduser -m -g opsim -s /bin/bash opsim

USER opsim
WORKDIR /home/opsim

RUN mkdir dds repos && \
    cd dds && \
    curl -Ok ftp://ftp.noao.edu/pub/lsst/mareuter/sched_stuff/scheduler_ddslibs.tar.gz && \
    tar zxvf scheduler_ddslibs.tar.gz && \
    rm scheduler_ddslibs.tar.gz && \
    cd ../ && \
    cd repos && \
    git clone https://github.com/lsst-ts/ts_opensplice.git && \
    git clone https://github.com/lsst-ts/ts_dateloc.git && \
    git clone https://github.com/lsst-ts/ts_astrosky_model.git && \
    git clone https://github.com/lsst-ts/ts_observatory_model.git && \
    git clone https://github.com/lsst-ts/ts_scheduler.git && \
    git clone https://github.com/lsst/sims_utils.git && \
    git clone https://github.com/lsst/sims_skybrightness_pre.git && \
    git clone https://github.com/lsst-sims/sims_ocs.git && \
    git clone https://github.com/lsst-sims/opsim4_config_ui.git && \
    git clone https://github.com/lsst-sims/opsim4_tools.git && \
    cd ../ && \
    bash -c "source stack/loadLSST.bash && \
    eups declare sims_utils git -r ./repos/sims_utils -c && \
    eups declare sims_skybrightness_pre git -r ./repos/sims_skybrightness_pre -c && \
    eups declare ts_dateloc git -r ./repos/ts_dateloc -c && \
    eups declare ts_astrosky_model git -r ./repos/ts_astrosky_model -c && \
	eups declare ts_observatory_model git -r ./repos/ts_observatory_model -c && \
    eups declare ts_scheduler git -r ./repos/ts_scheduler -c && \
    eups declare sims_ocs git -r ./repos/sims_ocs -c && \
    eups declare opsim4_config_ui git -r ./repos/opsim4_config_ui -c && \
    cd repos && \
    cd sims_utils && \
    setup sims_utils git && \
    scons && \
    cd ../ && \
    cd sims_skybrightness_pre && \
    setup sims_skybrightness_pre git && \
    scons && \
    cd ../ && \
    cd ts_dateloc && \
    git checkout $DATELOC_VERSION && \
    setup ts_dateloc git && \
    scons && \
    cd ../ && \
    cd ts_astrosky_model && \
    git checkout $ASTROSKY_VERSION && \
    setup ts_astrosky_model git && \
    scons && \
    cd ../ && \
    cd ts_observatory_model && \
    git checkout $OBSMOD_VERSION && \
    setup ts_observatory_model git && \
    scons && \
    cd ../ && \
    cd sims_ocs && \
    git checkout $SOCS_VERSION && \
    setup sims_ocs git && \
    scons && \
    cd ../ && \
    cd ts_scheduler && \
    git checkout $SCHED_VERSION && \
    setup ts_scheduler git && \
    scons && \
    cd .. && \
    cd opsim4_config_ui && \
    git checkout $CONFUI_VERSION && \
    setup opsim4_config_ui git && \
    scons && \
    cd .."

ENV NDDS_DISCOVERY_PEERS=builtin.shmem:// \
    OPENSPLICE_LOC=${HOME}/repos/ts_opensplice/OpenSpliceDDS/V6.4.1/HDE/x86_64.linux \
    SCHED_TOPIC_LIB=${HOME}/dds/lib \
    SIMS_SKYBRIGHTNESS_DATA=${HOME}/sky_brightness_data
ENV OSPL_URI=file://${OPENSPLICE_LOC}/etc/config/ospl.xml \
    LD_LIBRARY_PATH=${OPENSPLICE_LOC}/lib:${SCHED_TOPIC_LIB}:${LD_LIBRARY_PATH} \
    PYTHONPATH=${SCHED_TOPIC_LIB}:${PYTHONPATH}

ADD ./startup.sh /home/opsim/startup.sh
ADD ./.opsim4_profile /home/opsim/.opsim4_profile
CMD ["/bin/bash", "/home/opsim/startup.sh"]