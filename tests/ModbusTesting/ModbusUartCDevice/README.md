# RIAPS Modbus UART Device Component Library 

This library code will create two shared libraries:  
* libriapsmodbusuart.so - for use as the C++ device component 
* riapsmodbusuartpy.cpython-35m-x86_64-linux-gnu.so - to expose the device command 
interface to Python application components.  


# Required Software Installation (for compiling and use)
* Cmake 3.8 update

1. Uninstall the default version provided by Ubuntu's package manager:

'''
    $ sudo apt-get purge cmake
'''
    
2. Go to the official CMake webpage (https://cmake.org/download/), then download and extract the latest version. 
Update the version variable in the following command to the desired version:

'''
    $ version=3.10.0
    $ mkdir ~/temp
    $ cd ~/temp
    $ wget https://cmake.org/files/v3.10/cmake-$version.tar.gz
    $ tar -xzvf cmake-$version.tar.gz
    $ cd cmake-$version/
'''

3. Install the extracted source by running:

'''
    $ ./bootstrap
    $ make -j4
    $ sudo make install
'''

4. Test your new cmake version.

'''
    $ /usr/local/bin/cmake --version
        cmake version 3.10.0

        CMake suite maintained and supported by Kitware (kitware.com/cmake).
'''

* Pybind11 is used to allow an interface to be exposed between the C++ device library and 
a Python based application component.  Download and install pybind11.  This will place 
include files needed in /usr/local/include/pybind11.

''' 
    $ git clone https://github.com/pybind/pybind11.git
    $ cd pybind11
    $ mkdir build
    $ cd build
    $ cmake ..
    $ make check -j 4
    $ sudo make install
'''

* libmodbus Library
This library should be installed on the machine where the library will be built and on 
the BBBs where the library will be call from the RIAPS Modbus UART shared library.

'''
    $ git clone https://github.com/cmjones01/libmodbus.git
    $ sudo apt-get install autoconf
    $ sudo apt-get install libtool
    $ sudo apt-get install pkg-config
    $ cd libmodbus
    $ ./autogen.sh
    $ ./configure
    $ make

        libmodbus 3.1.2
        ===============
        prefix:                 /usr/local
        sysconfdir:             ${prefix}/etc
        libdir:                 ${exec_prefix}/lib
        includedir:             ${prefix}/include

    $ sudo make install

    ----------------------------------------------------------------------
    Libraries have been installed in:
        /usr/local/lib
    ----------------------------------------------------------------------
'''

Note: cmjones01 fork was used to allow option for asynchronous operation in the future 
- See https://martin-jones.com/2015/12/16/modifying-libmodbus-for-asynchronous-operation/

# Building the Shared Libraries

Original development was done using 
'''
    $ mkdir build
    $ cd build
    $ /usr/local/bin/cmake -Darch=amd64 -DPYBIND11_PYTHON_VERSION=3.5 ..
    $ make
'''

Resulting shared libraries:
* libriapsmodbusuart.so
* riapsmodbusuartpy.cpython-35m-x86_64-linux-gnu.so


