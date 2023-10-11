'''
Distributed coordination

Python implementation of group formation, communications, leader election, consensus and action coordination. 

Created on Feb 23, 2019
Author: riaps
'''

import time
import logging
import struct
import collections
import traceback
import random
import string
import ipaddress
# import ctypes
import threading
import zmq
from zmq.backend.cython.utils import ZMQError
# from riaps.run.port import Port
from riaps.consts.defs import *
# from riaps.utils import spdlog_setup
# import spdlog
from riaps.run.exc import BuildError, OperationError, PortError
from riaps.run.dcPorts import GroupPubPort, GroupSubPort, GroupQryPort, GroupAnsPort
import capnp
from riaps.run import dc_capnp

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle


class Poll(object):
    '''
    Poll object to represent an active poll in the group leader. 
    '''
    
    # Voting type 
    MAJORITY = 'majority'  # Must match dc_capnp spec 
    CONSENSUS = 'consensus'
    
    # Subject type
    VALUE = 'value'  # Must match dc_capnp spec 
    ACTION = 'action'
    
    def __init__(self, parent, rfv, member, timeout, deadline, numPeers):
        self.parent = parent
        self.topic = rfv.topic
        self.rfvId = rfv.rfvId
        self.kind = rfv.kind
        self.subject = rfv.subject
        self.release = rfv.release
        self.started = rfv.started
        self.timeout = timeout
        self.deadline = deadline
        self.member = member
        self.numPeers = numPeers
        self.threshold = int(numPeers / 2 + 1)
        self.voteCnt = 0
        self.yesCnt = 0
   
    def vote(self, vote):
        '''
        Count one vote (yes/no)
        '''
        self.voteCnt += 1
        if vote: self.yesCnt += 1 
    
    def expired(self, now):
        '''
        Return True if the voting has expired
        '''
        return (now > self.deadline)
    
    def allVoted(self):
        '''
        Return True if all peers voted
        '''
        return (self.voteCnt == self.numPeers)
    
    def result(self):
        '''
        Return True if the majority/all voted yes 
        '''
        if self.kind == 'majority':
            return (self.yesCnt >= self.threshold)
        elif self.kind == 'consensus':
            return (self.yesCnt == self.numPeers)
        
        
