'''
Deployment language processor
Created on Nov 7, 2016

@author: riaps
'''

from os.path import join
from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
from textx.exceptions import TextXError

import sys
import os
import argparse
import json
import pprint

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
            self.deployments = jsonModel[self.appName]['deployments']
            try:
                self.network = jsonModel[self.appName]['network']
            except:
                self.network = { }              # Should raise an error      
            fp.close()
        else:
            errMsg = None
            try:
                # Instantiate the model object structure from the model file 
                depl_model = depl_meta.model_from_file(join(this_folder, fileName))
            except IOError as e:
                errMsg = "I/O error({0}): {1}".format(e.errno, e.strerror)
            except TextXError as e:
                errMsg = 'TextX error: %s' % e.message
            except Exception as e: 
                errMsg = "Unexpected error:" % sys.exc_info()[1]
            if errMsg:
                if verbose: print(errMsg)
                raise DeplError(errMsg)
    
            # Optionally export model to dot
            # model_export(depl_model, join(this_folder, 'sample.dot'))
        
            self.appName = depl_model.name
            self.network = { }
            for hostDeployment in depl_model.hostDeployments:
                hostName = '[]' if hostDeployment.all else hostDeployment.host.name
                hostNet = hostDeployment.hostNet
                network = []
                if hostNet.any:
                    pass
                else:
                    for host_DNS in hostNet.access:
                        network.append('dns' if host_DNS.dns else host_DNS.host.name)
                self.network[hostName] = network
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
                                         "actors" : actors
                                         })
        
            
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
        
    def getNetwork(self):
        return self.network
        
def main(standalone=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model file name")       # Model file argument
    parser.add_argument("-v","--verbose", help="print JSON on console", action="store_true")
    parser.add_argument("-g","--generate", help="generate JSON file", action="store_true")
    args = parser.parse_args()
    try:
        deplo = DeploymentModel(args.model,debug=False,verbose=args.verbose)
    except Exception as e: 
        if standalone:
            return 
        else:
            raise e 
    if args.verbose:
        pprint.pprint (deplo.deployments,width=1)
        pprint.pprint (deplo.network,width=1)
    # Generated JSON files for each app    
    if args.generate:
        appName = deplo.getAppName()
        deploys = deplo.getDeployments()
        network = deplo.getNetwork()
        deploObj = {}
        deploObj[appName] = { }
        deploObj[appName]['deployment'] = deploys
        deploObj[appName]['network'] = network 
        fp = open(appName + '-deplo.json','w')
        json.dump(deploObj,fp,indent=4,sort_keys=True,separators=(',', ':'))
        fp.close()
        
# if __name__ == '__main__':
#     m = main()

