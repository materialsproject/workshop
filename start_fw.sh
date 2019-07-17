#!/bin/bash

mongod --dbpath=/home/jovyan/mongodb &

if [ ! -s /usr/etc/slurm.conf ]; then
    name=`hostname -s`
    /home/jovyan/slurm-config.sh $name $name CPUs=1
    echo "SlurmUser=jovyan" >> /usr/etc/slurm.conf
    echo "SlurmdUser=jovyan" >> /usr/etc/slurm.conf
    echo "SlurmdSpoolDir=/var/run/spool" >> /usr/etc/slurm.conf
    echo "slurm.conf generated."
fi

/usr/sbin/munged -f --syslog --key-file=/tmp/munge.key --pid-file=/tmp/munged.pid --socket=/tmp/munge.socket.2
/usr/sbin/slurmctld -c
/usr/sbin/slurmd -c
sinfo

if [[ -z "${JUPYTERHUB_SERVICE_PREFIX}" ]]; then
  app_root="/"
else
  app_root="${JUPYTERHUB_SERVICE_PREFIX}"
fi

export FW_APPLICATION_ROOT="${app_root}fireworks/"
export FW_CONFIG_FILE="/home/jovyan/mp_workshop/fireworks_config/FW_config.yaml"
lpad webgui -s --nworkers 1
