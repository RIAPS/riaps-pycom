#!/bin/bash
pycomrepo=`pwd`
version=0.3.2
tmpdir=`mktemp --directory`
mkdir $tmpdir/riaps-pycom_v$version
cd $tmpdir/riaps-pycom_v$version
git clone file:///$pycomrepo 
rm -rf $tmpdir/riaps-pycom_v$version/riaps-pycom/.git
tar cvzf riaps-pycom_v$version.tar.gz riaps-pycom
cp riaps-pycom_v$version.tar.gz $pycomrepo/.
rm -rf $tmpdir 
