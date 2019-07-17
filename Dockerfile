FROM jupyter/base-notebook:7a3e968dd212
# Built from... https://hub.docker.com/r/jupyter/base-notebook/
#               https://github.com/jupyter/docker-stacks/blob/master/base-notebook/Dockerfile
# Built from... Ubuntu 18.04

USER root
RUN locale-gen en_US.UTF-8
RUN apt-get update -q && apt-get install --yes gcc vim emacs mongodb graphviz
ENV BUILD_DEPS="git devscripts equivs apt-utils apache2-dev libslurm-dev python-setuptools cython python-dev libslurmdb-dev libslurm-dev ca-certificates"
ENV RUN_DEPS="apache2 libapache2-mod-wsgi javascript-common python-flask clustershell libjs-bootstrap libjs-jquery-flot libjs-jquery-tablesorter libmunge-dev munge node-uglify fonts-dejavu-core python-ldap python-redis libjs-requirejs libjs-requirejs-text libjs-three libjs-d3 libjs-handlebars"
RUN apt-get update -q && apt-get -y install $BUILD_DEPS $RUN_DEPS
RUN ln -s /usr/lib/x86_64-linux-gnu/ /usr/lib64
RUN a2enmod wsgi && a2enconf javascript-common

# apt could not locate slurm-llnl
WORKDIR /root
RUN wget https://github.com/SchedMD/slurm/archive/slurm-17-11-8-1.tar.gz
RUN cd /usr/src && tar axvf /root/slurm-17-11-8-1.tar.gz && cd /usr/src/slurm-slurm-17-11-8-1 && \
      ./configure --prefix=/usr && make -j && make install && \
      rm -rf /usr/src/slurm-slurm-17-11-8-1 && rm -f /root/slurm-17-11-8-1.tar.gz
RUN git clone https://github.com/jamesmcclain/SlurmDocker.git && cd SlurmDocker && cp config/slurm.conf.template /etc/
RUN apt-get clean

#COPY fireworks /tmp/fireworks
#RUN chown -R jovyan:users /tmp/fireworks

USER $NB_USER
WORKDIR /home/jovyan
RUN mkdir /home/jovyan/mongodb
COPY start_fw.sh /home/jovyan/start_fw.sh
ADD https://api.github.com/repos/tschaume/fireworks/git/refs/heads/master version.json
RUN git clone https://github.com/tschaume/fireworks.git
RUN cd fireworks && pip install --no-cache-dir -e .
#RUN cd /tmp/fireworks && pip install --no-cache-dir -e .
RUN pip install --no-cache-dir --upgrade Jinja2 python-dateutil
RUN pip install --no-cache-dir jupyter-server-proxy
RUN pip install --upgrade --ignore-installed terminado --force jupyter ipython jupyter-console nbconvert
COPY setup.py /home/jovyan/
COPY mp_workshop /home/jovyan/mp_workshop
RUN cd /home/jovyan/ && pip install --no-cache-dir -e .
COPY lessons /home/jovyan/work/lessons
COPY slurm-config.sh /home/jovyan/slurm-config.sh

USER root
RUN chown -R jovyan:users /home/jovyan/work/lessons
RUN chown -R jovyan:users /home/jovyan/mp_workshop
RUN chmod +x /home/jovyan/slurm-config.sh
RUN mkdir -p /usr/etc && touch /usr/etc/slurm.conf && chown -R jovyan:users /usr/etc
RUN mkdir -p /var/{log,lib,run}/munge && chown jovyan:users /var/{log,lib,run}/munge
RUN mkdir -p /var/run/spool && chown jovyan:users /var/run/spool
RUN PASSWORD=${1:-"Setec Astronomy"} && \
  echo -n $PASSWORD | sha512sum | cut -d' ' -f1 > /tmp/munge.key && \
  chown jovyan:users /tmp/munge.key && \
  chmod go-rwx /tmp/munge.key


USER $NB_USER
RUN pip install --no-cache-dir --upgrade pythreejs
RUN jupyter nbextension install --user --py pythreejs
RUN jupyter nbextension enable --user --py pythreejs
RUN pip install --no-cache-dir -e git+https://github.com/materialsproject/crystaltoolkit.git#egg=crystaltoolkit

USER $NB_USER
RUN jupyter serverextension enable --sys-prefix jupyter_server_proxy
COPY server_proxy_config.py /tmp/server_proxy_config.py
RUN cat /tmp/server_proxy_config.py >> /home/jovyan/.jupyter/jupyter_notebook_config.py
COPY POTCARs.tar.gz /home/jovyan/
RUN tar -xvzf /home/jovyan/POTCARs.tar.gz -C /home/jovyan/
RUN echo "PMG_VASP_PSP_DIR: /home/jovyan/POTCARs" >> /home/jovyan/.pmgrc.yaml

# MPContribs
ADD https://api.github.com/repos/materialsproject/MPContribs/git/refs/heads/dev version.json
RUN git clone -b dev https://github.com/materialsproject/MPContribs.git
WORKDIR /home/jovyan/MPContribs
ENV SETUPTOOLS_SCM_PRETEND_VERSION 1.6.0
RUN cd mpcontribs-client && pip install --no-cache-dir -e .
RUN cd mpcontribs-io && pip install --no-cache-dir -e .
RUN npm install 2>&1
RUN cp -v binder/binder.js . && \
    cp -v webpack-binder.config.js webpack.config.js && \
    npm run webpack 2>&1
RUN mkdir /home/jovyan/.jupyter/custom && \
    mv -v dist /home/jovyan/.jupyter/custom/js
#RUN cp -v binder/custom.js /home/jovyan/.jupyter/custom/
RUN mkdir /home/jovyan/work/lessons/MPContribs/ && \
    cp -v binder/*.ipynb /home/jovyan/work/lessons/MPContribs/
RUN export FW_CONFIG_FILE="/home/jovyan/mp_workshop/fireworks_config/FW_config.yaml"

WORKDIR /home/jovyan/work
