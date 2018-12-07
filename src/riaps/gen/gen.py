import sys
import os
import argparse
import shutil
import json
from riaps.gen.target.cpp import cppgen, sync_cpp
from riaps.gen.target.python import pygen, sync_python

from multigen.jinja import JinjaTask, JinjaGenerator

def preprocess(model):
    items = {}

    for key, value in model['components'].items():
        items[key] = value
        items[key]['is_device'] = False
        items[key]['appname'] = model['name']

    for key, value in model['devices'].items():
        items[key] = value
        items[key]['is_device'] = True
        items[key]['appname'] = model['name']


    return items


def main():
    model = {}
    parser = argparse.ArgumentParser()
    output_dir = ""

    parser.add_argument("-m", "--model", help="Model file path.",required=True)
    parser.add_argument("-o", "--output", help="Output directory. Default is the directory of the model file.")
    parser.add_argument("-l", "--lang", help="Target language.", default='c++', choices=['c++', 'python'])
    parser.add_argument("-s", "--ser", help="Message serializer to be used.", default="capnp", choices=["capnp", "pickle"])
    parser.add_argument("-w", "--overwrite", help="Overwrite the existing code.", action="store_true")
    args = parser.parse_args()

    # Load json model
    try:
        fp = open(args.model, 'r')
        model = json.load(fp)
    except IOError as e:
        print("I/O error({0}): {1} {2}".format(e.errno, e.strerror, e.filename))
        os._exit(1)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        os._exit(1)

    model = preprocess(model)

    # C++ with pickle is not implemented
    if args.lang == "c++" and args.ser == "pickle":
        print("Error: C++ pickle marshalling is not implemented, please choose python to use pickle or switch to capnp serialization.")
        os._exit(1)

    # If the output dir is not specified, the output is generated into the {json file dir}/generated
    if args.output:
        output_dir = args.output
    else:
        output_dir = os.path.join(os.path.abspath(os.path.dirname(args.model)), "generated")

    # Backup the source to keep implementation parts
    if not args.overwrite:
        backup_dir = f"{output_dir}_bak"
        if os.path.isdir(backup_dir):
            shutil.rmtree(backup_dir)
        if os.path.isdir(output_dir):
            shutil.copytree(output_dir, backup_dir)

    if args.lang == 'c++':
        gen = cppgen.CompGenerator()
        gen.generate(model, output_dir)
        # sync the generated code with the previous implementations
        if not args.overwrite:
            sync = sync_cpp.FileSync(model)
            sync.sync_all(output_dir)
    elif args.lang == 'python':
        gen = pygen.CompGenerator(args.ser == "capnp")
        gen.generate(model, output_dir)
        if not args.overwrite:
            sync = sync_python.FileSync(model)
            sync.sync_code(output_dir)

if __name__ == '__main__':
    main()