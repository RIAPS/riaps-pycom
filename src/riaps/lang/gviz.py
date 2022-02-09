'''
Created on Mar 17, 2018

@author: riaps
'''

from riaps.lang.lang import compileModel
from riaps.lang.depl import DeploymentModel

import sys
import argparse
import pydot

ucount = 0

def unique(name):
    global ucount
    ucount = ucount + 1
    return str(name) + '_' + str(ucount)

def visualize_messages(G,appModel,msgMap, msgMapUsed):
    msgs = pydot.Subgraph('msgs',rank='min') #,rankdir='LR')
    msgList = appModel['messages']
    for msg in msgList:
        msgName = msg['name']
        msgNode = pydot.Node(msgName)
        msgNode.set('shape','ellipse')
        msgs.add_node(msgNode)
        msgMap[msgName] = msgNode
        msgMapUsed[msgName] = False
    G.add_subgraph(msgs)
    return msgs

def findMsgNode(msgType,
                actorLocals,actorLocalMessageNodes,
                actorInternals,actorInternalMessageNodes,
                msgMap,msgMapUsed,
                localMsgGraph,
                internalMsgGraph):
    msgNode = None
    if msgType in actorLocals:
        if msgType in actorLocalMessageNodes:
            msgNode = actorLocalMessageNodes[msgType]
        else: 
            msgNode = pydot.Node(unique(msgType), label=msgType)
            msgNode.set('shape','ellipse')
            localMsgGraph.add_node(msgNode)
            actorLocalMessageNodes[msgType] = msgNode
    elif msgType in actorInternals:
        if msgType in actorInternalMessageNodes:
            msgNode = actorInternalMessageNodes[msgType]
        else: 
            msgNode = pydot.Node(unique(msgType), label=msgType)
            msgNode.set('shape','ellipse')
            internalMsgGraph.add_node(msgNode)
            actorInternalMessageNodes[msgType] = msgNode
    else:
        msgNode = msgMap[msgType]
        msgMapUsed[msgType] = True
    return msgNode

def findMsgNodePair(msgType,
                    actorLocals,actorLocalMessageNodes,
                    actorInternals,actorInternalMessageNodes,
                    msgMap,
                    localMsgGraph,internalMsgGraph,globalMsgGraph):
    msgNode = None
    reqType,repType = msgType
    msgPair = str(reqType) + '_' + str(repType)
    msgLabel = '{' + str(reqType) + ' | ' + str(repType) + '}'
    if (reqType in actorLocals) and (repType in actorLocals):
        if msgPair in actorLocalMessageNodes:
            msgNode = actorLocalMessageNodes[msgPair]
        else:
            msgNode = pydot.Node(unique(msgPair), label=msgLabel)
            msgNode.set('shape','Mrecord')
            localMsgGraph.add_node(msgNode)
            actorLocalMessageNodes[msgPair] = msgNode
    elif (reqType in actorInternals) and (repType in actorInternals):
        if msgPair in actorInternalMessageNodes:
            msgNode = actorInternalMessageNodes[msgPair]
        else:
            msgNode = pydot.Node(unique(msgPair), label=msgLabel)
            msgNode.set('shape','Mrecord')
            internalMsgGraph.add_node(msgNode)
            actorInternalMessageNodes[msgPair] = msgNode      
    else:
        if msgPair in msgMap:
            msgNode = msgMap[msgPair]
        else:
            msgNode = pydot.Node(unique(msgPair), label=msgLabel)
            msgNode.set('shape','Mrecord')
            msgMap[msgPair] = msgNode
            globalMsgGraph.add_node(msgNode)
    return msgNode