class GroupThread(threading.Thread):
    '''
    Worker thread for DC behavior
    '''
    # Group/component states (RAFT)
    FOLLOWER = 1           
    CANDIDATE = 2
    LEADER = 3
    
    # Coordination messages, with content
    HEARTBEAT = 'tic'.encode('utf-8')
    # { ownId }
    REQVOTE = 'req'.encode('utf-8')
    # { term ; ownId }
    RSPVOTE = 'vot'.encode('utf-8')
    # { term; candId; bool; ownId }
    AUTHORITY = 'ldr'.encode('utf-8')
    # { term; ldrId; ldrHost; ldrPort } 
    # Special port number indicating no leader
    NO_LEADER = 0
    
    def __init__(self, group):
        threading.Thread.__init__(self,daemon=False)
        self.logger = logging.getLogger(__name__)
        self.group = group
        self.coordinated = False if self.group.kind == "default" else True
        # Assumption: we use IPv4 addresses - converted to ulong for the wire protocol
        self.host = ipaddress.IPv4Address(self.group.parent.parent.owner.parent.getGlobalIface())
        self.ldrPort = None
        self.groupSize = group.groupSize
        self.groupHeartbeat = group.heartbeat               # const.groupHeartbeat 
        self.groupElectionMin = group.electionMin           # const.groupElectionMin
        self.groupElectionMax = group.electionMax           # const.groupElectionMax
        self.groupPeerTimeout = group.peerTimeout           # const.groupPeerTimeout
        self.groupConsensusTimeout = group.consensusTimeout # const.groupConsensusTimeout
        self.timeout = None
        self.leaderDeadline = None
        self.numPeers = -1
        self.leader = None
        self.ownId = None 
    
    def setup(self):
        self.group.setup(self)
        if self.coordinated:
            actorId = self.group.parent.parent.owner.parent.getActorID()
            # Assumption: id can be represented on 8 bytes
            self.ownId = actorId + id(self.group).to_bytes(8, 'big')
            assert(len(self.ownId) == 16)
            self.peers = {}
            self.numPeers = len(self.peers)
            self.timeout = self.groupHeartbeat
            self.setLeaderDeadline()
            self.lastWait = 0
            self.lastHeartbeat = 0
            self.term = 0
            self.votes = 0
            self.votedFor = None
            self.leader = None 
            self.polls = { }
            
    def getOwnId(self):
        return self.ownId
    
    def isLeader(self):
        return self.leader == self.ownId
    
    def setLeaderDeadline(self):
        '''
        Set deadline for heartbeat from leader 
        '''
        timeout = random.randrange(self.groupElectionMax, self.groupPeerTimeout)
        self.leaderDeadline = time.time() + timeout/1000.0
    
    def electionTimeout(self):
        '''
        Produce a random election timeout
        '''
        return random.randrange(self.groupElectionMin, self.groupElectionMax)
    
    def threshold(self):
        '''
        Calculate the threshold for leader election, based on membership list 
        '''
        return int(self.numPeers / 2 + 1)  # Threshold for votes for leader election
    
    def setTimeout(self, value, now):
        '''
        Set the next timeout value, update lastWait (with 'now')
        '''
        assert(type(value) == int)
        self.timeout = value
        self.lastWait = now
            
    def heartbeat(self, now):
        '''
        Send out a group heartbeat (so that group members can maintain an accurate membership list) 
        '''
        if now > (self.lastHeartbeat + self.groupHeartbeat / 1000.0):
            msg = struct.pack('!16s', self.ownId)
            self.pubPort.sendGroup(GroupThread.HEARTBEAT, msg)
            self.lastHeartbeat = now
        
    def sendChangeMessage(self, change, someId):
        '''
        Send message about a change to the component
        '''
        msgOut = [zmq.Frame(change), zmq.Frame(someId)]
        self.groupSocket.send_multipart(msgOut)
    
    def updatePeers(self, now):
        '''
        Update membership list (with the current time as the last time a peer was heard from)
        '''
        leavers = []
        for peer in \
            [p for p in self.peers if int((now - self.peers[p]) * 1000) > self.groupPeerTimeout]:
                leavers += [peer] 
        if len(leavers) > 0:
            for leaver in leavers:
                self.sendChangeMessage(Group.GROUP_MLT, leaver)  # Member dropped out
                del self.peers[leaver] 
            self.numPeers = len(self.peers)
                  
    def updateTimeout(self, now):
        '''
        Update the timeout value - used when a data message was received from the group; 
        the timeout is updated to reflect elapsed time.
        '''
        elapsed = now - self.lastWait
        remains = max(self.timeout - int(elapsed * 1000), 1)
        self.lastWait = now
        assert(type(remains) == int)
        self.timeout = remains
    
    def handleCompMessage(self):
        '''
        Handle a message coming from the component
        '''
        toStop = False
        msgFrames = self.groupSocket.recv_multipart()
        cmd = msgFrames[0]
        if cmd == Group.GROUP_UPD:  # Update message for sub port
            host, port = msgFrames[1].decode(), struct.unpack("d", msgFrames[2])[0]
            self.logger.info("GroupThread.handleCompMessage(GROUP_UPD,%s,%d)", host, port)
            self.subPort.update(host, port)
        elif cmd == Group.GROUP_MSG:  # Generic message to be published to the group
            self.logger.info("GroupThread.handleCompMessage(GROUP_MSG,...)")
            try:
                self.pubPort.sendGroup(Group.GROUP_MSG, msgFrames[1])
                self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ACK)])
            except zmq.error.ZMQError as e:
                self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ERR), zmq.Frame(pickle.dumps(e))])
                self.logger.error("error sending GROUP_MSG:%s", str(e))
        elif cmd == Group.GROUP_MTL:  # Message for the leader (from component)
            self.logger.info("GroupThread.handleCompMessage(GROUP_MTL,...)")
            if self.leader == None:  # Error: no leader
                self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_NLD)])
            else:
                try:
                    if self.isLeader():  # We are the leader
                        self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ACK)])   
                        msg = msgFrames[1]  # Forward it to component
                        msgOut = [zmq.Frame(Group.GROUP_MTL), zmq.Frame(msg)]    
                        msgOut += [zmq.Frame(bytes(0))]  # Special case: 0 == own identity
                        if self.group.isTimed:
                            now = time.time()
                            self.recvTime = now
                            self.sendTime = now
                            msgOut += [zmq.Frame(self.recvTime)]
                            msgOut += [zmq.Frame(self.sendTime)]
                        self.groupSocket.send_multipart(msgOut)
                    else:
                        self.qryPort.sendToLeader(Group.GROUP_MTL, msgFrames[1])
                        self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ACK)])
                except zmq.error.ZMQError as e:
                    self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ERR), zmq.Frame(pickle.dumps(e))])
                    self.logger.error("error sending GROUP_MTL:%s", str(e))
        elif cmd == Group.GROUP_MFL:  # Message from leader (for a component)
            self.logger.info("GroupThread.handleCompMessage(GROUP_MFL,...)")
            if self.leader == None:  # Error: no leader
                self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_NLD)])
            else:
                try:
                    if self.isLeader and msgFrames[2] == bytes(0):  # We are the leader and we sent the message
                        self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ACK)])   
                        msg = msgFrames[1]  # Forward it to component
                        msgOut = [zmq.Frame(Group.GROUP_MFL), zmq.Frame(msg)]    
                        if self.group.isTimed:
                            now = time.time()
                            self.recvTime = now
                            self.sendTime = now
                            msgOut += [zmq.Frame(self.recvTime)]
                            msgOut += [zmq.Frame(self.sendTime)]
                        self.groupSocket.send_multipart(msgOut)
                    else:
                        self.ansPort.set_identity(msgFrames[2])
                        self.ansPort.sendToMember(Group.GROUP_MFL, msgFrames[1])
                        self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ACK)])
                except zmq.error.ZMQError as e:
                    self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ERR), zmq.Frame(pickle.dumps(e))])
                    self.logger.error("error sending GROUP_MFL:%s", str(e))
        elif cmd == Group.GROUP_RFV:  # Request for vote (through leader)
            self.logger.info("GroupThread.handleCompMessage(GROUP_RFV,...)")
            if self.leader == None:  # Error: no leader
                self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_NLD)])
            else:
                try:
                    if self.isLeader():  # We are the leader
                        self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ACK)])   
                        msg = msgFrames[1]
                        identity = bytes(0)  # Self identity                      
                        ok = self.startPoll(msg, identity)  # Start the poll
                        if (ok):
                            self.pubPort.sendGroup(Group.GROUP_RCM, msg)  # Send RCM to group
                        else: 
                            with dc_capnp.GroupVote.from_bytes(msg) as rfv:  # Poll failed (before it got started)        
                                which = rfv.which()
                                assert(which == 'rfv')
                                rfvId = rfv.rfv.rfvId
                                self.announceConsensus(rfvId, 'timeout')
                    else:
                        self.qryPort.sendToLeader(Group.GROUP_RFV, msgFrames[1])
                        self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ACK)])
                except zmq.error.ZMQError as e:
                    self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ERR), zmq.Frame(pickle.dumps(e))])
                    self.logger.error("error sending GROUP_RFV:%s", str(e)) 
        elif cmd == Group.GROUP_RTC:  # Reply to consensus request
            self.logger.info("GroupThread.handleCompMessage(GROUP_RTC,...)")
            if self.leader == None:  # Error: no leader
                self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_NLD)])
            else:
                try:
                    if self.isLeader():  # We are the leader and we sent the vote
                        self.updatePoll(msgFrames[1])
                    else:
                        self.qryPort.sendToLeader(Group.GROUP_RTC, msgFrames[1])
                    self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ACK)])
                except zmq.error.ZMQError as e:
                    self.groupSocket.send_multipart([zmq.Frame(Group.GROUP_ERR), zmq.Frame(pickle.dumps(e))])
                    self.logger.error("error sending GROUP_RTC:%s", str(e)) 
        elif cmd == Group.GROUP_MLT:    # Our component is leaving the group
            self.logger.info("GroupThread.handleCompMessage(GROUP_MLT,...)")
            self.pubPort.sendGroup(Group.GROUP_MLT,zmq.Frame(self.ownId))
            toStop = True 
        else:
            self.logger.error("GroupThread.handleCompMessage() - unknown message type: %s", str(cmd))
        return toStop
            
        
    def handleTimeout(self, now):
        '''
        Handle the timeout on communications within the group
        '''
        self.logger.info("GroupThread.handleTimeout()")
        assert(self.coordinated)
        self.updatePeers(now)
        self.checkAllPolls(now)
        if self.state == GroupThread.FOLLOWER:  
            if self.leaderDeadline and now > self.leaderDeadline: # Past leader deadline (if set)
                if self.numPeers > int(self.groupSize / 2) + 1:   
                    self.logger.info("... FOLLOWER --> CANDIDATE, starting leader election")                     
                    if self.leader != None:
                        self.logger.info("... past leader %s deadline" % self.leader.hex())
                        self.sendChangeMessage(Group.GROUP_LEX, self.leader)  # Leader exited
                    self.term += 1  # increment term
                    self.state = GroupThread.CANDIDATE  # candidate state
                    self.votes = 1                      # self-vote
                    self.votedFor = self.ownId          # voted for ourselves
                    self.qryPort.update(None, None)  # Disconnect query port
                    msg = struct.pack('!L16s', self.term, self.ownId)
                    self.pubPort.sendGroup(GroupThread.REQVOTE, msg)    # request votes
                    self.setTimeout(self.electionTimeout(), now)        # Timeout for votes to come in
                    self.leaderDeadline = None                          # No leader / deadline
                    self.leader = None
                else:
                    self.logger.info("... FOLLOWER, no majority in group to start election")
                    self.setLeaderDeadline()         
                    self.setTimeout(self.groupHeartbeat,now)
            else:
                self.setTimeout(self.groupHeartbeat,now)
        elif self.state == GroupThread.CANDIDATE:  # We are beyond the current election timeout then
            self.logger.info("... CANDIDATE --> FOLLOWER, timeout on leader election")
            self.state = GroupThread.FOLLOWER  # follower state
            self.votedFor = None
            if self.leader != None:
                self.logger.info("... previous leader %s ?" % self.leader.hex())
                self.sendChangeMessage(Group.GROUP_LEX, self.leader)  # Leader exited
            self.leader = None
            self.setTimeout(self.groupHeartbeat, now)
            self.leaderDeadline = None
        elif self.state == GroupThread.LEADER:  # Leader sends message to inform members: term,id, host, port
            self.logger.info("... LEADER, sending out leadership note")
            assert(self.leader == self.ownId)
            msg = struct.pack('!L16sLL', self.term, self.ownId, \
                              int(self.host), \
                              int(self.ldrPort))
            self.pubPort.sendGroup(GroupThread.AUTHORITY, msg)
            self.setTimeout(self.groupHeartbeat, now)
            self.leaderDeadline = None
        else:
            self.logger.error("GroupThread.handleTimeout() - in undefined state")
            pass  # Error : timeout in unknown state")
    
    
    def handleNetMessage(self, now=None):
        '''
        Handle (broadcast) messages coming from the group. 
        Messages could be data messages (to be handed over to the component), 
        peer heartbeat messages, or  election-related messages
        '''
        self.logger.info("GroupThread.handleNetMessage()")
        msgFrames = self.subPort.recvGroup()
        cmd = msgFrames[0]
        if cmd == Group.GROUP_MSG:
            self.logger.info("... handle GROUP_MSG")
            msg = msgFrames[1]           
            msgOut = [zmq.Frame(Group.GROUP_MSG), zmq.Frame(msg)]
            if self.group.isTimed:
                self.recvTime = self.subPort.recvTime()
                self.sendTime = self.subPort.sendTime
                msgOut += [zmq.Frame(self.recvTime)]
                msgOut += [zmq.Frame(self.sendTime)]
            self.groupSocket.send_multipart(msgOut)
            if self.coordinated:
                self.updateTimeout(now)
            return 
        elif cmd == Group.GROUP_MLT:    # One of our peers left the group
            frame = msgFrames[1]
            leaver = struct.unpack('!16s', frame)[0]
            if leaver in self.peers:
                self.sendChangeMessage(Group.GROUP_MLT,leaver)
                del self.peers[leaver] 
            self.numPeers = len(self.peers)
        if self.coordinated:  # Non-data messages are meaningful only for coordinated groups 
            assert(now != None)
            frame = msgFrames[1]
            self.logger.info("... [%s].%d:%s", \
                             self.group.getGroupName(), self.state, cmd.decode('utf-8'))
            if cmd == GroupThread.HEARTBEAT:  # Incoming peer heartbeat message
                try:
                    peer = struct.unpack('!16s', frame)[0]
                except:
                    self.logger.error("... invalid peer in heartbeat: %s" % str(frame))
                    return
                if peer not in self.peers:
                    self.sendChangeMessage(Group.GROUP_MJD, peer)
                self.peers[peer] = now
                self.numPeers = len(self.peers)
                self.updateTimeout(now)
                return
            if cmd == Group.GROUP_RCM:  # Incoming group RCM message (from leader to a member)
                self.logger.info("... handle GROUP_RCM")
                msg = msgFrames[1]           
                msgOut = [zmq.Frame(Group.GROUP_RCM), zmq.Frame(msg)]
                if self.group.isTimed:
                    self.recvTime = self.subPort.recvTime()
                    self.sendTime = self.subPort.sendTime
                    msgOut += [zmq.Frame(self.recvTime)]
                    msgOut += [zmq.Frame(self.sendTime)]
                self.groupSocket.send_multipart(msgOut)  # forward it to component
                self.updateTimeout(now)
                self.setLeaderDeadline()
                return 
            if cmd == Group.GROUP_ANN:  # Incoming announcement (from leader)
                self.logger.info("... handle GROUP_ANN")
                msg = msgFrames[1]           
                msgOut = [zmq.Frame(Group.GROUP_ANN), zmq.Frame(msg)]
                if self.group.isTimed:
                    self.recvTime = self.subPort.recvTime()
                    self.sendTime = self.subPort.sendTime
                    msgOut += [zmq.Frame(self.recvTime)]
                    msgOut += [zmq.Frame(self.sendTime)]
                self.groupSocket.send_multipart(msgOut)  # forward it to component
                self.updateTimeout(now)
                self.setLeaderDeadline()
                return
            # Everything else is election-related
            if self.state == GroupThread.FOLLOWER:  # We are a FOLLOWER              
                if cmd == GroupThread.AUTHORITY:  # Message from leader
                    self.logger.info('... leader asserts authority')
                    (_term, _leader, _host, _port) = struct.unpack('!L16sLL', frame)
                    if self.term >= _term and self.leader and self.leader != _leader:
                        self.logger.info("GroupThread[%s] - leader has changed", self.group.getGroupName()) 
                    self.term = _term  # update term/leader
                    prevLeader = self.leader
                    self.leader = _leader    
                    if prevLeader != _leader:  # If leader has changed
                        self.sendChangeMessage(Group.GROUP_LEL, self.leader)             
                    self.votedFor = None  # clear last vote
                    self.setTimeout(self.electionTimeout(), now)  # TODO: Set new election timeout 
                    self.setLeaderDeadline()
                    if _port == GroupThread.NO_LEADER:
                        _host, _port = None, None  # Will this ever happen?
                    else:
                        _host = ipaddress.IPv4Address(_host).compressed
                        _port = int(_port)
                    self.qryPort.update(_host, _port)  # Update query port to new leader
                elif cmd == GroupThread.REQVOTE:  # Message to request a vote
                    self.logger.info('... follower vote requested')
                    (_term, _node) = struct.unpack('!L16s', frame)
                    vote = None
                    if self.votedFor == None:  # Not voted yet
                        vote = True  # vote yes
                    else:  # Already voted
                        if _term > self.term:  # Newer term 
                            vote = True
                        else:  # Current term
                            if _node != self.votedFor:  # different leader
                                vote = False  # vote no
                            else:  # same leader
                                vote = True  # vote yes
                    self.logger.info('... voting for leader %s for term %s with %s', _node.hex(), str(_term), str(vote))
                    rsp = struct.pack("!L16sL16s", _term, _node, int(vote), self.ownId)
                    self.pubPort.sendGroup(GroupThread.RSPVOTE, rsp)
                    self.term = _term
                    if self.leader != None: 
                        self.sendChangeMessage(Group.GROUP_LEX, self.leader)
                    self.leaderDeadline = None 
                    self.leader = None
                    self.qryPort.update(None, None)  # disconnect from previous leader (if at all)
                    if vote: self.votedFor = _node
                    self.setTimeout(self.electionTimeout(), now)
                elif cmd == GroupThread.RSPVOTE:  # Somebody's vote
                    self.setTimeout(self.electionTimeout(), now)  # ignore, keep waiting 
            elif self.state == GroupThread.CANDIDATE:  # Candidate is requested to vote
                if cmd == GroupThread.REQVOTE:
                    self.logger.info("... candidate requested to vote")
                    (_term, _node) = struct.unpack('!L16s', frame)
                    if _term == self.term:          # For current term
                        if _node != self.ownId:     # Another candidate -> vote no
                            rsp = struct.pack("!L16sL16s", _term, _node, int(False), self.ownId)    
                            self.pubPort.sendGroup(GroupThread.RSPVOTE, rsp)
                        else:
                            pass                    # We already 'voted' for ourselves
                    elif _term > self.term:  # For a future (next) term
                        self.state = GroupThread.FOLLOWER  # Go back to follower
                        # Vote yes        
                        rsp = struct.pack("!L16sL16s", _term, _node, int(True), self.ownId)
                        self.pubPort.sendGroup(GroupThread.RSPVOTE, rsp)
                        self.term = _term
                        if self.leader != None:
                            self.sendChangeMessage(Group.GROUP_LEX, self.leader)  # Leader exited
                        self.leader = None
                        self.qryPort.update(None, None)  # disconnect from previous leader (if at all)
                        self.votedFor = _node
                    else:  # For past term - ignore
                        pass
                    self.setTimeout(self.electionTimeout(), now)
                elif cmd == GroupThread.RSPVOTE:
                    self.logger.info("... candidate received vote")
                    (_term, _leader, _vote, _node) = struct.unpack("!L16sL16s", frame)
                    if bool(_vote) and _leader == self.ownId:  # it is a vote for us
                            self.votes += 1
                            if self.votes >= self.threshold():  # we won 
                                self.logger.info("... candidate won election")
                                self.state = GroupThread.LEADER    
                                self.leader = self.ownId
                                self.sendChangeMessage(Group.GROUP_LEL, self.leader)  # Tell ourselves that we are elected
                                self.ansPort.updatePoller(self.poller)  # Update ans socket/poller
                                self.ansSocket = self.ansPort.getSocket()
                                self.ldrPort = self.ansPort.getPortNumber()
                                msg = struct.pack('!L16sLL', self.term, self.ownId, \
                                                    int(self.host), \
                                                    int(self.ldrPort))
                                self.pubPort.sendGroup(GroupThread.AUTHORITY, msg)
                                self.setTimeout(self.groupHeartbeat, now)
                elif cmd == GroupThread.AUTHORITY:
                    self.logger.info("... candidate received message from leader")
                    (_term, _leader, _host, _port) = struct.unpack('!L16sLL', frame)
                    self.state = GroupThread.FOLLOWER  # we lost, go back to FOLLOWER
                    self.term = _term  # update term/leader
                    prevLeader = self.leader            
                    self.leader = _leader
                    if prevLeader != _leader:
                        self.sendChangeMessage(Group.GROUP_LEL, self.leader)               
                    self.votedFor = None  # clear last vote
                    _host = ipaddress.IPv4Address(_host).compressed
                    _port = int(_port)
                    self.qryPort.update(_host, _port)  # connect qry port to leader
                    self.setTimeout(self.electionTimeout(), now)  # set new election timeout
                    self.setLeaderDeadline()
            elif self.state == GroupThread.LEADER:  # leader received a  message
                self.logger.info("... leader received message")
                timeout = self.groupHeartbeat
                if cmd == GroupThread.REQVOTE:      # outstanding request
                    pass
                elif cmd == GroupThread.RSPVOTE:    # late vote
                    pass
                elif cmd == GroupThread.AUTHORITY:
                    (_term, _leader, _host, _port) = struct.unpack('!L16sLL', frame)
                    if self.term == _term and self.ownId != _leader: 
                        self.logger.error("GroupThread[%s].%r - leader conflict with %r", 
                                          self.group.getGroupName(),self.ownId.hex(),_leader.hex())
                        # Accept 'other' leader...
                        self.state = GroupThread.FOLLOWER   # we lost, go back to FOLLOWER
                        self.term = _term                   # update term/leader
                        prevLeader = self.leader            
                        self.leader = _leader
                        if prevLeader != _leader:
                            self.sendChangeMessage(Group.GROUP_LEL, self.leader)               
                        self.votedFor = None                # clear last vote
                        _host,_port = ipaddress.IPv4Address(_host).compressed, int(_port)
                        self.qryPort.update(_host, _port)   # connect qry port to leader
                        timeout = self.electionTimeout()    # set new election timeout
                        self.setLeaderDeadline()
                self.setTimeout(timeout, now)
        else:
            self.logger.error("GroupThread[%s] - not coordinated", self.group.getGroupName())
                        
    def startPoll(self, msg, member):
        '''
        Start a poll for a member based on message
        '''
        self.logger.info("GroupThread.startPoll()")
        with dc_capnp.GroupVote.from_bytes(msg) as rfv:
            which = rfv.which()
            if which == 'rfv':
                now = time.time()
                rfvId = rfv.rfv.rfvId
                started = rfv.rfv.started
                timeout = rfv.rfv.timeout
                if timeout == 0.0: timeout = self.groupConsensusTimeout
                delta = now - started
                if delta > timeout:  # We are past the timeout
                    return False
                deadline = started + timeout - delta  # Compensate for initial delay 
                poll = Poll(self, rfv.rfv, member, timeout, deadline, self.numPeers)
                self.polls[rfvId] = poll
                return True
            else:
                self.logger.error('GroupThread.startPoll(): invalid message type %s', str(which))
                return False
    
    def announceConsensus(self, rfvId, vote):
        '''
        Announce consensus vote result (yes/no/timeout)
        '''
        self.logger.info("GroupThread.announceConsensus()")
        msg = dc_capnp.GroupVote.new_message()
        ann = msg.init('ann')
        ann.rfvId = rfvId
        ann.vote = vote  # Result (yes/no)
        msgBytes = msg.to_bytes()              
        self.pubPort.sendGroup(Group.GROUP_ANN, msgBytes)  # Announce result
    
    def checkPoll(self, poll, now):
        '''
        Check the result of of one poll
        '''
        self.logger.info("GroupThread.checkPoll()")
        res = False
        if poll.expired(now):  # Poll has expired
            self.logger.info("... voting timeout")
            self.announceConsensus(poll.rfvId, 'timeout')       
            res = True        
        elif poll.allVoted():  # All voted
            self.logger.info("... all have voted")
            self.announceConsensus(poll.rfvId, 'yes' if poll.result() else 'no')
            res = True
        else:
            self.logger.info("... not all have voted: %d vs. %d", poll.voteCnt, poll.numPeers)
            pass
        return res
    
    def checkAllPolls(self, now):
        '''
        Check the results of all polls
        '''
        self.logger.info("GroupThread.checkPoll()")
        toRemove = []
        for p in self.polls:
            poll = self.polls[p]
            done = self.checkPoll(poll, now)
            if done: toRemove += [p]
        for r in toRemove:
            del self.polls[r]
        
    def updatePoll(self, msg):
        '''
        Update poll with the vote in msg
        '''
        self.logger.info("GroupThread.updatePoll()")
        with dc_capnp.GroupVote.from_bytes(msg) as rtc:
            which = rtc.which()
            if which == 'rtc':
                rfvId = rtc.rtc.rfvId
                if rfvId in self.polls:
                    poll = self.polls[rfvId] 
                    now = time.time()
                    vote = True if rtc.rtc.vote == 'yes' else False
                    poll.vote(vote)
                    done = self.checkPoll(poll, now)
                    if done:
                        del self.polls[rfvId]
                else:
                    self.logger.info("... rpfId is not in polls")
                    pass
            
    def handleMessageForLeader(self):
        '''
        Handle message sent to the leader (in leader)
        '''
        self.logger.info("GroupThread.handleMessageForLeader()")
        msgFrames = self.ansPort.recvFromMember()
        cmd = msgFrames[0]
        if cmd == Group.GROUP_MTL:  # Simple message to leader
            self.logger.info('...: simple message to leader')
            msg = msgFrames[1]  # Forward it to component
            msgOut = [zmq.Frame(Group.GROUP_MTL), zmq.Frame(msg)]    
            msgOut += [self.ansPort.get_identity()]
            if self.group.isTimed:
                self.recvTime = self.ansPort.recvTime()
                self.sendTime = self.ansPort.sendTime
                msgOut += [zmq.Frame(self.recvTime)]
                msgOut += [zmq.Frame(self.sendTime)]
            self.groupSocket.send_multipart(msgOut)
        elif cmd == Group.GROUP_RFV:  # Request for consensus message to leader
            self.logger.info('...: request for consensus message to leader')
            msg = msgFrames[1]     
            ok = self.startPoll(msg, self.ansPort.get_identity())  # Start the poll
            if (ok):
                self.pubPort.sendGroup(Group.GROUP_RCM, msg)  # Send RCM to group
            else: 
                with dc_capnp.GroupVote.from_bytes(msg) as rfv:  # Poll failed (before it got started)        
                    which = rfv.which()
                    assert(which == 'rfv')
                    rfvId = rfv.rfv.rfvId
                    self.announceConsensus(rfvId, 'timeout')
        elif cmd == Group.GROUP_RTC:  # Reply to consensus to leader
            self.logger.info('...: consensus vote to leader')
            msg = msgFrames[1]
            self.updatePoll(msg)
        else:
            self.logger.error("GroupThread.handleMessageForLeader() - unknown message type: %s", str(cmd))            
    
    def handleMessageForMember(self):
        '''
        Handle simple message from leader (in member)
        '''
        self.logger.info("GroupThread.handleMessageForMember()")
        msgFrames = self.qryPort.recvFromLeader()
        cmd = msgFrames[0]
        if cmd == Group.GROUP_MFL:
            msg = msgFrames[1]           
            msgOut = [zmq.Frame(Group.GROUP_MFL), zmq.Frame(msg)]
            if self.group.isTimed:
                self.recvTime = self.ansPort.recvTime()
                self.sendTime = self.ansPort.sendTime
                msgOut += [zmq.Frame(self.recvTime)]
                msgOut += [zmq.Frame(self.sendTime)]
            self.groupSocket.send_multipart(msgOut)

    def run(self):
        '''
        Main loop for GroupThread - polls all sources and calls handlers
        '''
        self.logger.info("GroupThread.run() [%s]" % self.group.getGroupName())
        self.setup()
        self.pubPort = self.group.pubPort
        self.pubSocket = self.pubPort.getSocket()
        self.subPort = self.group.subPort
        self.subSocket = self.subPort.getSocket()
        self.groupSocket = self.group.groupSocket
        if self.coordinated:
            self.qryPort = self.group.qryPort
            self.qrySocket = self.qryPort.getSocket()
            self.ansPort = self.group.ansPort
            self.ansSocket = self.ansPort.getSocket()
        else:
            self.qryPort = None
            self.qrySocket = None
            self.ansPort = None
            self.ansSocket = None
        self.poller = zmq.Poller()
        self.poller.register(self.groupSocket, zmq.POLLIN)
        self.poller.register(self.subSocket, zmq.POLLIN)
        if self.coordinated:
            self.poller.register(self.qrySocket, zmq.POLLIN)
            self.poller.register(self.ansSocket, zmq.POLLIN)
        
        if self.coordinated:
            # time.sleep(self.electionTimeout() / 1000.0)  # Initial random sleep
            self.state = GroupThread.FOLLOWER
            now = time.time()
            self.lastWait = now
            self.lastHeartbeat = 0
            self.heartbeat(now)
            self.timeout = self.groupHeartbeat
            self.leader = None
            self.setLeaderDeadline()
        else:
            self.timeout = None 
            now = None
            
        toStop = False
        while True:
            events = self.poller.poll(self.timeout)
            # self.logger.info("GroupThread.runGroup() - polled")
            if self.coordinated:
                now = time.time()
                self.heartbeat(now)
                self.updatePeers(now)                           # Check if there is a change in peers 
            if len(events) == 0 and self.coordinated:
                self.handleTimeout(now)
            else:
                sockets = dict(events)
                if self.groupSocket in sockets:  # Message from component
                    toStop = self.handleCompMessage()
                    # del sockets[self.groupSocket]
                if self.subSocket in sockets:  # Group message: data, heartbeat, leader, or election messages    
                    self.handleNetMessage(now)
                    # del sockets[self.subSocket]
                if self.coordinated:
                    if self.ansSocket in sockets:  # Message to leader
                        self.handleMessageForLeader()
                        # del sockets[self.ansSocket]
                    if self.qrySocket in sockets:  # Message from leader
                        self.handleMessageForMember()
                        # del sockets[self.qrySocket]
            if toStop: break
        self.done = False
        self.group.unsetup(self)


