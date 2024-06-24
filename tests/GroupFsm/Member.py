# import riaps
from riaps.run.comp import Component
from riaps.run.dc import Poll
import logging
import time
import random

groups = {"E": ["Ext"], "g1": ["1", "2", "3"], "Eg1": ["E", "1", "2", "3"]}

formation_seq = {0: ["Eg1"], 1: ["E", "g1"]}


class Member(Component):
    """ """

    def __init__(self, uid):
        super().__init__()
        self.name = uid
        self.formation_number = 0
        self.current_group = None
        self.activated = False
        self.group_id = None
        self.round_without_leader = 0
        self.round_limit = 20

    def update_group(self):
        if self.current_group:
            group_name = self.current_group.getGroupName()
            self.logger.info(f"Node: {self.name} leave group: {group_name}")
            self.leaveGroup(self.current_group)
            self.formation_number += 1
        next_formation = formation_seq[self.formation_number % len(formation_seq)]
        for group in next_formation:
            if self.name in groups[group]:
                next_group = group
                self.current_group = self.joinGroup("TheGroup", f"g_{next_group}")
                group_name = self.current_group.getGroupName()
                self.own_grp_id = self.current_group.getGroupId()
                self.logger.info(f"Node: {self.name} joined group {group_name}")
                return

    def on_clock(self):
        now = self.clock.recv_pyobj()  # Receive time.time() as float
        if self.activated and not self.current_group:
            self.update_group()
        if self.current_group:
            self.logger.info(f"Group size: {self.current_group.groupSize()}")
            if self.current_group.hasLeader():
                self.round_without_leader = 0
                self.update_group()
            else:
                self.round_without_leader += 1

                self.logger.info(
                    f"Node: {self.name} Group: {self.current_group.getGroupName()} Leader: {self.current_group.hasLeader()} Round: {self.round_without_leader}"
                )
                # seconds_to_timeout = self.current_group.groupThread.timeout
                # # self.logger.info(f"Time until next timeout: {seconds_to_timeout}")
                # # if seconds_to_timeout <= 1000:
                # if self.round_without_leader >= self.round_limit:
                #     self.round_without_leader = 0
                #     old_election_min = self.current_group.electionMin
                #     old_election_max = self.current_group.electionMax
                #     old_peer_timeout = self.current_group.peerTimeout
                #     election_min = old_election_min + 5000
                #     election_max = old_election_max + 5000
                #     peer_timeout = old_peer_timeout + 5000
                #     self.current_group.electionMin = election_min
                #     self.current_group.electionMax = election_max
                #     self.current_group.peerTimeout = peer_timeout
                #     self.logger.info(
                #         f"Increase election timeout"
                #         f"from [{old_election_min}:{old_election_max}]"
                #         f"to [{election_min}:{election_max}]"
                #     )

    def handleActivate(self):
        self.activated = True

    def handleGroupMessage(self, group):
        msg = group.recv_pyobj()
        self.logger.info("handleGroupMessage() by %s recv = %s" % (self.name, str(msg)))

    def handleMessageToLeader(self, group):
        msg = group.recv_pyobj()
        identity = group.identity
        self.logger.info(
            "handleMessageToLeader() %s:%s of %s = # %s #"
            % (self.name, str(identity), group.getGroupName(), str(msg))
        )
        rsp = "to member from leader of %s = %s" % (group.getGroupName(), msg[::-1])
        group.sendToMember_pyobj(rsp, identity)

    def handleMessageFromLeader(self, group):
        msg = group.recv_pyobj()
        rsp = "from leader of %s to member %s = # %s #" % (
            group.getGroupName(),
            self.name,
            msg[::-1],
        )
        self.logger.info("handleMessageFromLeader()  %s" % rsp)

    def handleVoteRequest(self, group, rfcId):
        msg = group.recv_pyobj()
        vote = True
        self.logger.info(
            "handleVoteRequest[%s] = %s -->  %s" % (str(rfcId), str(msg), str(vote))
        )
        group.sendVote(rfcId, vote)

    def handleActionVoteRequest(self, group, rfcId, when):
        msg = group.recv_pyobj()
        vote = True
        self.logger.info(
            "handleActionVoteRequest[%s] = %s @ %s -->  %s"
            % (str(rfcId), str(msg), str(when), str(vote))
        )
        group.sendVote(rfcId, vote)

    def handleVoteResult(self, group, rfcId, vote):
        self.logger.info("handleVoteResult[%s] = %s " % (str(rfcId), str(vote)))

    def handleMemberJoined(self, group, memberId):
        if memberId == self.own_grp_id:
            pass
        else:
            self.logger.info(
                f"handleMemberJoined[{group.getGroupName()}]: memberId: {memberId}"
            )

    def handleMemberLeft(self, group, memberId):
        self.logger.info(
            "handleMemberLeft[%s]: %s" % (group.getGroupName(), str(memberId))
        )

    def handleLeaderElected(self, group, leaderId):
        self.logger.info(
            f"handleLeaderElected: {group.getGroupName()} Leader: {str(leaderId)}"
        )

    def handleLeaderExited(self, group, leaderId):
        self.logger.info(
            "handleLeaderExited[%s]: %s" % (group.getGroupName(), str(leaderId))
        )
