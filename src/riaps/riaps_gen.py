#!/usr/bin/python3
'''
Top-level script to start the language processor ('lang') for app models
Created on Nov 15, 2018

Arguments:
  -m,   --model        : Full path of the model.json.
  -o,   --output       : Output directory. Default is the directory of the model file.
  -cpp, --cpp          : List of components to be generated in C++.
  -py,  --python       : List of components to be generated in Python.
  -s,   --ser          : Message serializer ('capnp' or 'pickle').
  -w,   --overwrite    : Overwrite existing code (no sync).

@author: riaps
'''
from riaps.gen.gen import main

if __name__ == '__main__':
    main()