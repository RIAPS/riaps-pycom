# 
# FSM Example
# 

from riaps.run.fsm import FSM
from enum import Enum, auto
import logging
import time

class Player(FSM):
    '''
    Ping-poing player class
    '''
    class states(Enum):
        '''
        States of a player: initial, has_ball, no_ball
        '''
        initial = auto()
        has_ball = auto()
        no_ball = auto()
    
    class events(Enum):
        '''
        Triggering events for the player: tick, catch
        Names must match the names of ports (timer or input) where the trigger is coming from.
        '''
        tick = auto()
        catch = auto()
    
    def __init__(self,who,ball):
        '''
        Arguments carry the identity string (who) and whether has the ball or not (ball) 
        '''
        FSM.__init__(self,initial=Player.states.initial)
        self.name = who

        self.ball = ball
        self.partner = False
        self.logger.info('%s in state %r' % (self.name, self.state))
    
    def handleActivate(self):
        '''
        Activation handler -- joins the PingPong group
        '''
        self.group = self.joinGroup('PingPong',self.name)
    
    def handleMemberJoined(self,group,memberId):
        '''
        When another member (player) joins the group we know we have a partner, hence the game can start.
        '''
        self.logger.info('handleMemberJoined[%s]: %s' % (group.getGroupName(),str(memberId)))
        self.partner = True
    
    def is_ready(self):
        '''
        Return True if we have a partner AND we are connected
        '''
        # self.logger.info('%s partner=%r,=%r' % (self.name,self.partner, self.catch.connected()))
        return self.partner and self.catch.connected() > 1
    
    @FSM.on(event=events.tick,state=states.initial,guard=lambda self: self.is_ready())
    def start(self):
        '''
        WHEN the tick event arrives AND we are in the initial state AND we have a partner
        we change our state according to the constructor argument (ball=True/False) 
        '''
        self.state = Player.states.has_ball if self.ball else Player.states.no_ball # This is a shortcut to change state
        self.logger.info('%s started in state %r' % (self.name,self.state))
        
    @FSM.on(event=events.tick,state=states.has_ball,guard=lambda self: self.is_ready(),then=states.no_ball)
    def has_it(self):
        '''
        WHEN the tick event arrives AND we have the ball AND we have a partner
        we throw the ball
        THEN we go to the 'no_ball' state.
        '''
        self.logger.info('%s throws ball' % self.name)
        self.throw.send_pyobj((self.name,'ball',))
        
    @FSM.on(event=events.tick,state=states.no_ball)
    def miss_it(self):
        '''
        WHEN the tick event arrives AND we don't have the ball
        THEN we do nothing
        '''
        self.logger.info('%s has no ball' % self.name)
        
    def not_own_ball(self):
        '''
        Return true if the ball is not ours
        '''
        msg = self.catch.msg_pyobj()
        own = (msg[0] == self.name)
        # self.logger.info("%s %s ball" % (self.name,'own' if own else 'not own'))
        return not own
         
    @FSM.on(event=events.catch,state=states.no_ball,guard=lambda self: self.not_own_ball(),then=states.has_ball)
    def catch_ball(self):
        '''
        WHEN  we catch a ball AND we are in the no_ball state AND it is not our own ball
        THEN we got to the has_ball state
        '''
        self.partner = True
        self.logger.info('%s got ball' % self.name)
        
    @FSM.on(event=events.catch,state=states.has_ball)
    def error_ball(self):
        '''
        WHEN we catch a ball AND already have a ball
        print an error message
        '''
        msg = self.catch.msg_pyobj()
        self.partner = True
        self.logger.info('%s got another ball? %r' % (self.name,msg))
    
    @FSM.on(event=events.catch,state=states.initial,then=states.has_ball)
    def catch_ball_initial(self):
        '''
        WHEN we catch a ball AND we are in the initial state
        THEN we go to the has_ball state 
        '''
        self.partner = True
        self.logger.info('%s got [initial] ball' % self.name)
        
        
        
 


