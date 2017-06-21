from setuptools import setup, find_packages

setup(name='riaps-pycom',
      version='@version@',
      description='python implementation of riaps component model',
      url='',
      author='riaps',
      author_email='riaps@vanderbilt.com',
      license='',
      packages=find_packages(),
      package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.capnp']},      
      data_files=[('riaps/etc', ['riaps/etc/riaps.conf',  'riaps/etc/riaps-log.conf']),
                  ('riaps/lang',['riaps/lang/riaps.tx', 'riaps/lang/depl.tx']),
                  ('riaps/etc',['riaps/etc/redis.conf']),
                  ('riaps/etc',['riaps/etc/riaps-ctrl.glade']),
                  ('riaps/keys',['riaps/keys/id_rsa.key','riaps/keys/id_rsa.pub'])
               ],
      scripts = [
        "scripts/riaps_actor", "scripts/riaps_ctrl", "scripts/riaps_deplo", "scripts/riaps_disco", "scripts/riaps_lang", "scripts/riaps_depll", "scripts/riaps_device", "scripts/riaps_devm"

     ],
     
     # These packages will be installed as part of the deb package for riaps-pycom.  Some of these packages are not installed on the armhf architecture.
     # The deb package has specific instructions for amd64 and armhf. If you are installing this without using the deb package, be aware that more may be installed than necessary.  Also be
     # aware that these requirements will change over time and are not being updated here (it is duplication).
     # install_requires=['rpyc>=3.3.1','textX == 1.5.1','redis >= 2.10.5','hiredis >= 0.2.0','pyzmq >= 16','pycapnp >= 0.5.9','netifaces >= 0.10.5','paramiko >= 2.0.2','cryptography >= 1.5.3', 'Adafruit_BBIO >= 1.0.3'],
     # dependency_links=["git+https://github.com/adubey14/rpyc#egg=rpyc-3.3.1"],
     
      zip_safe=False)

 

