#!/bin/bash

usage="$(basename "$0") [-d] [-h]
Create Debian packages for indicated architecture. Use -d to create a developer package (for the controller system).
Arguments are:
    -h show this help text
    -d create a developer package (optional)"

dev="false"

while getopts hd option
do
  case "$option" in 
    h) echo "$usage"; exit;;
    d) echo "Dev Selected"; dev="true";;
  esac
done

echo "Developer Package: $dev"

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
  cp -r DEBIAN/pkgfiles/conffiles package/$package_name/DEBIAN/conffiles
  cp -r DEBIAN/pkgfiles/postinst package/$package_name/DEBIAN/postinst
  cp -r DEBIAN/pkgfiles/postrm package/$package_name/DEBIAN/postrm
  cp -r DEBIAN/pkgfiles/prerm package/$package_name/DEBIAN/prerm

  mkdir -p package/$package_name/opt/riaps-pycom/
  mkdir -p package/$package_name/etc/
  mkdir -p package/$package_name/etc/riaps/
  mkdir -p package/$package_name/usr/local/bin/
  mkdir -p package/$package_name/usr/local/riaps/etc/
  mkdir -p package/$package_name/usr/local/riaps/keys/
  mkdir -p package/$package_name/usr/local/riaps/lang/

  cp -r DEBIAN/sysfiles/etc/* package/$package_name/etc/.
  cp -r src package/$package_name/opt/riaps-pycom/.
  cp -r src/riaps/etc/riaps.conf package/$package_name/etc/riaps/.
  cp -r src/riaps/etc/riaps-log.conf package/$package_name/etc/riaps/.
  cp -r src/riaps/etc/redis.conf package/$package_name/etc/riaps/.
  cp -r src/riaps/lang/riaps.tx package/$package_name/usr/local/riaps/lang/.
  cp -r src/riaps/lang/depl.tx package/$package_name/usr/local/riaps/lang/.
  cp -r src/riaps/keys/id_rsa.key package/$package_name/etc/riaps/.
  cp -r src/riaps/keys/id_rsa.pub package/$package_name/etc/riaps/.
  cp -r src/riaps/keys/riaps-sys.cert package/$package_name/etc/riaps/.
  cp -r src/riaps/keys/x509.pem package/$package_name/etc/riaps/.

  sed s/@version@/$pycomversion/g -i package/$package_name/opt/riaps-pycom/src/setup.py
else
  cp -r DEBIAN/pkgfiles/control-dev package/$package_name/DEBIAN/control
  cp -r DEBIAN/pkgfiles/conffiles-dev package/$package_name/DEBIAN/conffiles
  cp -r DEBIAN/pkgfiles/postinst-dev package/$package_name/DEBIAN/postinst
  cp -r DEBIAN/pkgfiles/postrm-dev package/$package_name/DEBIAN/postrm
  cp -r DEBIAN/pkgfiles/prerm-dev package/$package_name/DEBIAN/prerm

  mkdir -p package/$package_name/etc/
  mkdir -p package/$package_name/etc/riaps/
  mkdir -p package/$package_name/usr/

  cp -r DEBIAN/sysfiles/usr/* package/$package_name/usr/.
  cp -r src/riaps/etc/riaps-hosts.conf package/$package_name/etc/riaps/.
  cp -r src/riaps/etc/riaps-ctrl.glade package/$package_name/etc/riaps/.
fi

sed s/@version@/$pycomversion/g -i package/$package_name/DEBIAN/control


fakeroot dpkg-deb --build package/$package_name
cp package/$package_name.deb .

