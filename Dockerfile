FROM jupyterhub/k8s-singleuser-sample:0.8.0

# install additional package...
RUN pip install --no-cache-dir jupyter-server-proxy
RUN jupyter serverextension enable --sys-prefix jupyter_server_proxy
 
