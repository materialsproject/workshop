FROM jupyterhub/k8s-singleuser-sample:0.8.0

USER root
RUN locale-gen en_US.UTF-8
RUN apt-get update -q && apt-get install --yes gcc vim emacs mongodb
ENV BUILD_DEPS="git devscripts equivs apt-utils apache2-dev libslurm-dev python-setuptools cython python-dev libslurmdb-dev libslurm-dev ca-certificates"
ENV RUN_DEPS="apache2 libapache2-mod-wsgi javascript-common python-flask clustershell libjs-bootstrap libjs-jquery-flot libjs-jquery-tablesorter munge node-uglify fonts-dejavu-core python-ldap python-redis libjs-requirejs libjs-requirejs-text libjs-three libjs-d3 libjs-handlebars"
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

ENV SLURM_VER=17.11.0
RUN cd /usr/src && \
    git clone https://github.com/PySlurm/pyslurm.git && \
    cd pyslurm && \
    git checkout remotes/origin/$SLURM_VER && \
    sed -i 's/__max_slurm_hex_version__ = "0x0f0803"/__max_slurm_hex_version__ = "0x0f0807"/' setup.py && \
    tar cvfj ../python-pyslurm_$SLURM_VER.orig.tar.bz2 --exclude .git . && \
    mk-build-deps -ri -t "apt-get -y --no-install-recommends" && \
    dch -v $SLURM_VER-1 -D testing "New upstream release" && \
    debuild -us -uc && \
    dpkg -i ../python-pyslurm_$SLURM_VER-1_amd64.deb

RUN cd /usr/src && \
    git clone https://github.com/edf-hpc/opentypejs.git && \
    cd opentypejs && \
    git checkout debian/0.4.3-2 && \
	tar cvfj ../opentypejs_0.4.3.orig.tar.bz2 --exclude .git . && \
	mk-build-deps -ri -t "apt-get -y --no-install-recommends" && \
	debuild -us -uc && \
	dpkg -i ../node-opentypejs_0.4.3-2_all.deb

RUN cd /usr/src && \
	git clone https://github.com/edf-hpc/libjs-bootstrap-typeahead.git && \
	cd libjs-bootstrap-typeahead/ && \
    git checkout debian/0.11.1-1 && \
	tar cvfj ../libjs-bootstrap-typeahead_0.11.1.orig.tar.bz2 --exclude .git . && \
	debuild -us -uc && \
	dpkg -i ../libjs-bootstrap-typeahead_0.11.1-1_all.deb

RUN cd /usr/src && \
	git clone https://github.com/edf-hpc/libjs-bootstrap-tagsinput.git && \
	cd libjs-bootstrap-tagsinput/ && \
    git checkout debian/0.8.0-1 && \
	tar cvfj ../libjs-bootstrap-tagsinput_0.8.0.orig.tar.bz2 --exclude .git . && \
	debuild -us -uc && \
	dpkg -i ../libjs-bootstrap-tagsinput_0.8.0-1_all.deb

RUN cd /usr/src && \
    git clone https://github.com/edf-hpc/slurm-web.git && \
    cd slurm-web && \
    git checkout debian/2.0.0 && \
    debuild -us -uc && \
    dpkg -i ../slurm-web-*deb

RUN mkdir /etc/container_environment
RUN rm /etc/apache2/sites-available/default-ssl.conf && \
    echo www-data > /etc/container_environment/APACHE_RUN_USER && \
    echo www-data > /etc/container_environment/APACHE_RUN_GROUP && \
    echo /var/log/apache2 > /etc/container_environment/APACHE_LOG_DIR && \
    echo /var/lock/apache2 > /etc/container_environment/APACHE_LOCK_DIR && \
    echo /var/run/apache2.pid > /etc/container_environment/APACHE_PID_FILE && \
    echo /var/run/apache2 > /etc/container_environment/APACHE_RUN_DIR && \
    chown -R www-data:www-data /var/log/apache2
RUN mkdir -p /etc/service/apache2
COPY apache2.sh /etc/service/apache2/run
RUN chmod +x /etc/service/apache2/run

COPY start_slurm.sh /root/start_slurm.sh
RUN chmod +x /root/start_slurm.sh

RUN apt-get clean
#COPY fireworks /tmp/fireworks
#RUN chown -R jovyan:users /tmp/fireworks

USER $NB_USER
WORKDIR /home/jovyan
RUN mkdir /home/jovyan/mongodb
RUN npm install -g mongo-express
COPY start_mongo.sh /home/jovyan/start_mongo.sh
COPY start_fw.sh /home/jovyan/start_fw.sh
RUN pip install --no-cache-dir -e git+https://github.com/tschaume/fireworks.git#egg=fireworks
#RUN cd /tmp/fireworks && pip install --no-cache-dir -e .
RUN pip install --no-cache-dir jupyter-server-proxy
RUN pip install --no-cache-dir --upgrade Jinja2 python-dateutil
RUN pip install --upgrade --force jupyter ipython jupyter-console nbconvert
#RUN pip uninstall -y tornado && pip install tornado==5.1.1
COPY setup.py /home/jovyan/
COPY mp_workshop /home/jovyan/mp_workshop
RUN cd /home/jovyan/ && pip install --no-cache-dir -e .
COPY lessons /home/jovyan/work/lessons

USER root
RUN chown -R jovyan:users /home/jovyan/work/lessons
RUN chown -R jovyan:users /home/jovyan/mp_workshop

USER $NB_USER
RUN jupyter serverextension enable --sys-prefix jupyter_server_proxy
COPY server_proxy_config.py /tmp/server_proxy_config.py
RUN cat /tmp/server_proxy_config.py >> /home/jovyan/.jupyter/jupyter_notebook_config.py
WORKDIR /home/jovyan/work
