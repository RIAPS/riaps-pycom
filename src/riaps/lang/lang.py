#!/usr/bin/env python
'''
DSL for RIAPS software models
Created on Oct 9, 2016
Uses the textX parser
@author: riaps
'''

from os.path import join
from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
from textx.exceptions import TextXSemanticError, TextXSyntaxError
import textx.model

import sys
import json
import os
import argparse

class LangError(Exception):
    def __init__(self, message):
        super(LangError, self).__init__(message)

class RiapsModel2JSON(object):
    '''
    Class to convert the RIAPS model (constructed by the parser) into a data structure
    suitable for generating JSON output.Dependent on the DSL syntax and the object structure
    built by the parser.
    '''
    def __init__(self,model):
        ''' 
        Constructs the JSON structures from the model objects
        '''
        self.model = model
        self.apps = {}
        for app in model.apps:
            appObj = {}
            appObj['name'] = app.name
            appObj['messages'] = self.getMessages(app.messages)
            appObj['groups'] = self.getGroups(app.groups)
            appObj['libraries'] = self.getLibraries(app.libraries)
            appObj['devices'] = self.getIOComponents(app.components)
            appObj['components'] = self.getComponents(app.components)
            appObj['actors'] = self.getActors(app.actors)
            self.apps[app.name] = appObj
    def getMessages(self,messages):
        res = []
        for msg in messages:
            msgObj = { } 
            msgObj["name"] = msg.name
            res.append(msgObj)
        return res
    def getGroups(self,groups):
        res = []
        for group in groups:
            groupObj = { }
            groupObj["name"] = group.name
            groupObj["kind"] = group.kind.kind if group.kind else 'default'
            msgs = []
            for msg in group.messages:
                msgObj = {}
                msgObj["type"] = msg.name
                msgs.append(msgObj)
            groupObj['messages'] = msgs
            res.append(groupObj)
        return res
    def getLibraries(self,libraries):
        res = []
        for lib in libraries:
            libObj = { } 
            libObj["name"] = lib.name
            res.append(libObj)
        return res
    def getFormals(self,formals):
        res = []
        names = []
        for formal in formals:
            formalObj = { }
            argName = formal.argName
            if argName in names:
                raise TextXSemanticError('Argument name "%s" is not unique.' % 
                                         argName)
            else:
                names.append(argName)
            formalObj["name"] = argName
            if formal.argDefault != None:
                formalObj["default"] = formal.argDefault.default
            res.append(formalObj)
        return res
    def getImpl(self,comp):
        l = comp.language
        if l == None:
            return "default"
        elif l.pyImpl:
            return "py"
        elif l.cppImpl:
            return "cpp" 
    def getIOComponents(self,components):
        res = {}
        for comp in components:
            if comp.ioComponent:
                if comp.name in res:
                    raise TextXSemanticError('Component name "%s" is not unique.' % 
                                             comp.name)
                compObj = { }
                compObj["name"] = comp.name
                compObj["formals"] = self.getFormals(comp.formals)
                compObj["language"] = self.getImpl(comp)
                compObj["ports"] = self.getPorts(comp.ports)
                res[comp.name] = compObj
        return res
    def getComponents(self,components):
        res = {}
        for comp in components:
            if comp.appComponent:
                if comp.name in res:
                    raise TextXSemanticError('Component name "%s" is not unique.' % 
                                             comp.name)
                compObj = { }
                compObj["name"] = comp.name
                compObj["formals"] = self.getFormals(comp.formals)
                compObj["language"] = self.getImpl(comp)
                compObj["ports"] = self.getPorts(comp.ports)
                res[comp.name] = compObj
        return res
    def getPorts(self,ports):
        pubs = {}
        subs = {}
        clts = {}
        srvs = {}
        reqs = {}
        reps = {}
        tims = {}
        inss = {}
        qrys = {}
        anss = {}
        portNames = []
        for port in ports:
            portObj = { }
            if(port.name in portNames):
                raise TextXSemanticError('Port name "%s" is not unique' %
                                         port.name)
            else:
                portNames.append(port.name)
            portClass = port.__class__.__name__
            if (portClass == 'PubPort'):
                portObj['type'] = port.type.name
                portObj['timed'] = port.timed
                pubs[port.name] = portObj
            elif (portClass == 'SubPort'):
                portObj['type'] = port.type.name
                portObj['timed'] = port.timed
                portObj['deadline'] = port.deadline
                subs[port.name] = portObj
            elif (portClass == 'ClntPort'):
                portObj['req_type'] = port.req_type.name
                portObj['rep_type'] = port.rep_type.name
                portObj['timed'] = port.timed
                clts[port.name] = portObj
            elif (portClass == 'SrvPort'):
                portObj['req_type'] = port.req_type.name
                portObj['rep_type'] = port.rep_type.name
                portObj['timed'] = port.timed
                portObj['deadline'] = port.deadline
                srvs[port.name] = portObj
            elif (portClass == 'ReqPort'):
                portObj['req_type'] = port.req_type.name
                portObj['rep_type'] = port.rep_type.name
                portObj['timed'] = port.timed
                portObj['deadline'] = port.deadline
                reqs[port.name] = portObj
            elif(portClass == 'RepPort'):
                portObj['req_type'] = port.req_type.name
                portObj['rep_type'] = port.rep_type.name
                portObj['timed'] = port.timed
                portObj['deadline'] = port.deadline
                reps[port.name] = portObj
            elif(portClass == 'TimPort'):
                portObj['period'] = port.period
                portObj['deadline'] = port.deadline
                tims[port.name] = portObj
            elif (portClass == 'InsPort'):
                inss[port.name] = portObj
                portObj['spec'] = port.spec
            elif (portClass == 'QryPort'):
                portObj['req_type'] = port.req_type.name
                portObj['rep_type'] = port.rep_type.name
                portObj['timed'] = port.timed
                portObj['deadline'] = port.deadline
                qrys[port.name] = portObj
            elif (portClass == 'AnsPort'):
                portObj['req_type'] = port.req_type.name
                portObj['rep_type'] = port.rep_type.name
                portObj['timed'] = port.timed
                portObj['deadline'] = port.deadline
                anss[port.name] = portObj
            else:
                raise TextXSemanticError('Unknown type for port "%s"' %
                                         port.name)
        return { "subs" : subs , "pubs" : pubs,
                 "clts" : clts , "srvs" : srvs,
                 "reqs" : reqs,  "reps" : reps,
                 "tims" : tims,  "inss" : inss,
                 "qrys" : qrys,  "anss" : anss
                 }
    def getActors(self,actors):
        res = {}
        for act in actors:
            if act.name in res:
                raise TextXSemanticError('Actor name "%s" is not unique.' % 
                                         act.name)
            actObj = { } 
            actObj["formals"] = self.getFormals(act.formals)
            actObj["locals"] = self.getLocals(act.locals)
            actObj["internals"] = self.getInternals(act.internals)
            actObj["usage"] = self.getUsage(act.usage)
            actObj["instances"] = self.getInstances(act.instances)
