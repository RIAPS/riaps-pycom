#!/bin/bash
pycomrepo=`pwd`
version=0.3.3
tmpdir=`mktemp --directory`
mkdir -p $tmpdir
cd $tmpdir
pwd
git clone file:///$pycomrepo 
tar cvzf riaps-pycom_v$version.tar.gz riaps-pycom
cp riaps-pycom_v$version.tar.gz $pycomrepo/.
rm -rf $tmpdir 
