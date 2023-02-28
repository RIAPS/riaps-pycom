import re
import os
from collections import namedtuple
import datetime
from statemachine import StateMachine, State
import argparse

Event = namedtuple("Event",['ts','lvl','msg'])

spdlogformat = re.compile("^\[(?P<logLevel>info)\]:\[(?P<timestamp>[0-9:\-\. ]+)\]:\[(?P<pid>[0-9]+)\]:(?P<msg>.*)")
pylogformat = re.compile("^(?P<logLevel>INFO|ERROR):(?P<timestamp>[0-9:, -]+?):\[(?P<pid>[0-9]+)\]:(?P<msg>.*)")
journaldformat = re.compile("^Feb \d{2} [\d:]+ riaps-[0-9a-f]{4} RIAPS-DEPLO\[\d+\]: (?P<msg>.*)")

discofmt = re.compile("^riaps\.discd\.(dbase|dbase_dht|discs):(?P<msg>.*?)")
deplofmt = re.compile("^riaps\.deplo\.deplo:(?P<msg>.*?)")

dc_format = re.compile("^riaps.run.dc:(?P<msg>.*)")
grpthdfmt = re.compile("^\.\.\. (?P<msg>.*)")
grpthd_ndmsg = re.compile("^\[(?P<groupType>\w+)\.(?P<groupInstance>\w+)\]\.(?P<state>\d):(?P<cmd>tic|req|vot|ldr)")

def from_journald(s: str):
    m = journaldformat.match(s)
    if not m:
        return
    msg = m['msg']
    return msg

def from_spdlog(s: str):
    m = spdlogformat.match(s)
    if not m:
        return
    lvl,ts,pid,msg = (m['logLevel'],m['timestamp'],m['pid'],m['msg'])
    #01-12-2023 21:24:34.336
    # ts = strptime(ts, "%m-%d-%Y %H:%M:%S.%f")
    ts = datetime.datetime.strptime(ts.split()[1], "%H:%M:%S.%f")
    ts = (((ts.hour*60)+ts.minute)*60+ts.second) + ts.microsecond/1_000_000.0
    return lvl,ts,pid,msg

def from_pylog(s: str):
    m = pylogformat.match(s)
    if not m:
        return
    lvl,ts,pid,msg = (m['logLevel'],m['timestamp'],m['pid'],m['msg'])
    #01-12-2023 21:24:34.336
    ts = datetime.datetime.strptime(ts, "%H:%M:%S,%f")
    ts = (((ts.hour*60)+ts.minute)*60+ts.second) + ts.microsecond/1_000_000.0
    return lvl,ts,pid,msg

class Results(object):
    def __init__(self):
        self.nodes = {}
    
    def add(self, node):
        self.nodes[node.hostname] = node
    
    def getNode(self, hostname: str):
        return self.nodes[hostname]

    def asUML(self, outPath):
        with open(outPath, 'w') as file:
            file.write("@startuml\n")
            for hostname, node in self.nodes.items():
                file.write(f"concise \"{hostname}\" as {node.umlname}\n")
            file.write("\n")
            [n.asUML(file) for n in self.nodes.values()]
            file.write("@enduml\n")
        
class NodeRecord(object):
    def __init__(self, hostname: str):
        self.hostname=hostname
        self.umlname = self.hostname.replace('-','').replace('.local','')
        self.actors = []
        self.deplo = None
        self.disco = None

    def __eq__(self,other):
        return self.hostname == other.hostname

    def addActor(self, actor):
        actor.setNode(self.umlname)
        self.actors.append(actor)

    def importJournal(self, path):
        with open(path,'r') as file:
            for line in file:
                m = pylogformat.match(line)
                if not m:
                    # print(f"Unknown format in journal log. Line:\n{line}",end='')
                    continue
                lvl,ts,pid,msg = (m['logLevel'],m['timestamp'],m['pid'],m['msg'])
                m = discofmt.match(msg)
                if m:
                    if self.disco is None: self.disco = DiscoLog(pid)
                    self.disco.addEvent(Event(ts,lvl,msg))
                    continue
                m = deplofmt.match(msg)
                if m:
                    if self.deplo is None: self.deplo = DeploLog(pid)
                    self.deplo.addEvent(Event(ts,lvl,msg))
                    continue
                print(f"Unknown logger: Line:\n{line}")
        
    def asUML(self, file):
        for a in self.actors:
            a.asUML(file)