#            actObj["wires"] = self.getWires(act.wires)
            res[act.name] = actObj
        return res
    def getLocals(self,locals_):
        res = []
        for local in locals_:
            localObj = {}
            localObj["type"] = local.name
            res.append(localObj)
        return res
    def getInternals(self,internals):
        res = []
        for internal in internals:
            internalObj = {}
            internalObj["type"] = internal.name
            res.append(internalObj)
        return res
    def getActuals(self,actuals):
        res = []
        names = []
        for actual in actuals:
            actualObj = { }
            argName = actual.argName
            if argName in names:
                raise TextXSemanticError('Argument "%s" is not unique.' % 
                                         argName)
            else:
                names.append(argName)
            actualObj["name"] = argName
            if actual.argValue.param != '':
                actualObj["param"] = actual.argValue.param
            else:
                actualObj["value"] = actual.argValue.value
            res.append(actualObj)
        return res
    @staticmethod
    def convertTime(value,unit):
        ''' Convert all time values to msec'''
        if unit == 'msec':
            return value 
        elif unit == 'sec':
            return value * 1000
        elif unit == 'min':
            return value * 60 * 1000
    @staticmethod
    def convertMem(value,unit):
        ''' Convert all memory size values to kilobytes'''
        if unit == 'mb':
            return value * 1024 
        elif unit == 'kb':
            return value
        elif unit == 'gb':
            return value * 1024 * 1024
    def convertRate(self,value,unit):
        ''' Convert all rate values to bytes/sec'''
        if unit == 'kbps':
            return int(value * 1024)
        elif unit == 'mbps':
            return int(value * 1024 * 1024)
        else:
            return None;
    def getUsage(self,usage):
        cpuUsage = { }
        memUsage = { }
        spcUsage = { }
        netUsage = { }
        for use in usage:
            useClass = use.__class__.__name__
            if (useClass == 'CPUUsage'):
                cpuUsage['use'] = use.usage
                cpuUsage['max'] = use.max
                unit = 'sec' if use.unit == None else use.unit 
                cpuUsage['interval'] = self.convertTime(use.interval,unit)
            elif (useClass == 'MemUsage'):
                unit = 'MB' if use.unit == None else use.unit
                memUsage['use'] = self.convertMem(use.usage,unit)
            elif (useClass == 'SpaceUsage'):
                unit = 'MB' if use.unit == None else use.unit
                spcUsage['use'] = self.convertMem(use.usage,unit)
            elif (useClass == 'NetUsage'):
                netUsage['rate'] = self.convertRate(use.rate,use.rateUnit)
                netUsage['ceil'] = 0 if use.ceil == None else self.convertRate(use.ceil,use.ceilUnit)
                netUsage['burst'] = 0 if use.burst == None else int(use.burst * 1024)
            else:
                raise TextXSemanticError('Unknown usage for port "%s"' %
                                         (str(use)))
        return { "cpu" : cpuUsage , "mem" : memUsage, 
                "spc" : spcUsage , "net" : netUsage
                }
    def getInstances(self,instances):
        res = { } 
        for inst in instances:
            if inst.name in res:
                raise TextXSemanticError('Instance name "%s" is not unique.' % 
                                         inst.name)
            instObj = { "type" : inst.type.name,
                       }
            instObj["actuals"] = self.getActuals(inst.actuals)
            res[inst.name] = instObj
        return res
