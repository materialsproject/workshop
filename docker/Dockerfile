FROM materialsproject/mp_workshop_base:latest

USER $NB_USER
WORKDIR /home/jovyan

ADD https://api.github.com/repos/tschaume/fireworks/git/refs/heads/master version.json
RUN git clone https://github.com/tschaume/fireworks.git
RUN cd fireworks && pip install --no-cache-dir -e .

ADD https://api.github.com/repos/materialsproject/crystaltoolkit/git/refs/heads/master version.json
RUN git clone https://github.com/materialsproject/crystaltoolkit.git
RUN cd crystaltoolkit && pip install --no-cache-dir -e .

ADD https://api.github.com/repos/materialsproject/MPContribs/git/refs/heads/dev version.json
RUN git clone -b dev https://github.com/materialsproject/MPContribs.git
RUN mv node_modules MPContribs

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

WORKDIR /home/jovyan
COPY start_fw.sh /home/jovyan/start_fw.sh
COPY setup.py /home/jovyan/
COPY mp_workshop /home/jovyan/mp_workshop
COPY lessons /home/jovyan/work/lessons
COPY slurm-config.sh /home/jovyan/slurm-config.sh
COPY server_proxy_config.py /tmp/server_proxy_config.py
RUN cat /tmp/server_proxy_config.py >> /home/jovyan/.jupyter/jupyter_notebook_config.py
COPY POTCARs.tar.gz /home/jovyan/
RUN tar -xvzf /home/jovyan/POTCARs.tar.gz -C /home/jovyan/
RUN echo "PMG_VASP_PSP_DIR: /home/jovyan/POTCARs" >> /home/jovyan/.pmgrc.yaml
RUN export FW_CONFIG_FILE="/home/jovyan/mp_workshop/fireworks_config/FW_config.yaml"

USER root
RUN chown -R jovyan:users /home/jovyan/work/lessons
RUN chown -R jovyan:users /home/jovyan/mp_workshop
RUN chmod +x /home/jovyan/slurm-config.sh

USER $NB_USER
RUN mkdir /home/jovyan/work/lessons/MPContribs/ && \
    cp -v /home/jovyan/MPContribs/binder/*.ipynb /home/jovyan/work/lessons/MPContribs/
RUN cd /home/jovyan/ && pip install --no-cache-dir -e .

WORKDIR /home/jovyan/work
