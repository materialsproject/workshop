FROM jupyterhub/k8s-singleuser-sample:0.8.0

USER root
RUN apt-get update && apt-get install --yes \
  gcc \
  vim \
  emacs \
  mongodb \
&& rm -rf /var/lib/apt/lists/* 

USER $NB_USER
# install additional package...
RUN pip install --no-cache-dir jupyter-server-proxy atomate
RUN jupyter serverextension enable --sys-prefix jupyter_server_proxy
COPY server_proxy_config.py /tmp/server_proxy_config.py
RUN cat /tmp/server_proxy_config.py >> /home/jovyan/.jupyter/jupyter_notebook_config.py 
RUN mkdir /home/jovyan/mongodata