#     def getWires(self,wires):
#         res = []
#         for wire in wires:
#             wireObj = { "lhsName" : wire.lhsInst.name,
#                         "lhsPort" : wire.lhsPort.name,
#                         "rhsName" : wire.rhsInst.name,
#                         "rhsPort" : wire.rhsPort.name,
#                         }
#             res.append(wireObj)
#         return res

# Object processor for timer ports: the 'spec' part is optional. If missing, it means period=0, i.e. a one-shot timer
def timport_obj_processor(timport):
    if timport.spec == 0:
        timport.period = 0
    else:
        spec = timport.spec
        unit = 'msec' if timport.periodUnit == None else timport.periodUnit 
        timport.period = RiapsModel2JSON.convertTime(spec,unit)
    if timport.deadline != 0:
        spec = timport.deadline
        unit = 'msec' if timport.unit == None else timport.unit
        timport.deadline = RiapsModel2JSON.convertTime(spec,unit)

# Object processor for inside  ports: the 'spec' part is optional. If missing it implies the default 1sec trigger
def insport_obj_processor(insport):
    if insport.spec == True :
        insport.spec = 'default'
    else:
        insport.spec = None

# Object processor for non-operation ports: the 'timed' flag is optional. 
def timed_port_obj_processor(port):
    if port.timed == 'timed':
        port.timed = True
    else:
        port.timed = False

# Object processor for operation ports: the 'timed' and deadline are optional. 
def op_port_obj_processor(port):
    if port.timed == 'timed':
        port.timed = True
    else:
        port.timed = False
    if port.deadline != 0:
        spec = port.deadline
        unit = 'msec' if port.unit == None else port.unit
        port.deadline = RiapsModel2JSON.convertTime(spec,unit)

# Object processor for io component instances: messages must be local
def instance_obj_processor(instance):
    component = instance.type
    if component.ioComponent:
        localMessages = instance.parent.locals
        localMessageNames = [localMessage.name for localMessage in localMessages]
        portMessageNames = []
        for port in component.ports:
            if hasattr(port, 'type'):
                portMessageNames.append(port.type.name)
            elif hasattr(port,'req_type'):
                portMessageNames.append(port.req_type.name)
            elif hasattr(port,'rep_type'):
                portMessageNames.append(port.rep_type.name)
            else:
                pass
        for portMessageName in portMessageNames:
            if portMessageName not in localMessageNames:
                raise TextXSemanticError('Non-local message type %s for IO component %s:%s' 
                                         % (portMessageName,instance.name,component.name))
    else:
        pass

