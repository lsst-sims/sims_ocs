FROM lsst/opsim4:base
MAINTAINER Michael Reuter <mareuter@lsst.org>

ENV USER ${USER:-opsim}
ENV HOME /home/opsim

# Create user and group
RUN groupadd opsim && adduser -m -g opsim -s /bin/bash opsim

USER opsim
WORKDIR /home/opsim

RUN mkdir stack && \
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
    python -c 'import matplotlib.pyplot' && \
    conda clean -ay && \
    rm -rfv /home/opsim/stack/Linux64/miniconda2/*/pkgs"

# Create a UUID file for Qt's DBUS
USER root
RUN bash -c "source /home/opsim/stack/loadLSST.bash && \
    dbus-uuidgen > /etc/machine-id"
USER opsim
