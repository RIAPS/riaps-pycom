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
        '': ['*.capnp'],
        'riaps.gen.target.cpp' : ['tpl/*'],
        'riaps.gen.target.python' : ['tpl/*'],
        'riaps.gen.target.capnp' : ['tpl/*']},
      #data_files=[('riaps/etc', ['riaps/etc/riaps.conf',  'riaps/etc/riaps-log.conf', 'riaps/etc/riaps-hosts.conf']),
      #            ('riaps/lang',['riaps/lang/riaps.tx', 'riaps/lang/depl.tx']),
      #            ('riaps/etc',['riaps/etc/redis.conf']),
      #            ('riaps/etc',['riaps/etc/riaps-ctrl.glade']),
      #            ('riaps/keys',['riaps/keys/id_rsa.key','riaps/keys/id_rsa.pub'])
      #         ],
      scripts = [
        "scripts/riaps_actor", "scripts/riaps_ctrl", "scripts/riaps_ctrl_host", "scripts/riaps_depll",
        "scripts/riaps_deplo", "scripts/riaps_device", "scripts/riaps_disco", "scripts/riaps_gen",
        "scripts/riaps_gen_cert", "scripts/riaps_gviz", "scripts/riaps_lang", "scripts/riaps_fab",
        "scripts/riaps_mn", "scripts/riaps_log_server"
     ],

     # Please see the riaps-externals/DEBIAN/<arch>/postinst file for the PIP package installations needed and RIAPS specific system file placements.
     # The <arch> is amd64 for the host VM and armhf for the beaglebones.s
     

      zip_safe=False)
