#!/bin/bash
# This script will check the Python version for the system and change the 
# RIAPS apparmor file to match

# Path to the file that contains the version string
riaps_apparmor_file="/etc/apparmor.d/usr.local.bin.riaps_actor"

# Get the system's Python version (only major and minor)
system_pyversion=$(python3 -c 'import platform; python_version=platform.python_version_tuple(); print(python_version[0] + "." + python_version[1])')

# Read the current version from the file (assumes there's only one occurrence)
current_apparmor_pyversion=$(grep -oP '@\{PYTHONVERSION\}=\K\d+\.\d+' "$riaps_apparmor_file")

# Check if the system version is different from the current version in the file
if [[ "$system_pyversion" != "$current_apparmor_pyversion" ]]; then
    # Use sed to replace the version in the file in-place
    sudo sed -i "s/@{PYTHONVERSION}=$current_apparmor_pyversion/@{PYTHONVERSION}=$system_pyversion/" "$riaps_apparmor_file"
fi