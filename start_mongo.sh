#!/bin/bash

if [[ -z "${JUPYTERHUB_SERVICE_PREFIX}" ]]; then
  app_root="/"
else
  app_root="${JUPYTERHUB_SERVICE_PREFIX}"
fi

export ME_CONFIG_SITE_BASEURL="${app_root}mongo/"
mongod --dbpath=/home/jovyan/mongodb &
mongo-express -a -d mp_workshop
