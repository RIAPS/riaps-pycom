# import riaps
from riaps.run.comp import Component
from riaps.run.dc import Poll
import logging
import time
import random


class Groupie(Component):
    """
    :param gs: string containing 1 character group names
    :param tl: string containing the selection of tests:
                c = clock logging
                m = group message
                l = message to leader
                v = vote for value consensus
                t = vote for action consensus
                d = leave and the rejoin group
    """

    def __init__(self, uid):
        super(Groupie, self).__init__()
        self.name = uid
        self.groups = []
        
    def on_clock(self):
        now = self.clock.recv_pyobj()       # Receive time.time() as float
        self.logger.info('on_clock(): %s' % str(now))

    def handleActivate(self):

        group = self.joinGroup("TheGroup", "g_%s" % "testGroup")
        self.groups += [group]
        self.logger.info("joined group[%s]: %s" % (group.getGroupName(),str(group.getGroupId())))

    def handleGroupMessage(self,group):
        assert (group in self.groups)
        msg = group.recv_pyobj()
        self.logger.info('handleGroupMessage() by %s recv = %s' % (self.name,str(msg)))
        
    def handleMessageToLeader(self,group):
        assert (group in self.groups)
        msg = group.recv_pyobj()
        identity = group.identity
        self.logger.info('handleMessageToLeader() %s:%s of %s = # %s #' % (self.name,str(identity),group.getGroupName(),str(msg)))
        rsp = "to member from leader of %s = %s" % (group.getGroupName(),msg[::-1])
        group.sendToMember_pyobj(rsp,identity)
        
    def handleMessageFromLeader(self,group):
        assert (group in self.groups)
        msg = group.recv_pyobj()
        rsp = "from leader of %s to member %s = # %s #" % (group.getGroupName(),self.name,msg[::-1])
        self.logger.info('handleMessageFromLeader()  %s' % rsp)
        
    def handleVoteRequest(self,group,rfcId):
        assert (group in self.groups)
        msg = group.recv_pyobj()
        vote = random.uniform(0,1) > 0.51        
        self.logger.info('handleVoteRequest[%s] = %s -->  %s' % (str(rfcId),str(msg), str(vote)))
        group.sendVote(rfcId,vote)
            
    def handleActionVoteRequest(self,group,rfcId,when):
        assert (group in self.groups)
        msg = group.recv_pyobj()
        vote = random.uniform(0,1) > 0.51        
        self.logger.info('handleActionVoteRequest[%s] = %s @ %s -->  %s' % (str(rfcId),str(msg),str(when),str(vote)))
        group.sendVote(rfcId,vote)
        
    def handleVoteResult(self,group,rfcId,vote):
        assert (group in self.groups)
        self.logger.info('handleVoteResult[%s] = %s ' % (str(rfcId),str(vote)))

    def handleMemberJoined(self,group,memberId):
        assert (group in self.groups)
        self.logger.info('handleMemberJoined[%s]: %s' % (group.getGroupName(),str(memberId)))
    
    def handleMemberLeft(self,group,memberId):
        assert (group in self.groups)
        self.logger.info('handleMemberLeft[%s]: %s' % (group.getGroupName(),str(memberId)))
    
    def handleLeaderElected(self,group,leaderId):
        assert (group in self.groups)
        self.logger.info('handleLeaderElected[%s]: %s' % (group.getGroupName(),str(leaderId)))
    
    def handleLeaderExited(self,group,leaderId):
        assert (group in self.groups)
        self.logger.info('handleLeaderExited[%s]: %s' % (group.getGroupName(),str(leaderId)))
        
        
        