# # Object processor for wires: checks if the names used are correct. 
# # Wires are to connect ports of local instances.
# def wire_obj_processor(wire):
# #    print '(' + wire.lhsName + '.' + wire.lhsPortName + '=' + wire.rhsName + '.' + wire.rhsPortName + ')'
#     instances = wire.parent.instances
#     lhsInst = [inst for inst in instances if inst.name == wire.lhsName]
#     if not lhsInst:
#         raise TextXSemanticError('Wire LHS instance "%s" not found.' %
#                                  wire.lhsName)
#     else:
#         wire.lhsInst = lhsInst[0]
#     lhsPort = [port for port in wire.lhsInst.type.ports if port.name == wire.lhsPortName]
#     if not lhsPort:
#         raise TextXSemanticError('Wire LHS port "%s" in instance "%s" not found.' %
#                                  (wire.lhsPortName, wire.lhsName))
#     else:
#         wire.lhsPort=lhsPort[0]
#     rhsInst = [inst for inst in instances if inst.name == wire.rhsName]
#     if not rhsInst:
#         raise TextXSemanticError('Wire RHS instance "%s" not found.' %
#                                  wire.rhsName)
#     else:
#         wire.rhsInst=rhsInst[0]
#     rhsPort = [port for port in wire.rhsInst.type.ports if port.name == wire.rhsPortName]
#     if not rhsPort:
#         raise TextXSemanticError('Wire RHS port "%s" in instance "%s" not found.' %
#                                  (wire.rhsPortName, wire.rhsName))
#     else:
#         wire.rhsPort=rhsPort[0]
# #    print lhsInst, lhsPort, rhsInst, rhsPort
           
def compileModel(modelFileName,verbose=False,debug=False,generate=True):
    riaps_folder = os.getenv('RIAPSHOME', './') # RIAPSHOME points to the folder containing the grammar
    this_folder = os.getcwd()  
    
    # Get meta-model from language grammar
    riaps_meta = metamodel_from_file(join(riaps_folder, 'lang/riaps.tx'),
                                     debug=debug)       
    
    # Register object processors for wires and timer ports
    obj_processors = {
#         'Wire': wire_obj_processor,
        'TimPort': timport_obj_processor,
         # 'InsPort': op_port_obj_processor, # Inside port cannot be timed / have deadline
        'Instance': instance_obj_processor,
        'PubPort' : timed_port_obj_processor,
        'SubPort' : op_port_obj_processor,
        'ClntPort': timed_port_obj_processor,
        'SrvPort' : op_port_obj_processor,
        'ReqPort' : op_port_obj_processor,
        'RepPort' : op_port_obj_processor,
        'QryPort' : op_port_obj_processor,
        'AnsPort' : op_port_obj_processor,
        # We should also check for parameters: 
        #   (1) formal/actual lists should match, 
        #   (2) inherited parameters should appear in their parent 
        }
    riaps_meta.register_obj_processors(obj_processors)
    
    # Optionally export meta-model to dot (for debugging only)
    # metamodel_export(riaps_meta, join(this_folder, 'riaps_meta.dot'))
    
    try:
        # Instantiate the model object structure from the model file 
        example_riaps_model = riaps_meta.model_from_file(join(this_folder,modelFileName))
    except IOError as e:
        errMsg = "I/O error({0}): {1}".format(e.errno, e.strerror)
        if verbose: print (errMsg)
        raise LangError(errMsg)
    except TextXSyntaxError as e:
        errMsg = "Syntax error: %s" % e.args
        if verbose: print (errMsg)
        raise LangError(errMsg)
    except TextXSemanticError as e:
        errMsg = "Semantic error: %s" % e.args
        if verbose: print (errMsg)
        raise LangError(errMsg)
    except Exception as e: 
        errMsg = "Unexpected error %s:%s" % (sys.exc_info()[0],e.args())
        if verbose: print (errMsg)
        raise LangError(errMsg)
    
    # Optionally export model to dot
    # model_export(example_riaps_model, join(this_folder, 'sample.dot'))

    # Convert model object structure into JSON data
    riaps_model = RiapsModel2JSON(example_riaps_model)
    riaps_model_json = { }
    
    # Optionally print generated JSON on console
    if verbose:
        riaps_model_json = json.dumps(riaps_model.apps,indent=2,
                                      separators=(',', ':'))
        print(riaps_model_json)
    
    # Generated JSON files for each app    
    if generate:
        for appName in riaps_model.apps:
            fp = open(appName + '.json','w')
            appObj = riaps_model.apps[appName]
            json.dump(appObj,fp,indent=4,sort_keys=True,separators=(',', ':'))
            fp.close()
        
    return riaps_model.apps
    
def main(debug=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model file")
    parser.add_argument("-v","--verbose", help="print JSON on console", action="store_true")
    args = parser.parse_args()
    return compileModel(args.model,args.verbose)

if __name__ == '__main__':
    m = main()
#   print (m)
    