class Group(object):
    '''
    Group object, represents one group instance that belongs to a component. 
    Acts as the front-end for the GroupThread, channels messages to/from.
    Some of its methods are run in the GroupThread
    '''
    GROUP_ACK = 'ack'.encode('utf-8')  # Response: Acknowledge 
    GROUP_ERR = 'err'.encode('utf-8')  # Response: Error  
    GROUP_NLD = 'nld'.encode('utf-8')  # Response: No leader
    GROUP_MSG = 'msg'.encode('utf-8')  # Message to group
    GROUP_UPD = 'upd'.encode('utf-8')  # Update for port from disco
    GROUP_MTL = 'mtl'.encode('utf-8')  # Message to leader
    GROUP_MFL = 'mfl'.encode('utf-8')  # Message from leader
    GROUP_RFV = 'rfv'.encode('utf-8')  # Request for consensus (from member to leader)
    GROUP_RCM = 'rcm'.encode('utf-8')  # Request consensus from member (by leader)
    GROUP_RTC = 'rtc'.encode('utf-8')  # Reply to consensus request
    GROUP_ANN = 'ann'.encode('utf-8')  # Announce consensus result
    GROUP_MJD = 'mjd'.encode('utf-8')  # Group member joined
    GROUP_MLT = 'mlt'.encode('utf-8')  # Group member left
    GROUP_LEL = 'lel'.encode('utf-8')  # Group leader elected
    GROUP_LEX = 'lex'.encode('utf-8')  # Group leader exited
    
    def __init__(self, parent, thread, groupType, groupInstance, componentId, groupSpec, groupSize):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.thread = thread
        self.context = thread.context
        self.groupType = groupType
        self.groupInstance = groupInstance
        self.componentId = componentId
        self.groupSpec = groupSpec
        self.groupInstanceName = groupType + '.' + groupInstance
        self.messageType = self.groupSpec['message']
        self.isTimed = self.groupSpec['timed']
        self.kind = self.groupSpec['kind']
        self.coordinated = False if self.kind == "default" else True
        self.groupSize = groupSize
        self.setupParams()
        # PAIR socket for the component poller
        self.compSocket = self.context.socket(zmq.PAIR)
        self.compSocket.bind('inproc://%s' % self.groupSocketName(self.groupType, self.groupInstance, self.componentId))
        # Message queue for group messages
        self.msgQueue = collections.deque()
        # Group thread
        self.groupThread = GroupThread(self)  # Create the worker thread 
        self.done = False
        self.groupThread.start()
        while not self.done: time.sleep(0.1)  # Allow groupThread to create sockets
        # send a message to disco to register new group
        assert(self.pubInfo.portKind == 'gpub')
        assert(self.subInfo.portKind == 'gsub')
        host, pubPort = self.pubInfo.portHost, self.pubInfo.portNum
        comp = self.parent.parent
        partName = comp.getName()
        partType = comp.getTypeName()
        portName = self.groupInstanceName
        # ???
        msg = ('group', self.groupType, self.groupInstance, self.messageType, host, pubPort, partName, partType, portName) 
        self.thread.sendControl(msg)
        time.sleep(1.0)  # 
    
    GROUP_PARAMETERS = {'heartbeat' : const.groupHeartbeat, 
                        'electionMin' : const.groupElectionMin,
                        'electionMax' : const.groupElectionMax,
                        'peerTimeout' : const.groupPeerTimeout,
                        'consensusTimeout' : const.groupConsensusTimeout 
                        }
    
    def setupParams(self):
        modelParams = self.groupSpec["params"]
        for (name,value) in Group.GROUP_PARAMETERS.items():
            result = modelParams.get(name,None) or value
            assert result > 0, "Group parameter %s must be >0 " % name
            setattr(self,name,result)
        assert self.heartbeat < self.electionMin and \
                self.electionMin < self.electionMax and \
                self.electionMax < self.peerTimeout and \
                self.consensusTimeout < self.electionMax, \
                "Group timing parameter(s) incorrectly ordered"   
                    
    def leave(self):
        self.logger.info("Group.leave(): %s" % self.groupInstanceName)
        # 
        comp = self.parent.parent
        partName = comp.getName()
        partType = comp.getTypeName()
        portName = self.groupInstanceName
        host, pubPort = self.pubInfo.portHost, self.pubInfo.portNum
        comp = self.parent.parent
        msg = ('ungroup', self.groupType, self.groupInstance, self.messageType, host, pubPort, partName, partType, portName) 
        self.thread.sendControl(msg)
        
        msgFrames = [zmq.Frame(Group.GROUP_MLT)]    # Send out message the component is leaving group
        self.compSocket.send_multipart(msgFrames)
        self.groupThread.join()

        self.compSocket.close()
    
    def getGroupName(self):
        '''
        Group unique name
        '''
        return self.groupInstanceName 
    
    def getSocket(self):
        '''
        Returns inproc socket used to communicate with GroupThread 
        '''
        return self.compSocket
    
    def groupSocketName(self, groupType, groupName, componentId):
        '''
        Forms the unique name for the inproc socket. 
        '''
        return "group-%s.%s.%s" % (groupType, groupName, str(componentId))

    def setup(self, groupThread):
        '''
        Set up all the sockets for the worker thread
        Runs in group thread
        '''
        self.pubPort = GroupPubPort(self.parent.parent.owner, self.groupInstanceName + '_pub', self.groupSpec)
        self.pubInfo = self.pubPort.setupSocket(groupThread)
        self.subPort = GroupSubPort(self.parent.parent.owner, self.groupInstanceName + '_sub', self.groupSpec)
        self.subInfo = self.subPort.setupSocket(groupThread) 
        if self.coordinated: 
            self.qryPort = GroupQryPort(self.parent.parent.owner, self.groupInstanceName + '_qry', self.groupSpec)
            self.qryInfo = self.qryPort.setupSocket(groupThread)
            self.ansPort = GroupAnsPort(self.parent.parent.owner, self.groupInstanceName + '_ans', self.groupSpec)
            self.ansInfo = self.ansPort.setupSocket(groupThread)
        else:
            self.qryPort = None 
            self.qryInfo = None
            self.ansPort = None
            self.ansInfo = None 
        self.groupSocket = self.context.socket(zmq.PAIR)
        self.groupSocket.connect('inproc://%s' % self.groupSocketName(self.groupType, self.groupInstance, self.componentId))
        self.done = True
    
    def unsetup(self,groupThread):
        '''
        Discard all the sockets used in worker thread
        Runs in group thread
        '''
        self.pubPort.closeSocket()
        self.subPort.closeSocket()
        if self.coordinated:
            self.qryPort.closeSocket()
            self.ansPort.closeSocket()
        self.groupSocket.close()
        
    def update(self, host, port):
        '''
        Ask the worker thread to update its sockets.
        Called when the disco responds with the server (pub) host/port pair for the socket(s)
        to connect to by the client (sub) 
        Runs in component thread
        '''
        self.logger.info("Group.update(%s,%d)" % (host, port))
        msgFrames = [zmq.Frame(Group.GROUP_UPD), zmq.Frame(host.encode('utf-8')), zmq.Frame(struct.pack("d", port))]
        self.compSocket.send_multipart(msgFrames)
    
    def send_port(self, msgType, msg, has_identity=False):
        '''
        Send a message to the worker thread.
        Used by all messages - the messages have multiple frames
        Runs in component thread 
        '''
        msgFrames = [zmq.Frame(msgType)]  # Frame 0: message type
        msgFrames += [zmq.Frame(msg)]  # Frame 1: payload                
        if has_identity:
            assert (self.identity != None)
            msgFrames += [self.identity]  # Frame 2: identity (opt)      
        self.compSocket.send_multipart(msgFrames)  # Receive a response from worker thread
        while(True):
            repFrames = self.compSocket.recv_multipart()
            res = repFrames[0]
            if res == Group.GROUP_ACK:  # Msg ack-d
                return True
            elif res == Group.GROUP_NLD:  # No leader(caller should handle it)
                return False
            elif res == Group.GROUP_ERR:  # Error detected
                err = pickle.loads(repFrames[1])
                raise PortError("send error: %s" % msg, err.__repr__(), err.errno)
            else:  # Group MSG, MTL, MFL, etc. 
                self.handleMessage(repFrames)  # Handle it as normal message

    def send_pyobj(self, msg):
        '''
        Sends a Python object as a message to all members of the group
        Runs in component thread
        '''
        msgBytes = pickle.dumps(msg)
        return self.send_port(Group.GROUP_MSG, msgBytes)

    def send(self, msg):
        '''
        Sends a bytes object as a message to all members of the group
        Runs in component thread
        '''
        assert(type(msg) == bytes)
        return self.send_port(Group.GROUP_MSG, msg)
    
    def handleMessage(self, msgFrames=None):
        '''
        Receives message from the worker thread and handles it
        Runs in component thread (called from component polling loop, or from send_port)
        '''
        try:
            if msgFrames == None:  # No frames (called from send_port)
                msgFrames = self.compSocket.recv_multipart()  # Receive message
            cmd = msgFrames[0]
            self.logger.info("Group.handleMessage() = %s", str(cmd))
            if cmd == Group.GROUP_MSG:  # Data message from a group member
                msg = msgFrames[1]
                self.msgQueue.append(msg)  # Add payload to queue to be read by recv/recv_pyobj
                if self.isTimed:  # If group is timed, store values
                    self.recvTime = msgFrames[2]
                    self.sendTime = msgFrames[3]
                self.parent.parent.handleGroupMessage(self)  # Call group message handler
            elif cmd == Group.GROUP_MTL:  # Message to leader
                msg = msgFrames[1]
                self.identity = msgFrames[2]  # Save sender's identity
                self.msgQueue.append(msg)  # Add payload to queue to be read by recv/recv_pyobj
                if self.isTimed:  # If group is timed, store values
                    self.recvTime = msgFrames[3]
                    self.sendTime = msgFrames[4]
                self.parent.parent.handleMessageToLeader(self)  # Call leader's message handler
            elif cmd == Group.GROUP_MFL:  # Message from leader to the member
                msg = msgFrames[1]
                self.msgQueue.append(msg)  # Add payload to queue to be read by recv/recv_pyobj
                if self.isTimed:  # If group is timed, store values
                    self.recvTime = msgFrames[2]
                    self.sendTime = msgFrames[3]
                self.parent.parent.handleMessageFromLeader(self)  # Call member's message handler
            elif cmd == Group.GROUP_RCM:
                msg = msgFrames[1]
                if self.isTimed:  # If group is timed, store values
                    self.recvTime = msgFrames[2]
                    self.sendTime = msgFrames[3]
                with dc_capnp.GroupVote.from_bytes(msg) as rfv:
                    which = rfv.which()
                    if which == 'rfv':
                        topic = rfv.rfv.topic
                        rfvId = rfv.rfv.rfvId
                        subject = rfv.rfv.subject
                        self.msgQueue.append(topic)
                        if subject == Poll.ACTION:  # Call member's appropriate message handler
                            when = rfv.rfv.release
                            self.parent.parent.handleActionVoteRequest(self, rfvId, when)    
                        elif subject == Poll.VALUE:
                            self.parent.parent.handleVoteRequest(self, rfvId)
                        else:
                            self.logger.error("handleMessage() - unknown poll subject %s", str(subject))
            elif cmd == Group.GROUP_ANN:
                msg = msgFrames[1]
                if self.isTimed:  # If group is timed, store values
                    self.recvTime = msgFrames[2]
                    self.sendTime = msgFrames[3]
                with dc_capnp.GroupVote.from_bytes(msg) as ann:
                    which = ann.which()
                    if which == 'ann':
                        rfvId = ann.ann.rfvId
                        vote = ann.ann.vote
                        self.parent.parent.handleVoteResult(self, rfvId, vote)  # Call member's message handler
            elif cmd == Group.GROUP_MJD:
                memberId = msgFrames[1]
                self.parent.parent.handleMemberJoined(self, memberId)
            elif cmd == Group.GROUP_MLT:
                memberId = msgFrames[1]
                self.parent.parent.handleMemberLeft(self, memberId)
            elif cmd == Group.GROUP_LEL:
                leaderId = msgFrames[1]
                self.parent.parent.handleLeaderElected(self, leaderId)
            elif cmd == Group.GROUP_LEX:
                leaderId = msgFrames[1]
                self.parent.parent.handleLeaderExited(self, leaderId)
            else:
                self.logger.error("handleMessage() - unknown control message %s", str(cmd))
        except zmq.error.ZMQError as e:
            raise PortError("recv error: %s" % e.__repr__(), e.errno) from e
    
    def recv_msg(self, is_pyobj):
        '''
        Receive a message from the worker thread.
        Message are coming through a message queue.
        Runs in component thread, called from a component
        '''
        if len(self.msgQueue) == 0:
            errno = zmq.EFAULT
            raise PortError("recv error (%d)" % errno, errno)
        else:
            msg = self.msgQueue.popleft()
            if is_pyobj:
                result = pickle.loads(msg)
            else:
                result = msg
            return result
            
    def recv_pyobj(self):
        '''
        Receive a Python object message from the worker thread
        Runs in component thread, called from a component
        '''
        return self.recv_msg(True)
    
    def recv(self):
        '''
        Receive a bytes object message from the worker thread
        Runs in component thread, called from a component
        '''
        return self.recv_msg(False)
    
    def sendToLeader(self, msg):
        '''
        Send message to group leader from a member
        Raise an exception if the group is not coordinated
        Return False (indicating operation failure) if no leader 
        Runs in component thread. 
        ''' 
        if not self.groupThread.coordinated:
            raise PortError("sendToLeader error: group is not coordinated")
        if self.groupThread.leader:
            assert(type(msg) == bytes)
            return self.send_port(Group.GROUP_MTL, msg)
        else:
            return False

    def sendToLeader_pyobj(self, msg):
        '''
        Send PyObject message to group leader from a member
        Raise an exception if the group is not coordinated
        Return False (indicating operation failure) if no leader 
        Runs in component thread. 
        ''' 
        if not self.groupThread.coordinated:
            raise PortError("sendToLeader error: group is not coordinated")
        if self.groupThread.leader:
            msgOut = pickle.dumps(msg)             
            return self.send_port(Group.GROUP_MTL, msgOut)
        else:
            return False
    
    def sendToMember_pyobj(self, msg, identity=None):
        '''
        Send PyObject message to group member (with identity) from the leader
        If identity is not supplied, last value of identity is used. 
        Raise an exception if the group is not coordinated
        Return False (indicating operation failure) if no leader 
        Runs in component thread. 
        ''' 
        if not self.groupThread.coordinated:
            raise PortError("sendToLeader error: group is not coordinated")
        if self.groupThread.leader:
            if identity != None:
                self.identity = identity
            assert(self.identity != None)
            msgOut = pickle.dumps(msg) 
            return self.send_port(Group.GROUP_MFL, msgOut, True)
        else:
            return False
    
    def sendToMember(self, msg, identity=None):
        '''
        Send message to group member (with identity) from the leader
        If identity is not supplied, last value of identity is used. 
        Raise an exception if the group is not coordinated
        Return False (indicating operation failure) if no leader 
        Runs in component thread. 
        ''' 
        if not self.groupThread.coordinated:
            raise PortError("sendToLeader error: group is not coordinated")
        if self.groupThread.leader:
            if identity != None:
                self.identity = identity
            assert(self.identity != None)
            assert(type(msg) == bytes) 
            return self.send_port(Group.GROUP_MFL, msg, True)
        else:
            return False
    
    def hasLeader(self):
        '''
        True if the group has a leader.
        '''
        return self.groupThread.leader != None
    
    def getLeaderId(self):
        '''
        Return the leader's id (or None if no leader)
        '''
        return self.groupThread.leader
        
    def isLeader(self):
        '''
        Return True if the group member IS the leader.
        '''
        return self.groupThread.isLeader()
    
    def groupSize(self):
        '''
        Return the size of the group (>= 1).  
        '''
        return self.groupThread.numPeers 
    
    def getGroupId(self):
        return self.groupThread.ownId
    
    def requestVote(self, topic, kind=Poll.MAJORITY, timeout=None):
        '''
        Request a vote on a topic (with timeout). Topic is a bytes.
        A message is sent to the leader (if any) that starts a voting process.
        Returns None if there is no leader, otherwise a generated id string for the request.  
        '''
        if not self.groupThread.coordinated:
            raise PortError("requestVote error: group is not coordinated")
        if self.groupThread.leader:
            assert(type(topic) == bytes)
            assert(timeout == None or type(timeout) == float) 
            rfvId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            msg = dc_capnp.GroupVote.new_message()
            rfv = msg.init('rfv')
            rfv.topic = topic
            rfv.rfvId = rfvId
            rfv.kind = kind
            rfv.subject = 'value'
            rfv.started = time.time()
            rfv.timeout = 0.0 if timeout == None else timeout / 1000.0 
            msgBytes = msg.to_bytes()              
            res = self.send_port(Group.GROUP_RFV, msgBytes)
            return rfvId if res == True else None
        else:
            return None
    
    def requestVote_pyobj(self, topic, kind=Poll.MAJORITY, timeout=None):
        '''
        Request a vote on a topic (with timeout). Topic is a Python object.
        A message is sent to the leader (if any) that starts a voting process.
        Returns None if there is no leader, otherwise a generated id string for the request.  
        '''
        if not self.groupThread.coordinated:
            raise PortError("requestVote_pyobj error: group is not coordinated")
        if self.groupThread.leader:
            assert(timeout == None or type(timeout) == float)
            topicOut = pickle.dumps(topic) 
            rfvId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            msg = dc_capnp.GroupVote.new_message()
            rfv = msg.init('rfv')
            rfv.topic = topicOut
            rfv.rfvId = rfvId
            rfv.kind = kind
            rfv.subject = 'value'
            rfv.started = time.time()
            rfv.timeout = 0.0 if timeout == None else timeout / 1000.0 
            msgBytes = msg.to_bytes()  
            res = self.send_port(Group.GROUP_RFV, msgBytes)
            return rfvId if res == True else False
        else:
            return False
        
    def sendVote(self, rfvId, vote):
        '''
        Send a vote (True/False) to the leader on a requested topic identified by the id of the request for vote. 
        '''
        # Send a True/False vote on the topic (identified by rfvId) to the leader 
        if not self.groupThread.coordinated:
            raise PortError("sendVote() error: group is not coordinated")
        msg = dc_capnp.GroupVote.new_message()
        rtc = msg.init('rtc')
        rtc.rfvId = rfvId
        rtc.vote = 'yes' if vote == True else 'no'   
        msgBytes = msg.to_bytes()  
        res = self.send_port(Group.GROUP_RTC, msgBytes)
        return res == True
    
    def requestActionVote(self, action, when, kind=Poll.CONSENSUS, timeout=None):
        # Send a request for a vote on an action to be taken in the future
        if not self.groupThread.coordinated:
            raise PortError("requestActionVote error: group is not coordinated")
        if self.groupThread.leader:
            assert(type(action) == bytes)
            assert(type(when) == float)
            assert(timeout == None or type(timeout) == float) 
            rfvId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            msg = dc_capnp.GroupVote.new_message()
            rfv = msg.init('rfv')
            rfv.topic = action
            rfv.rfvId = rfvId
            rfv.kind = kind
            rfv.subject = 'action'
            rfv.release = when
            rfv.started = time.time()
            rfv.timeout = 0.0 if timeout == None else timeout / 1000.0 
            msgBytes = msg.to_bytes()              
            res = self.send_port(Group.GROUP_RFV, msgBytes)
            return rfvId if res == True else None
        else:
            return None
        
    def requestActionVote_pyobj(self, action, when, kind=Poll.CONSENSUS, timeout=None):
        # Send a request for a vote on an action to be taken in the future
        if not self.groupThread.coordinated:
            raise PortError("requestActionVote error: group is not coordinated")
        if self.groupThread.leader:
            actionOut = pickle.dumps(action) 
            assert(type(when) == float)
            assert(timeout == None or type(timeout) == float) 
            rfvId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            msg = dc_capnp.GroupVote.new_message()
            rfv = msg.init('rfv')
            rfv.topic = actionOut
            rfv.rfvId = rfvId
            rfv.kind = kind
            rfv.subject = 'action'
            rfv.release = when
            rfv.started = time.time()
            rfv.timeout = 0.0 if timeout == None else timeout / 1000.0 
            msgBytes = msg.to_bytes()              
            res = self.send_port(Group.GROUP_RFV, msgBytes)
            return rfvId if res == True else None
        else:
            return None
        
    def sendActionVote(self, rfvId, vote):
        # Send a True/False vote on the action (identified by rfvId) to the leader 
        pass

    
