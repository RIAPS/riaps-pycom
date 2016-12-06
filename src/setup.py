from setuptools import setup, find_packages

setup(name='riaps',
      version='0.1',
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
                  ('riaps/etc',['riaps/dbase/redis.conf']),
                  ('riaps/etc',['riaps/ctrl/riaps-ctrl.glade']),
                  ('riaps/keys',['keys/id_rsa.key','keys/id_rsa.pub'])
               ],
      scripts = [
        'scripts/riaps_actor',"scripts/riaps_ctrl","scripts/riaps_deplo", "scripts/riaps_disco","scripts/riaps_lang"

     ],
      install_requires=['rpyc>=3.4', 'netifaces', 'textX >= 1.4','redis >= 2.10.5','hiredis >= 0.2.0','pyzmq >= 16','pycapnp >= 0.5.9','netifaces >= 0.10.5','paramiko >= 2.0.2','cryptography >= 1.5.3'],
dependency_links=[
        "git+https://github.com/tomerfiliba/rpyc#egg=rpyc-3.4"
    ],
      zip_safe=False)
