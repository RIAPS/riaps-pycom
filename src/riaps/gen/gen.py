import sys
import os
import argparse
import shutil
import json
from riaps.gen.target.cpp import cppgen, sync_cpp
from riaps.gen.target.python import pygen, sync_python

from multigen.jinja import JinjaTask, JinjaGenerator

def preprocess(model, cppcomponents, pycomponents):
    items={
        "py"       : [],
        "cpp"      : [],
        #"messages" : model['messages']
    }

    for part in ['components', 'devices']:
        for comp_name, comp_params in model[part].items():
            newitem = comp_params
            newitem['is_device'] = (part == 'devices')
            newitem['appname'] = model['name']
            if cppcomponents!=None and comp_name in cppcomponents:
                items['cpp'].append(newitem)
            elif pycomponents!=None and comp_name in pycomponents:
                items['py'].append(newitem)
            else:
                print("Language not specified for component: ".format(comp_name))
                os._exit(1)



    # for cppcomponent in cppcomponents:
    #     part = 'components'
    #     if cppcomponent in model['components']:
    #         items[cppcomponent] = model[part][cppcomponent]
    #     elif cppcomponent in model['devices']:
    #         items[cppcomponent] = model['devices'][cppcomponent]


    return items


def main():
    model = {}
    parser = argparse.ArgumentParser()
    output_dir = ""

    parser.add_argument("-m", "--model", help="Model file path.",required=True)
    parser.add_argument("-o", "--output", help="Output directory. Default is the directory of the model file.")
    #parser.add_argument("-l", "--lang", help="Target language.", default='c++', choices=['c++', 'python'])
    parser.add_argument("-cpp", "--cpp", help="List of components, where the target language is c++", nargs="*")
    parser.add_argument("-py", "--python", help="List of components, where the target language is python", nargs="*")
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

    cppcomponents = args.cpp
    pycomponents  = args.python

    model = preprocess(model, cppcomponents, pycomponents)

    # C++ with pickle is not implemented
    if cppcomponents and args.ser == "pickle":
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

    if cppcomponents:
        gen = cppgen.CompGenerator()
        gen.generate(model['cpp'], output_dir)
        # sync the generated code with the previous implementations
        #if not args.overwrite:
        #    sync = sync_cpp.FileSync(model)
        #    sync.sync_all(output_dir)
    elif pycomponents:
        gen = pygen.CompGenerator(args.ser == "capnp")
        gen.generate(model['py'], output_dir)
        #if not args.overwrite:
        #    sync = sync_python.FileSync(model)
        #    sync.sync_code(output_dir)

if __name__ == '__main__':
    main()