def visualize_actors(G,appModel,hostName,hostLabel,actors,msgMap,msgMapUsed,globalMsgSubgraph):
    host = pydot.Cluster(graph_name=hostName, label=hostLabel, rankdir = 'BT', rank='max')
    actorModels = appModel['actors']
    componentModels = appModel['components']
    deviceModels = appModel['devices']
    
    actorLocals = [] 
    actorLocalMessageNodes = { }
    localMsgSubgraph = None
    
    # Locals 
    for actor in actors:
        actorName = actor['name']
        actorModel = actorModels[actorName]
        for localMessage in actorModel['locals']:
            actorLocals.append(localMessage['type'])
    if len(actorLocals) != 0:
            localMsgSubgraph = pydot.Subgraph(unique(hostName + '_msgs'),rank='min') #,rankdir='LR')
            host.add_subgraph(localMsgSubgraph)
    
    for actor in actors:
        actorName = actor['name']
        # actorNode = pydot.Node(unique(actorName),label=actorName)
        # actorNode.set('shape','box3d')
        actorCluster = pydot.Cluster(graph_name=unique(actorName), label=actorName, style='rounded')
        actorModel = actorModels[actorName]
        # Internals
        actorInternals = []
        for internalMessage in actorModel['internals']:
            actorInternals.append(internalMessage['type'])
        actorInternalMessageNodes = { }
        if len(actorInternals) != 0:
            internalMsgSubgraph = pydot.Subgraph(unique(actorName + '_msgs'),rank='min') #,rankdir='LR')
            actorCluster.add_subgraph(internalMsgSubgraph)
        else:
            internalMsgSubgraph = None 
        for instName,instObj in actorModel['instances'].items():
            instType = instObj['type']
            compName = instName + '_' + instType
            compLabel = '\"' + instName + ':' + instType + '\"'
            compNode = pydot.Node(unique(compName), label=compLabel, rank='max')
            compNode.set('shape','component')
            actorCluster.add_node(compNode)
            compType = None
            if instType in componentModels:
                compType = componentModels[instType]
            elif instType in deviceModels:
                compType = deviceModels[instType]
            compPorts = compType['ports']
            for _key,value in compPorts['pubs'].items():
                msgType = value['type']
                msgNode = findMsgNode(msgType,
                                      actorLocals,actorLocalMessageNodes,
                                      actorInternals,actorInternalMessageNodes,
                                      msgMap,msgMapUsed,localMsgSubgraph,internalMsgSubgraph)
                G.add_edge(pydot.Edge(compNode,msgNode))
            for _key,value in compPorts['subs'].items():
                msgType = value['type']
                msgNode = findMsgNode(msgType,
                                      actorLocals,actorLocalMessageNodes,
                                      actorInternals,actorInternalMessageNodes,
                                      msgMap,msgMapUsed,localMsgSubgraph,internalMsgSubgraph)
                G.add_edge(pydot.Edge(msgNode,compNode))
            for _key,value in compPorts['qrys'].items():
                msgType = (value['req_type'],value['rep_type'])
                msgNode = findMsgNodePair(msgType,
                                          actorLocals,actorLocalMessageNodes,
                                          actorInternals,actorInternalMessageNodes,
                                          msgMap,
                                          localMsgSubgraph,internalMsgSubgraph,globalMsgSubgraph)
                G.add_edge(pydot.Edge(compNode,msgNode))
            for _key,value in compPorts['anss'].items():
                msgType = (value['req_type'],value['rep_type'])
                msgNode = findMsgNodePair(msgType,
                                          actorLocals,actorLocalMessageNodes,
                                          actorInternals,actorInternalMessageNodes,
                                          msgMap,
                                          localMsgSubgraph,internalMsgSubgraph,globalMsgSubgraph)
                G.add_edge(pydot.Edge(msgNode,compNode))
                
            for _key,value in compPorts['reqs'].items():
                msgType = (value['req_type'],value['rep_type'])
                msgNode = findMsgNodePair(msgType,
                                          actorLocals,actorLocalMessageNodes,
                                          actorInternals,actorInternalMessageNodes,
                                          msgMap,localMsgSubgraph,internalMsgSubgraph,globalMsgSubgraph)
                G.add_edge(pydot.Edge(compNode,msgNode))
            for _key,value in compPorts['reps'].items():
                msgType = (value['req_type'],value['rep_type'])
                msgNode = findMsgNodePair(msgType,
                                          actorLocals,actorLocalMessageNodes,
                                          actorInternals,actorInternalMessageNodes,
                                          msgMap,localMsgSubgraph,internalMsgSubgraph,globalMsgSubgraph)
                G.add_edge(pydot.Edge(msgNode,compNode))

            for _key,value in compPorts['clts'].items():
                msgType = (value['req_type'],value['rep_type'])
                msgNode = findMsgNodePair(msgType,
                                          actorLocals,actorLocalMessageNodes,
                                          actorInternals,actorInternalMessageNodes,
                                          msgMap,localMsgSubgraph,internalMsgSubgraph,globalMsgSubgraph)
                G.add_edge(pydot.Edge(compNode,msgNode))
            for _key,value in compPorts['srvs'].items():
                msgType = (value['req_type'],value['rep_type'])
                msgNode = findMsgNodePair(msgType,
                                          actorLocals,actorLocalMessageNodes,
                                          actorInternals,actorInternalMessageNodes,
                                          msgMap,localMsgSubgraph,internalMsgSubgraph,globalMsgSubgraph)
                G.add_edge(pydot.Edge(msgNode,compNode))
                           
        host.add_subgraph(actorCluster)
    G.add_subgraph(host) 

def cleanupMessages(G,msgMap,msgMapUsed):
    for msgName,msgUsed in msgMapUsed.items():
        if not msgUsed:
            G.del_node(msgMap[msgName])
            
def visualize(deplo,models):
    appName = deplo.getAppName()
    G = pydot.Dot(appName, graph_type='digraph', rankdir='TB', nodesep = "0.1",
                  ranksep="1.5", orientation='l') # , splines='ortho')
    appModel = models[appName]
    
    # Build a host map with all the actors
    hostMap = { }
    allActors = [ ]
    for depl in deplo.deployments:
        hosts = depl['target']
        actors = depl['actors']
        if hosts == []:
            allActors = allActors + actors
        else:
            for host in hosts:
                if host in hostMap:
                    hostMap[host] = hostMap[host] + actors
                else:
                    hostMap[host] = actors
    
    msgMap = { }
    msgMapUsed = { } 
    msgSubgraph = visualize_messages(G, appModel, msgMap, msgMapUsed)
    
    if allActors != []:
        visualize_actors(G,appModel,'all','- all -',allActors,msgMap,msgMapUsed,msgSubgraph)
    
    for hostName in hostMap.keys():
        visualize_actors(G,appModel,hostName,hostName,hostMap[hostName],msgMap,msgMapUsed,msgSubgraph)
    
    cleanupMessages(msgSubgraph,msgMap,msgMapUsed)
    
    G.write(appName + '.dot', format='raw', prog='dot')
    
    return appName
    

def gviz(model,deplo,verbose=False):
    try:
        model = compileModel(model,verbose,generate=False)
        deplo = DeploymentModel(deplo,verbose)
        return visualize(deplo,model)
    except Exception as e: 
        errMsg = "Unexpected error %s: %s" % (sys.exc_info()[0],e.args())
        print (errMsg)
        return None
        
def main(debug=False):
    parser = argparse.ArgumentParser()
    parser.add_argument("model", help="model file")       # Model file argument
    parser.add_argument("deplo", help="deployment file")
    parser.add_argument("-v","--verbose", help="print JSON on console", action="store_true")
    args = parser.parse_args()
    gviz(args.model,args.deplo,args.verbose)

if __name__ == '__main__':
    m = main()
