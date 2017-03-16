#!/bin/bash

pycomrepo=`pwd`

#we need the version variable to be set
source version
tmpdir=`mktemp --directory`
mkdir -p $tmpdir
cd $tmpdir
pwd
git clone file:///$pycomrepo 
sed -i s/@version@/$version/g riaps-pycom/src/setup.py
cat riaps-pycom/src/setup.py
tar cvzf riaps-pycom_v$version.tar.gz riaps-pycom
cp riaps-pycom_v$version.tar.gz $pycomrepo/.
#rm -rf $tmpdir 
