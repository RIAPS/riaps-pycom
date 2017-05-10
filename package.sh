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





