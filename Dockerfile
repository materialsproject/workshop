FROM jupyterhub/k8s-singleuser-sample:0.8.0

# install additional package...
RUN pip install --no-cache-dir jupyter-server-proxy
RUN jupyter serverextension enable --sys-prefix jupyter_server_proxy
COPY server_proxy_config.py /tmp/server_proxy_config.py
RUN cat /tmp/server_proxy_config.py >> /home/jovyan/.jupyter/jupyter_notebook_config.py 
