FROM mareuter/opsim4:base
MAINTAINER Michael Reuter <mareuter@lsst.org>

# Create user and group
RUN groupadd opsim && adduser -m -g opsim -s /bin/bash opsim

USER opsim
WORKDIR /home/opsim

RUN mkdir dds && mkdir repos

# Install Scheduler DDS topic library
WORKDIR /home/opsim/dds
RUN curl -Ok ftp://ftp.noao.edu/pub/lsst/mareuter/sched_stuff/scheduler_ddslibs.tar.gz && \
  tar zxvf scheduler_ddslibs.tar.gz && rm scheduler_ddslibs.tar.gz

# Clone all repos
WORKDIR /home/opsim/repos
RUN git clone https://github.com/lsst-ts/ts_opensplice.git

WORKDIR /home/opsim

ADD ./startup.sh /home/opsim/startup.sh
CMD ["/bin/bash", "/home/opsim/startup.sh"]
