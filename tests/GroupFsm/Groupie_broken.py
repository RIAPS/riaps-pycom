# import riaps
from riaps.run.comp import Component
from riaps.run.dc import Poll
import logging
import time
import random

groups = {"F123": ["1", "2", "3", "4", "5", "6", "7", "8"],
          "F12": ["1", "2", "3", "4", "5"],
          "F13": ["1", "2", "3", "6", "7", "8"],
          "F23": ["4", "5", "6", "7", "8"],
          "F1": ["1", "2", "3"],
          "F2": ["4", "5"],
          "F3": ["6", "7", "8"]
          }

formation_sequence = {
    0: ["F123"],
    1: ["F1", "F2", "F3"],
    2: ["F12", "F3"],
    3: ["F123"],
    4: ["F12", "F3"],
    5: ["F1", "F2", "F3"]
}


class Groupie(Component):
    """
    """

    def __init__(self, uid):
        super().__init__()
        self.name = uid
        self.formation_number = 0
        self.current_group = None
        self.activated = False

    def update_group(self):
        if self.current_group:
            self.leaveGroup(self.current_group)
            self.formation_number += 1
        next_formation = formation_sequence[self.formation_number]
        for group in next_formation:
            if self.name in groups[group]:
                next_group = group
                self.current_group = self.joinGroup("TheGroup", f"g_{next_group}")
                self.logger.info(f"joined group[{self.current_group.getGroupName()}]: {str(self.current_group.getGroupId())}")
                return

    def on_clock(self):
        now = self.clock.recv_pyobj()  # Receive time.time() as float
        self.logger.info(f"node name: {self.name} on_clock: {now}")
        if self.activated and not self.current_group:
            self.update_group()
        if self.current_group:
            self.logger.info(f"Has leader? {self.current_group.hasLeader()}")

    def handleActivate(self):
        self.activated = True
        # self.update_group()

    def handleGroupMessage(self, group):
        msg = group.recv_pyobj()
        self.logger.info('handleGroupMessage() by %s recv = %s' % (self.name, str(msg)))

    def handleMessageToLeader(self, group):
        msg = group.recv_pyobj()
        identity = group.identity
        self.logger.info(
            'handleMessageToLeader() %s:%s of %s = # %s #' % (self.name, str(identity), group.getGroupName(), str(msg)))
        rsp = "to member from leader of %s = %s" % (group.getGroupName(), msg[::-1])
        group.sendToMember_pyobj(rsp, identity)

    def handleMessageFromLeader(self, group):
        msg = group.recv_pyobj()
        rsp = "from leader of %s to member %s = # %s #" % (group.getGroupName(), self.name, msg[::-1])
        self.logger.info('handleMessageFromLeader()  %s' % rsp)

    def handleVoteRequest(self, group, rfcId):
        msg = group.recv_pyobj()
        vote = True
        self.logger.info('handleVoteRequest[%s] = %s -->  %s' % (str(rfcId), str(msg), str(vote)))
        group.sendVote(rfcId, vote)

    def handleActionVoteRequest(self, group, rfcId, when):
        msg = group.recv_pyobj()
        vote = True
        self.logger.info('handleActionVoteRequest[%s] = %s @ %s -->  %s' % (str(rfcId), str(msg), str(when), str(vote)))
        group.sendVote(rfcId, vote)

    def handleVoteResult(self, group, rfcId, vote):
        self.logger.info('handleVoteResult[%s] = %s ' % (str(rfcId), str(vote)))

    def handleMemberJoined(self, group, memberId):
        self.logger.info('handleMemberJoined[%s]: %s' % (group.getGroupName(), str(memberId)))

    def handleMemberLeft(self, group, memberId):
        self.logger.info('handleMemberLeft[%s]: %s' % (group.getGroupName(), str(memberId)))

    def handleLeaderElected(self, group, leaderId):
        self.logger.info('handleLeaderElected[%s]: %s' % (group.getGroupName(), str(leaderId)))

    def handleLeaderExited(self, group, leaderId):
        self.logger.info('handleLeaderExited[%s]: %s' % (group.getGroupName(), str(leaderId)))