class DistributedCoordinator(object):
    STATES = ["NONE", "FOLLOWER", "CANDIDATE", "LEADER"]
    
    class Group():
        def __init__(self,name):
            self.name = name
            self.events = []
            print(f"Made group {self.name}")

        def print_timeline(self):
            self.events.sort(key=lambda x: x.ts)
            groupMem = set()
            for e in self.events:
                if e.msg.find("Group.update(") == 0:
                    _, _, hostname = e.msg.partition("(")
                    hostname = hostname[:-1].replace(",",":")
                    if hostname in groupMem:
                        print(f"{hostname} UPDATED TWICE")
                    groupMem.add(hostname)
                    print(f"{e.ts}: Group is: {groupMem}")
                

    def __init__(self):
        super().__init__()
        self.events = []
        self.state = None
        self.groups = {}
        self.theGroup = None

    def asUML(self, file):
        # self.theGroup.print_timeline()
        for e in self.theGroup.events:
            n = grpthdfmt.match(e.msg)
            if n is None: continue
            m = grpthd_ndmsg.match(n['msg'])
            state = __class__.STATES[int(m['state'])]
            if state == "LEADER":
                state += "#pink"
            file.write(f"{e.ts} is {state}\n")

    def addEvent(self, e: Event):
        # print(f"DC: adding event {e}")
        if e.msg.find("Coordinator.joinGroup") == 0:
            coord, _, groupName = e.msg.partition('(')
            groupName = groupName[:-1].replace(',','.')
            # self.groups[groupName] = Group()
            # self.groups[groupName].events.append(e)
            self.theGroup = DistributedCoordinator.Group(groupName)
            self.theGroup.events.append(e)
            return
        if e.msg.find("Group.update(") == 0:
            self.theGroup.events.append(e)
            print("Added group update event")
            return
        if e.msg.find("... [") == 0:
            self.theGroup.events.append(e)
            return
            


        #NOTE: This assumes each actor is only participating in a single group
        # m = grpthdfmt.match(s)
        # if m:
        #     n = grpthd_ndmsg.match(m['msg'])
        #     if n:
        #         if self.state != n['state']:
        #             self.state = n['state']
        #             self.events.append(Event(e.ts,"info", __class__.STATES[int(n['state'])]))

            #BOOKMARK: I was working on parsing dc log statements
            # Consider ordering of events: maybe guarantee that all msgs are in order first?
            # Then, check events for state changes, create list of state changes
                
class DiscoLog(object):
    def __init__(self, pid):
        super().__init__()
        self.events = []
        self.pid = pid

    def addEvent(self, e: Event):
        if e.msg.find("FMMon.b") == 0:
            return
        self.events.append(e)

class DeploLog(object):
    def __init__(self, pid):
        super().__init__()
        self.pid = pid
        self.events = []
    
    def addEvent(self, e: Event):
        self.events.append(e)

class ActorLog(object):
    def __init__(self):
        super().__init__()
        self.pid = None
        self.events = []
        self.dc = DistributedCoordinator()

    def setNode(self, node):
        self.node = node

    def fromFile(filepath):
        pass

class StateGroupie(ActorLog):
    @staticmethod
    def valid(filename):
        return filename == "StateGroupie.log"

    def __init__(self):
        super().__init__()

    def addEvent(self,e: Event):
        # print(f"SG adding event {e}")
        m = dc_format.match(e.msg)
        if m:
            self.dc.addEvent(Event(e.ts,e.lvl,m['msg']))


    def asUML(self, file):
        file.write(f"@{self.node}\n")
        self.dc.asUML(file)
        file.write("\n")


    def fromFile(self,filepath):
        with open(filepath,'r') as fd:
            for l in fd:
                notAdded = True
                for fmt in [from_spdlog, from_pylog]:
                    res = fmt(l)
                    if res is None:
                        continue
                    lvl,ts,pid,msg = res
                    if not self.pid: self.pid = pid
                    assert(self.pid==pid)
                    self.addEvent(Event(ts,lvl,msg))
                    notAdded = False
                    break
                if notAdded:
                    print(f"ERROR: {l} did not match any known formats")
        return self



        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("log_dir",type=str)
    args=parser.parse_args()
    num_nodes = args.log_dir.split("-")[-1]
    theResults = Results()
    logsPath = os.path.join(os.getcwd(),args.log_dir)

    for node_dir in os.scandir(logsPath):
        # assert dir.is_dir()s
        if node_dir.name not in theResults.nodes:
            theResults.add(NodeRecord(node_dir.name))
        node = theResults.getNode(node_dir.name)
        for root, dirs, files in os.walk(os.path.join(logsPath,node.hostname)):
            assert len(dirs) == 0
            for f in files:
                if StateGroupie.valid(f):
                    node.addActor(StateGroupie().fromFile(os.path.join(root,f)))
                elif f == 'journal.log':
                    node.importJournal(os.path.join(root,f))
    print(f"# of nodes: {len(theResults.nodes)}")
    theResults.asUML(os.path.join(os.getcwd(),args.log_dir,f"results-{num_nodes}.uml"))
    # theResults