class Coordinator(object):
    '''
    Coordinator object.
    Each component has a coordinator object that creates the group objects for a component.
    A group instance can be created only once in a component, subsequent creations
    return the same group object 
    '''

    def __init__(self, parent):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.context = None
        self.groupTypes = self.parent.owner.parent.groupTypes
        self.groupMembers = { } 
        self.groups = { }

    def groupName(self, groupType, groupInstance):
        '''
        Form a name for a group instance
        '''
        return groupType + '.' + groupInstance
    
    def joinGroup(self, thread, groupType, groupInstance, componentId, groupSize):
        '''
        Operation to create a group instance in a component.
        Returns the instance
        '''
        self.logger.info("Coordinator.joinGroup(%s,%s)" % (groupType, groupInstance))
        # In component thread
        if not groupInstance.isidentifier():
            self.logger.error("Coordinator.joinGroup: invalid group name %s", groupInstance)
            return None
        if groupType not in self.groupTypes:
            self.logger.error("Coordinator.joinGroup: group %s undefined", groupType)
            return None
        else:
            groupSpec = self.groupTypes[groupType]
        key = self.groupName(groupType, groupInstance)
        res = None
        if key in self.groupMembers:
            res = self.groupMembers[key]
        else:
            res = Group(self, thread, groupType, groupInstance, componentId, groupSpec, groupSize)
            self.groupMembers[key] = res
        return res
    
    def getGroup(self, groupType, groupInstance):
        '''
        Returns a group instance based on its name
        '''
        key = self.groupName(groupType, groupInstance)
        return self.groupMembers[key] if key in self.groupMembers else None

    def leaveGroup(self, group):
        '''
        Operation to 'leave' a group by a component. 
        The group will be deactivated / its threads stopped, and deleted.. 
        '''
        groupName = group.getGroupName()
        self.logger.info("Coordinator.leaveGroup(%s)" % groupName)
        group.leave()
        del self.groupMembers[groupName]
        del group
        
    
