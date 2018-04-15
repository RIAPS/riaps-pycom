'''
Deployment language processor
Created on Nov 7, 2016

@author: riaps
'''

from os.path import join
from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
from textx.exceptions import TextXSemanticError

import sys
import os
import argparse
import json

class DeplError(Exception):
    def __init__(self, message):
        super(DeplError, self).__init__(message)

class DeploymentModel(object):
    '''
    Deployment model loader/parser
    '''
    def __init__(self,fileName,debug=False,verbose=False):
        riaps_folder = os.getenv('RIAPSHOME', './') # RIAPSHOME points to the folder containing the grammar
        this_folder = os.getcwd()  
        # Get meta-model from language grammar
        depl_meta = metamodel_from_file(join(riaps_folder, 'lang/depl.tx'),
                                         debug=debug)       
        # Register object processors for wires and timer ports
#       depl_meta.register_obj_processors(obj_processors)
    
        # Optionally export meta-model to dot (for debugging only)
        # metamodel_export(depl_meta, join(this_folder, 'depl_meta.dot'))
        
        if fileName.endswith('.json'):
            # TODO: Validate that this is a correct deployment file
            fp = open(join(this_folder,fileName),'r')             # Load json file (one app)
            jsonModel = json.load(fp)
            self.appName = list(jsonModel.keys())[0]
            self.deployments = jsonModel[self.appName]
            fp.close()
        else:
            try:
                # Instantiate the model object structure from the model file 
                depl_model = depl_meta.model_from_file(join(this_folder, fileName))
            except IOError as e:
                errMsg = "I/O error({0}): {1}".format(e.errno, e.strerror)
                if verbose: print(errMsg)
                raise e
            except: 
                print ("Unexpected error:", sys.exc_info()[0])
                raise e
            # Optionally export model to dot
            # model_export(depl_model, join(this_folder, 'sample.dot'))
        
            self.appName = depl_model.name
            self.deployments = []
            for dep in depl_model.actorDeployments:
                loc = dep.location
                target = []
                if loc.all:
                    pass
                else:
                    for host in loc.hosts:
                        target.append(host.name)
                actors = []
                for act in dep.actors:
                    actObj = { }
                    actObj["name"] = act.name
                    actObj["actuals"] = self.getActuals(act.actuals)
                    actors.append(actObj)
                self.deployments.append({"target" : target,
                                         "actors" : actors})
        
            
    def getActuals(self,actuals):
        res = []
        for actual in actuals:
            actualObj = { }
            actualObj["name"] = actual.argName
            actualObj["value"] = actual.argValue.value
            res.append(actualObj)
        return res
    
    def getAppName(self):
        return self.appName
    
    def getDeployments(self):
        return self.deployments
        
def main(debug=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model file name")       # Model file argument
    parser.add_argument("-v","--verbose", help="print JSON on console", action="store_true")
    parser.add_argument("-g","--generate", help="generate JSON file", action="store_true")
    args = parser.parse_args()
    try:
        deplo = DeploymentModel(args.model,args.verbose)
    except Exception as e: 
        errMsg = "Unexpected error %s: %s" % (sys.exc_info()[0],e.args())
        print (errMsg)
        raise DeplError(errMsg)
    if args.verbose:
        print (deplo.deployments)
    # Generated JSON files for each app    
    if args.generate:
        appName = deplo.getAppName()
        deploys = deplo.getDeployments()
        deploObj = {}
        deploObj[appName] = deploys
        fp = open(appName + '-deplo.json','w')
        json.dump(deploObj,fp,indent=4,sort_keys=True,separators=(',', ':'))
        fp.close()
        
if __name__ == '__main__':
    m = main()

