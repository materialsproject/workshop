#!/bin/bash

export ME_CONFIG_SITE_BASEURL="/mongo/"
mongod --dbpath=/home/jovyan/mongodb &
mongo-express
