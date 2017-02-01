FROM lsst/opsim4:base-linux
MAINTAINER Michael Reuter <mareuter@lsst.org>

ENV HOME /home/opsim

RUN mkdir -p /lsst/stack /lsst/repos /lsst/dds /opsim && \
	groupadd opsim && adduser -m -g opsim -s /bin/bash -u 1099 opsim && \
	chown -R opsim:opsim /lsst && chown -R opsim:opsim /opsim

COPY ./startup.sh /usr/local/bin/startup.sh
CMD ["/bin/bash", "/usr/local/bin/startup.sh"]