rm -rf package
source version.sh
mkdir -p package/riaps-pycom-amd64/DEBIAN
mkdir -p package/riaps-pycom-amd64/etc/
mkdir -p package/riaps-pycom-amd64/etc/riaps/
mkdir -p package/riaps-pycom-amd64/opt/riaps-pycom/
mkdir -p package/riaps-pycom-amd64/usr/local/riaps/etc/
mkdir -p package/riaps-pycom-amd64/usr/local/riaps/lang/

cp -r DEBIAN/amd64/pkgfiles/* package/riaps-pycom-amd64/DEBIAN/.
cp -r DEBIAN/amd64/etc/* package/riaps-pycom-amd64/etc/.
cp -r src package/riaps-pycom-amd64/opt/riaps-pycom/.
cp -r src/riaps/etc/riaps.conf package/riaps-pycom-amd64/etc/riaps/.
cp -r src/riaps/etc/riaps-log.conf package/riaps-pycom-amd64/etc/riaps/.
cp -r src/riaps/etc/riaps-hosts.conf package/riaps-pycom-amd64/etc/riaps/.
cp -r src/riaps/etc/redis.conf package/riaps-pycom-amd64/usr/local/riaps/etc/.
cp -r src/riaps/etc/riaps-ctrl.glade package/riaps-pycom-amd64/usr/local/riaps/etc/.
cp -r src/riaps/lang/riaps.tx package/riaps-pycom-amd64/usr/local/riaps/lang/.
cp -r src/riaps/lang/depl.tx package/riaps-pycom-amd64/usr/local/riaps/lang/.
cp -r src/riaps/keys/id_rsa.key package/riaps-pycom-amd64/etc/riaps/.
cp -r src/riaps/keys/id_rsa.pub package/riaps-pycom-amd64/etc/riaps/.
cp -r src/riaps/keys/riaps-sys.cert package/riaps-pycom-amd64/etc/riaps/.
cp -r src/riaps/keys/x509.pem package/riaps-pycom-amd64/etc/riaps/.

sed s/@version@/$pycomversion/g -i package/riaps-pycom-amd64/DEBIAN/control
sed s/@version@/$pycomversion/g -i package/riaps-pycom-amd64/opt/riaps-pycom/src/setup.py
fakeroot dpkg-deb --build package/riaps-pycom-amd64

cp package/riaps-pycom-amd64.deb .

source version.sh
mkdir -p package/riaps-pycom-armhf/DEBIAN
mkdir -p package/riaps-pycom-armhf/etc/
mkdir -p package/riaps-pycom-armhf/etc/riaps/
mkdir -p package/riaps-pycom-armhf/opt/riaps-pycom/
mkdir -p package/riaps-pycom-armhf/usr/bin/
mkdir -p package/riaps-pycom-armhf/usr/local/riaps/etc/
mkdir -p package/riaps-pycom-armhf/usr/local/riaps/lang/

cp -r DEBIAN/armhf/pkgfiles/* package/riaps-pycom-armhf/DEBIAN/.
cp -r DEBIAN/armhf/etc/* package/riaps-pycom-armhf/etc/.
cp -r DEBIAN/armhf/usr/bin/* package/riaps-pycom-armhf/usr/bin/.
cp -r src package/riaps-pycom-armhf/opt/riaps-pycom/.
cp -r src/riaps/etc/riaps.conf package/riaps-pycom-armhf/etc/riaps/.
cp -r src/riaps/etc/riaps-log.conf package/riaps-pycom-armhf/etc/riaps/.
cp -r src/riaps/etc/redis.conf package/riaps-pycom-armhf/usr/local/riaps/etc/.
cp -r src/riaps/lang/riaps.tx package/riaps-pycom-armhf/usr/local/riaps/lang/.
cp -r src/riaps/lang/depl.tx package/riaps-pycom-armhf/usr/local/riaps/lang/.
cp -r src/riaps/keys/id_rsa.key package/riaps-pycom-armhf/etc/riaps/.
cp -r src/riaps/keys/id_rsa.pub package/riaps-pycom-armhf/etc/riaps/.
cp -r src/riaps/keys/riaps-sys.cert package/riaps-pycom-armhf/etc/riaps/.
cp -r src/riaps/keys/x509.pem package/riaps-pycom-armhf/etc/riaps/.

sed s/@version@/$pycomversion/g -i package/riaps-pycom-armhf/DEBIAN/control
sed s/@version@/$pycomversion/g -i package/riaps-pycom-armhf/opt/riaps-pycom/src/setup.py
fakeroot dpkg-deb --build package/riaps-pycom-armhf

cp package/riaps-pycom-armhf.deb .

source version.sh
mkdir -p package/riaps-pycom-aarch64/DEBIAN
mkdir -p package/riaps-pycom-aarch64/etc/
mkdir -p package/riaps-pycom-aarch64/etc/riaps/
mkdir -p package/riaps-pycom-aarch64/opt/riaps-pycom/
mkdir -p package/riaps-pycom-aarch64/usr/bin/
mkdir -p package/riaps-pycom-aarch64/usr/local/riaps/etc/
mkdir -p package/riaps-pycom-aarch64/usr/local/riaps/lang/

cp -r DEBIAN/aarch64/pkgfiles/* package/riaps-pycom-aarch64/DEBIAN/.
cp -r DEBIAN/aarch64/etc/* package/riaps-pycom-aarch64/etc/.
cp -r DEBIAN/aarch64/usr/bin/* package/riaps-pycom-aarch64/usr/bin/.
cp -r src package/riaps-pycom-aarch64/opt/riaps-pycom/.
cp -r src/riaps/etc/riaps.conf package/riaps-pycom-aarch64/etc/riaps/.
cp -r src/riaps/etc/riaps-log.conf package/riaps-pycom-aarch64/etc/riaps/.
cp -r src/riaps/etc/riaps-hosts.conf package/riaps-pycom-aarch64/etc/riaps/.
cp -r src/riaps/etc/redis.conf package/riaps-pycom-aarch64/usr/local/riaps/etc/.
cp -r src/riaps/etc/riaps-ctrl.glade package/riaps-pycom-aarch64/usr/local/riaps/etc/.
cp -r src/riaps/lang/riaps.tx package/riaps-pycom-aarch64/usr/local/riaps/lang/.
cp -r src/riaps/lang/depl.tx package/riaps-pycom-aarch64/usr/local/riaps/lang/.
cp -r src/riaps/keys/id_rsa.key package/riaps-pycom-aarch64/etc/riaps/.
cp -r src/riaps/keys/id_rsa.pub package/riaps-pycom-aarch64/etc/riaps/.
cp -r src/riaps/keys/riaps-sys.cert package/riaps-pycom-aarch64/etc/riaps/.
cp -r src/riaps/keys/x509.pem package/riaps-pycom-aarch64/etc/riaps/.

sed s/@version@/$pycomversion/g -i package/riaps-pycom-aarch64/DEBIAN/control
sed s/@version@/$pycomversion/g -i package/riaps-pycom-aarch64/opt/riaps-pycom/src/setup.py
fakeroot dpkg-deb --build package/riaps-pycom-aarch64

cp package/riaps-pycom-aarch64.deb .
