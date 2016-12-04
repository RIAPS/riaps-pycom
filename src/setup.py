from setuptools import setup, find_packages

setup(name='riaps',
      version='0.1',
      description='python implementation of riaps component model',
      url='',
      author='riaps',
      author_email='riaps@vanderbilt.com',
      license='',
      packages=find_packages(),
      install_requires=['rpyc>=3.4', 'netifaces', 'textX >= 1.4','redis >= 2.10.5','hiredis >= 0.2.0','pyzmq >= 16','pycapnp >= 0.5.9','netifaces >= 0.10.5','paramiko >= 2.0.2','cryptography >= 1.5.3'],
dependency_links=[
        "git+https://github.com/tomerfiliba/rpyc#egg=rpyc-3.4"
    ],
      zip_safe=False)
