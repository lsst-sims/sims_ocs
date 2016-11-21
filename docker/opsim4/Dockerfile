FROM mareuter/opsim4:base
MAINTAINER Michael Reuter <mareuter@lsst.org>

# Create user and group
RUN groupadd opsim && adduser -m -g opsim -s /bin/bash opsim

USER opsim
WORKDIR /home/opsim

RUN mkdir dds && mkdir repos && mkdir run-local

# Install Conda for python
RUN curl -Ok ftp://ftp.noao.edu/pub/lsst/mareuter/sched_stuff/Miniconda2-latest-Linux-x86_64.sh && bash Miniconda2-latest-Linux-x86_64.sh -b -p miniconda && \
  rm Miniconda2-latest-Linux-x86_64.sh

# Update Conda, set SIMS channel and install dependencies
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    conda config --add channels http://conda.lsst.codes/sims/2.3.1 && \
    conda update -y conda && \
    conda install -y enum34 lsst-pex-config lsst-sims-skybrightness mysql-python pandas pytz requests sqlalchemy"

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
    cd sims_ocs && python setup.py develop && cd .."

# Setup opsim4_config_ui
RUN bash -c "export PATH=/home/opsim/miniconda/bin:$PATH && \
    source eups-setups.sh && setup opsim4_config_ui && \
    cd opsim4_config_ui && python setup.py build_rcc && cd .."

WORKDIR /home/opsim

ADD ./startup.sh /home/opsim/startup.sh
CMD ["/bin/bash", "/home/opsim/startup.sh"]
