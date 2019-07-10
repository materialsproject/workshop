#!/bin/bash

export ME_CONFIG_SITE_BASEURL="/${JUPYTERHUB_SERVICE_PREFIX}mongo/"
mongod --dbpath=/home/jovyan/mongodb &
mongo-express -a -d mp_workshop
