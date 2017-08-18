rm -rf package
source version.sh
mkdir -p package/riaps-pycom-amd64/DEBIAN
mkdir -p package/riaps-pycom-amd64/opt/riaps-pycom/
cp -r DEBIAN/amd64/* package/riaps-pycom-amd64/DEBIAN/.
cp -r src package/riaps-pycom-amd64/opt/riaps-pycom/.
sed s/@version@/$pycomversion/g -i package/riaps-pycom-amd64/DEBIAN/control
sed s/@version@/$pycomversion/g -i package/riaps-pycom-amd64/opt/riaps-pycom/src/setup.py
fakeroot dpkg-deb --build package/riaps-pycom-amd64

cp package/riaps-pycom-amd64.deb .

source version.sh
mkdir -p package/riaps-pycom-armhf/DEBIAN
mkdir -p package/riaps-pycom-armhf/opt/riaps-pycom/
cp -r DEBIAN/armhf/* package/riaps-pycom-armhf/DEBIAN/.
cp -r src package/riaps-pycom-armhf/opt/riaps-pycom/.
sed s/@version@/$pycomversion/g -i package/riaps-pycom-armhf/DEBIAN/control
sed s/@version@/$pycomversion/g -i package/riaps-pycom-armhf/opt/riaps-pycom/src/setup.py
fakeroot dpkg-deb --build package/riaps-pycom-armhf

cp package/riaps-pycom-armhf.deb .


# services
cp -r services package/.
sed s/@version@/$pycomversion/g -i package/services/amd64/DEBIAN/control
sed s/@version@/$pycomversion/g -i package/services/armhf/DEBIAN/control
fakeroot dpkg-deb --build package/services/amd64
fakeroot dpkg-deb --build package/services/armhf
mv package/services/amd64.deb riaps-systemd-amd64.deb
mv package/services/armhf.deb riaps-systemd-armhf.deb



