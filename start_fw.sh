#!/bin/bash

if [[ -z "${JUPYTERHUB_SERVICE_PREFIX}" ]]; then
  app_root="/"
else
  app_root="${JUPYTERHUB_SERVICE_PREFIX}"
fi

export FW_APPLICATION_ROOT="${app_root}fireworks/"
python -c 'import mp_workshop.fireworks_config'
export FW_CONFIG_FILE="$HOME/mp_workshop/fireworks_config/FW_config.yaml"
lpad webgui -s --nworkers 1
