#!/bin/bash
root_device=$(awk '/ \/ / {print $1}' /etc/fstab)
ln -sf "$root_device" /dev/root