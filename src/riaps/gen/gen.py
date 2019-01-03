import sys
import os
import argparse
import shutil
import json
from riaps.gen.target.cpp import cppgen, sync_cpp
from riaps.gen.target.python import pygen, sync_python
from riaps.gen.target.capnp import capnpgen, sync_capnp

from multigen.jinja import JinjaTask, JinjaGenerator

def preprocess(model):
    items={
        "appname"  : model['name'],
        "py"       : [],
        "cpp"      : [],
        "messages" : [m['name'] for m in model['messages']]
    }

    cppspec = ['c++', 'cpp', 'C++']

    for part in ['components', 'devices']:
        for comp_name, comp_params in model[part].items():
            newitem = comp_params
            newitem['is_device'] = (part == 'devices')
            newitem['appname'] = model['name']
            if comp_params['language'] in cppspec :
                items['cpp'].append(newitem)
            else:
                items['py'].append(newitem)
    return items


def main():
    if sys.version_info[0] < 3 or sys.version_info[0] == 3 and sys.version_info[1]<6:
        print("riaps_gen requires python3.6 or above")

    model = {}
    parser = argparse.ArgumentParser()
    output_dir = ""

    parser.add_argument("-m", "--model", help="Model file path.",required=True)
    parser.add_argument("-o", "--output", help="Output directory. Default is the directory of the model file.")
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

    # If the output dir is not specified, the output is generated into the {json file dir}/generated
    if args.output:
        output_dir = args.output
    else:
        output_dir = os.path.join(os.path.abspath(os.path.dirname(args.model)), "generated")

    if output_dir == "./" or output_dir == ".":
        output_dir =  os.path.dirname(os.path.abspath(args.model))
      
    # Backup the source to keep implementation parts
    if not args.overwrite:
        backup_dir = f"{output_dir}_bak"
        if os.path.isdir(backup_dir):
            shutil.rmtree(backup_dir)
        if os.path.isdir(output_dir):
            shutil.copytree(output_dir, backup_dir)

    if model['cpp']:
        gen = cppgen.CompGenerator()
        gen.generate(model, output_dir)
        if not args.overwrite:
            sync = sync_cpp.FileSync(model['cpp'])
            sync.sync_all(output_dir)

    if model['py']:
        gen = pygen.CompGenerator()
        gen.generate(model, output_dir)
        if not args.overwrite:
            sync = sync_python.FileSync(model['py'])
            sync.sync_code(output_dir)

    # always generate capnp
    gen = capnpgen.CapnpGenerator(model['cpp'], output_dir)
    gen.generate(model, output_dir)
    if not args.overwrite:
        sync = sync_capnp.FileSync(model)
        sync.sync_capnp(output_dir)

if __name__ == '__main__':
    main()