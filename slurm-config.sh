#!/bin/bash

LEADER=${1:-$HOSTNAME}
NODES=${2:-$HOSTNAME}
CPUS=${3:-"ThreadsPerCore=2 CoresPerSocket=8 Sockets=2"}

sed -e "s/XXX/$LEADER/" -e "s/YYY/$NODES/" -e "s/ZZZ/$CPUS/" \
    /etc/slurm.conf.template > /usr/etc/slurm.conf
