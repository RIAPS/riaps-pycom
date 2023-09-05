#!/bin/bash

PYCOM_ETC_DIR="etc/riaps"
PYCOM_LN_DIR="usr/local/riaps"

usage="$(basename "$0") [-d] [-h]
Create Debian packages for indicated architecture. Use -d to create a developer package.
Arguments are:
    -h show this help text
    -d create a developer package (optional)"

dev="false"

while getopts hd option
do
  case "$option" in 
    h) echo "$usage"; exit;;
    d) echo "Developer Selected"; dev="true";;
  esac
done

rm -rf package
source version.sh

if [ $dev == "false" ]; then
  package_name="riaps-pycom"
else
  package_name="riaps-pycom-dev"
fi
echo "Package Name: $package_name"

mkdir -p package/$package_name/DEBIAN

if [ $dev == "false" ]; then
  cp -r DEBIAN/pkgfiles/control package/$package_name/DEBIAN/control
  cp -r DEBIAN/pkgfiles/postinst package/$package_name/DEBIAN/postinst
  cp -r DEBIAN/pkgfiles/postrm package/$package_name/DEBIAN/postrm
  cp -r DEBIAN/pkgfiles/prerm package/$package_name/DEBIAN/prerm
  cp -r DEBIAN/pkgfiles/conffiles package/$package_name/DEBIAN/conffiles
else
  cp -r DEBIAN/pkgfiles/control-dev package/$package_name/DEBIAN/control
  cp -r DEBIAN/pkgfiles/postinst-dev package/$package_name/DEBIAN/postinst
  cp -r DEBIAN/pkgfiles/postrm-dev package/$package_name/DEBIAN/postrm
  cp -r DEBIAN/pkgfiles/prerm-dev package/$package_name/DEBIAN/prerm
  cp -r DEBIAN/pkgfiles/conffiles-dev package/$package_name/DEBIAN/conffiles
fi

mkdir -p package/$package_name/opt/riaps-pycom/
mkdir -p package/$package_name/etc/
mkdir -p package/$package_name/$PYCOM_ETC_DIR/
mkdir -p package/$package_name/$PYCOM_LN_DIR/etc/
mkdir -p package/$package_name/$PYCOM_LN_DIR/keys/
mkdir -p package/$package_name/$PYCOM_LN_DIR/lang/

cp -r DEBIAN/sysfiles/etc/* package/$package_name/etc/.
cp -r pyproject.toml package/$package_name/opt/riaps-pycom/.
cp -r LICENSE package/$package_name/opt/riaps-pycom/.
cp -r README.md package/$package_name/opt/riaps-pycom/.
cp -r src package/$package_name/opt/riaps-pycom/.

cp -r src/riaps/etc/riaps.conf package/$package_name/$PYCOM_ETC_DIR/.
cp -r src/riaps/etc/riaps-log.conf package/$package_name/$PYCOM_ETC_DIR/.
cp -r src/riaps/etc/redis.conf package/$package_name/$PYCOM_ETC_DIR/.
if [ $dev == "true" ]; then
  cp -r src/riaps/etc/riaps-hosts.conf package/$package_name/$PYCOM_ETC_DIR/.
  cp -r src/riaps/etc/riaps-ctrl.glade package/$package_name/$PYCOM_ETC_DIR/.

  # Setup riaps-pycom-dev nic name to be the typical VM value
  sed s/"nic_name = eth0"/"# nic_name = eth0"/g -i package/$package_name/$PYCOM_ETC_DIR/riaps.conf
  sed s/"# nic_name = enp0s8"/"nic_name = enp0s8"/g -i package/$package_name/$PYCOM_ETC_DIR/riaps.conf
fi

cp -r src/riaps/lang/riaps.tx package/$package_name/$PYCOM_LN_DIR/lang/.
cp -r src/riaps/lang/depl.tx package/$package_name/$PYCOM_LN_DIR/lang/.
cp -r src/riaps/keys/id_rsa.key package/$package_name/$PYCOM_ETC_DIR/.
cp -r src/riaps/keys/id_rsa.pub package/$package_name/$PYCOM_ETC_DIR/.
cp -r src/riaps/keys/riaps-sys.cert package/$package_name/$PYCOM_ETC_DIR/.
cp -r src/riaps/keys/x509.pem package/$package_name/$PYCOM_ETC_DIR/.

sed s/@version@/$pycomversion/g -i package/$package_name/opt/riaps-pycom/pyproject.toml
sed s/@version@/$pycomversion/g -i package/$package_name/DEBIAN/control

fakeroot dpkg-deb --build package/$package_name
cp package/$package_name.deb .

