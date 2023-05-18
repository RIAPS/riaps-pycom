usage="$(basename "$0") [-a ARCH] [-d] [-h]
Create Debian packages for indicated architecture. Use -d to create a developer package (for the controller system).
Arguments are:
    -h show this help text
    -a indicate architecture for DEBIAN Package (amd64, armhf, arm64)
    -d create a developer package (optional)"

dev="false"

options='h:a:d:'
while getopt $options option; do
  case "$option" in 
    h) echo "$usage"; exit;;
    a) arch=$OPTARG;;
    d) dev="true";;
  esac
done

if [ arch == "amd64" ]; then
  arch_lib="x86_64-linux-gnu"
elif [ arch == "armhf" ]; then
  arch_lib="arm-linux-gnueabihf"
elif [ arch == "arm64" ]; then
  arch_lib="aarch64-linux-gnu"
else
  echo "Current available architectures are amd64, armhf and arm64"
  echo "$usage"
  exit 1
fi

rm -rf package
source version.sh

if [ $dev == "false" ]; then
  package_name="riaps-pycom-$arch"
else
  package_name="riaps-pycom-$arch-dev"
fi

mkdir -p package/$package_name/DEBIAN
mkdir -p package/$package_name/usr/local/bin/
mkdir -p package/$package_name/etc/
mkdir -p package/$package_name/etc/riaps/
mkdir -p package/$package_name/opt/riaps-pycom/
mkdir -p package/$package_name/usr/local/riaps/etc/
mkdir -p package/$package_name/usr/local/riaps/keys/
mkdir -p package/$package_name/usr/local/riaps/lang/

cp -r DEBIAN/pkgfiles/control package/$package_name/DEBIAN/control

if [ $dev == "false" ]; then
  cp -r DEBIAN/pkgfiles/conffiles package/$package_name/DEBIAN/conffiles
  cp -r DEBIAN/pkgfiles/postinst package/$package_name/DEBIAN/postinst
  cp -r DEBIAN/pkgfiles/postrm package/$package_name/DEBIAN/postrm
  cp -r DEBIAN/pkgfiles/prerm package/$package_name4/DEBIAN/prerm
else
  cp -r DEBIAN/pkgfiles/conffiles-dev package/$package_name/DEBIAN/conffiles
  cp -r DEBIAN/pkgfiles/postinst-dev package/$package_name/DEBIAN/postinst
  cp -r DEBIAN/pkgfiles/postrm-dev package/$package_name/DEBIAN/postrm
  cp -r DEBIAN/pkgfiles/prerm-dev package/$package_name/DEBIAN/prerm
fi

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

if [ $dev == "true" ]; then
  cp -r DEBIAN/sysfiles/usr/* package/$package_name/usr/.
  cp -r src/riaps/etc/riaps-hosts.conf package/$package_name/etc/riaps/.
  cp -r src/riaps/etc/riaps-ctrl.glade package/$package_name/etc/riaps/.
fi

sed s/@version@/$pycomversion/g -i package/$package_name/DEBIAN/control
sed s/@package@/$package_name/g -i package/$package_name/DEBIAN/control
sed s/@arch@/$arch/g -i package/$package_name/DEBIAN/control
sed s/@version@/$pycomversion/g -i package/$package_name/opt/riaps-pycom/src/setup.py
sed s/@arch-lib@/$arch_lib/g -i package/$package_name/etc/apparmor.d/usr.local.bin.riaps_actor

fakeroot dpkg-deb --build package/$package_name
cp package/$package_name.deb .

