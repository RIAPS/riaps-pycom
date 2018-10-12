      #data_files=[('riaps/etc', ['riaps/etc/riaps.conf',  'riaps/etc/riaps-log.conf']),
      #            ('riaps/lang',['riaps/lang/riaps.tx', 'riaps/lang/depl.tx']),
      #            ('riaps/etc',['riaps/etc/redis.conf']),
      #            ('riaps/etc',['riaps/etc/riaps-ctrl.glade']),
      #            ('riaps/keys',['riaps/keys/id_rsa.key','riaps/keys/id_rsa.pub'])
      #         ],

rm -rf package
source version.sh
mkdir -p package/riaps-pycom-amd64/DEBIAN
mkdir -p package/riaps-pycom-amd64/etc/
mkdir -p package/riaps-pycom-amd64/opt/riaps-pycom/
mkdir -p package/riaps-pycom-amd64/usr/local/riaps/etc/
mkdir -p package/riaps-pycom-amd64/usr/local/riaps/lang/
mkdir -p package/riaps-pycom-amd64/usr/local/riaps/keys/

cp -r DEBIAN/amd64/* package/riaps-pycom-amd64/DEBIAN/.
cp -r src package/riaps-pycom-amd64/opt/riaps-pycom/.
cp -r src/riaps/etc/riaps.conf package/riaps-pycom-amd64/etc/.
cp -r src/riaps/etc/riaps-log.conf package/riaps-pycom-amd64/etc/.
cp -r src/riaps/etc/redis.conf package/riaps-pycom-amd64/usr/local/riaps/etc/.
cp -r src/riaps/etc/riaps-ctrl.glade package/riaps-pycom-amd64/usr/local/riaps/etc/.
cp -r src/riaps/lang/riaps.tx package/riaps-pycom-amd64/usr/local/riaps/lang/.
cp -r src/riaps/lang/depl.tx package/riaps-pycom-amd64/usr/local/riaps/lang/.

cp -r src/riaps/keys/id_rsa.key package/riaps-pycom-amd64/usr/local/riaps/keys/.
cp -r src/riaps/keys/id_rsa.pub package/riaps-pycom-amd64/usr/local/riaps/keys/.

sed s/@version@/$pycomversion/g -i package/riaps-pycom-amd64/DEBIAN/control
sed s/@version@/$pycomversion/g -i package/riaps-pycom-amd64/opt/riaps-pycom/src/setup.py
fakeroot dpkg-deb --build package/riaps-pycom-amd64

cp package/riaps-pycom-amd64.deb .

source version.sh
mkdir -p package/riaps-pycom-armhf/DEBIAN
mkdir -p package/riaps-pycom-armhf/etc/
mkdir -p package/riaps-pycom-armhf/opt/riaps-pycom/
mkdir -p package/riaps-pycom-armhf/opt/riaps-pycom/
mkdir -p package/riaps-pycom-armhf/usr/local/riaps/etc/
mkdir -p package/riaps-pycom-armhf/usr/local/riaps/lang/
mkdir -p package/riaps-pycom-armhf/usr/local/riaps/keys/

cp -r DEBIAN/armhf/* package/riaps-pycom-armhf/DEBIAN/.
cp -r src package/riaps-pycom-armhf/opt/riaps-pycom/.
cp -r src/riaps/etc/riaps.conf package/riaps-pycom-armhf/etc/.
cp -r src/riaps/etc/riaps-log.conf package/riaps-pycom-armhf/etc/.
cp -r src/riaps/etc/redis.conf package/riaps-pycom-armhf/usr/local/riaps/etc/.
cp -r src/riaps/etc/riaps-ctrl.glade package/riaps-pycom-armhf/usr/local/riaps/etc/.
cp -r src/riaps/lang/riaps.tx package/riaps-pycom-armhf/usr/local/riaps/lang/.
cp -r src/riaps/lang/depl.tx package/riaps-pycom-armhf/usr/local/riaps/lang/.

cp -r src/riaps/keys/id_rsa.key package/riaps-pycom-armhf/usr/local/riaps/keys/.
cp -r src/riaps/keys/id_rsa.pub package/riaps-pycom-armhf/usr/local/riaps/keys/.

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
