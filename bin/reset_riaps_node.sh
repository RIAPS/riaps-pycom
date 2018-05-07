#!/usr/bin/env bash

for KILLPID in `ps ax | grep 'riaps_' | awk ' { print $1;}'`; do
  sudo kill -9 $KILLPID;
done

sudo rm -R /home/riaps/riaps_apps/riaps-apps.lmdb/
sudo rm -R /home/riaps/riaps_apps/DistributedEstimator/
sudo userdel distributedestimator9cbd