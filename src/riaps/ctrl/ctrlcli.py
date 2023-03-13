'''
Controller CMD
Created on Dec 6.2016

@author: riaps
'''
import gi
import rpyc
import time
import sys
import os
import zmq
from os.path import join
from _collections import OrderedDict
import re
import logging
import cmd
import traceback
import socket
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

from threading import RLock

cmdLock = RLock()  # Global GUI lock
cmdClient = None


class ControlCLIClient(object):
    '''
    Controller GUI class
    '''

    def __init__(self, port, controller,script):
        '''
        Builds the GUI, connects it to the server (thread). The GUI is just another client of
        the service.
        '''
        global cmdClient
        cmdClient = self
        self.logger = logging.getLogger(__name__)
        self.port = port
        self.controller = controller
        self.context = controller.context
        self.script = script
        self.prompt = '$ '
        (self.stdin,self.echo) = (sys.stdin,False) if self.script == '-' else (open(script,'r'),True)
        self.stdout = sys.stdout
#         self.conn = rpyc.connect(self.controller.hostAddress, port)  # Local connection to the service
#         GLib.io_add_watch(self.conn, 1, GLib.IO_IN, self.bg_server)  # Register the callback with the service
#         GLib.io_add_watch(self.stdin, 1, GLib.IO_IN, self.cmd_server)
#         self.conn.root.login("*gui*", self.on_serverMessage)  # Log in to the service

        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind(self.controller.endpoint)
        GLib.io_add_watch(self.socket.fileno(), 1, GLib.IO_IN, self.on_serverMessage)
        GLib.io_add_watch(self.stdin, 1, GLib.IO_IN, self.cmd_server)
        
        self.appDownLoaded = False
        self.appFolder = None
        self.appName = None
        self.deplName = None
        
        self.nodeIDDict = OrderedDict()
        self.appStatusDict = OrderedDict()

        self.loop = GLib.MainLoop()
    
    class CtrlCmdShell(cmd.Cmd):
        intro = 'Welcome to the ctrl shell.   Type help or ? to list commands.\n'
        
        def __init__(self,parent):
            super(parent.CtrlCmdShell, self).__init__()
            self.parent = parent
            
        def do_f(self,arg):
            '''Select app folder: f path'''
            self.parent.cmdSelectFolder(arg)
            
        def do_m(self,arg):
            '''Select app model: m app.riaps'''
            self.parent.cmdSelectApp(arg)
        
        def do_d(self,arg):
            '''Select deployment model: d app.depl '''
            self.parent.cmdSelectDepl(arg)
            
        def do_i(self,arg):
            '''Install app: i app'''
            self.parent.cmdLoadApp(arg)
            
        def do_l(self,arg):
            '''Launch app: g app'''
            self.parent.cmdLaunchApp(arg)
            
        def do_h(self,arg):
            '''Halt app: h app'''
            self.parent.cmdStopApp(arg)
    
        def do_r(self,arg):
            '''Remove app: r app'''
            self.parent.cmdRemoveApp(arg)
            
        def do_w(self,arg):
            '''Wait: w sec'''
            # self.parent.conn.poll_all(int(arg))
            #             poller = zmq.Poller()
            #             poller.register(self.parent.socket, zmq.POLLIN)
            #             socks = dict(poller.poll(int(arg)))
            #             if self.parent.socket in socks:
            #                 self.parent.on_serverMessage()
            time.sleep(int(arg))

        def do_e(self,arg):
            ''' Echo argument: e message'''
            self.stdout.write(arg + '\r\n')
            self.stdout.flush()
                
        def do_shell(self,arg):
            ''' Execute command: e ls -l'''
            subprocess.call(arg.split())
        
        def do_j(self,args):
            ''' Join host(s): j [hosts]+ [wait]'''
            try:
                items = args.split()
                wait = None
                if len(items) >= 2:
                    last = items[-1]
                    if last.isnumeric(): wait = abs(int(last)); items = items[0:-1]
                expected = set(items)
                expected = { socket.gethostbyname(host) for host in expected }
                while(True):
                    clients = set(self.parent.controller.getClients())
                    if expected.issubset(clients):
                        break
                    elif wait is not None: 
                        if wait > 0: 
                            time.sleep(1.0)
                            wait -= 1
                        else:
                            self.stdout.write('? join timeout ' + args + '\r\n')
                            self.stdout.flush()
                            break
            except Exception as e:
                self.stdout.write('exception: ' + str(e) + '\r\n')
                self.stdout.flush()                      
            
        def do_q(self,arg):
            '''Quit program'''
            self.parent.cmdQuit()
        
    def run(self):
        self.do_prompt()
        self.shell = self.CtrlCmdShell(self)
        self.loop.run()
    
#     def bg_server(self, source=None, cond=None):
#         '''Check if there is something pending from the server thread.'''
#         if self.conn:
#             self.conn.poll_all()
#             return True
#         else:
#             return False
    
    def do_prompt(self):
        if not self.echo:
            self.stdout.write(self.prompt)
            self.stdout.flush()

    def cmd_script(self,fname,fnames=[]):
        fnames.append(fname)
        with open(fname) as f:
            for line in f.readlines():
                self.cmd_line(line.rstrip('\r\n'),fnames)
    
    def cmd_line(self,line,fnames=[]):
        if self.echo: print('(cmd) %s' % line)
        if not len(line): return
        first = line[0]
        if first == '#':
            pass                # Comment
        elif first == '@':
            line = line.lstrip('@ ')
            if line in fnames:
                pass                            # Error
            else:
                echo = self.echo
                self.echo = True
                self.cmd_script(line,fnames)    # Load the script
                self.echo = echo
        else:

            self.shell.onecmd(line)
            
    def cmd_server(self, source=None, _cond=None):
        if source == None: return
        line = source.readline()
        if not len(line):
            line = 'EOF'
        else:
            line = line.rstrip('\r\n')
        if line == 'EOF':
            self.cmdQuit()
            return False
        else:
            try:
                self.cmd_line(line)
            except:
                traceback.print_exc()
            self.stdout.flush()
            source.flush()
            self.do_prompt()
        return True

    def log(self,text):
        global cmdLock
        with cmdLock:
            text = '\n> ' + text + '\n'
            print(text)
        
    def on_serverMessage(self, _channel=None, _cond=None):
        '''
        Callback used by the service thread(s): it prints a log message.
        '''
        while True:
            try:
                text = self.socket.recv_pyobj(flags=zmq.NOBLOCK)
                self.log(text)
            except zmq.error.ZMQError:
                break
        return True

    def isAppOK(self):
        aName = self.appName
        dName = self.deplName
        return (aName != None and aName != '' and dName != None and dName != '')

    def cmdSelectApp(self,fileName):
        if fileName != None:
            # Check if file exists
            self.appName = fileName
            self.controller.compileApplication(fileName, self.appFolder)
        
    def cmdClearApp(self):
        '''
        Clears the app entry.
        '''
        self.appName = ''
          
    def cmdSelectDepl(self,fileName):
        if fileName != None:
            # Check if file exists
            self.deplName = fileName
            self.controller.compileDeployment(fileName) 

    def cmdClearDepl(self):
        '''
        Clears the deployment entry
        '''
        self.deplName = ''

            
    def cmdSelectFolder(self,folderName):
        if folderName != None:
            # Check if folder exists
            self.appFolder = folderName
            self.controller.setAppFolder(folderName)
    
    def cmdQuit(self):
        '''
        Quit the app. Forces a return from the CMD loop
        '''
        # self.conn.close()
        self.socket.close()
        self.loop.quit()   

    def cmdLoadApp(self,appSelected):
        self.controller.loadByName(appSelected)
        
    def cmdLaunchApp(self,appSelected):
        self.controller.launchByName(appSelected)
              
    def cmdStopApp(self,appSelected):
        self.controller.haltByName(appSelected)
       
    def cmdRemoveApp(self,appSelected):
        self.controller.removeAppByName(appSelected)

    def clearApplication(self):
        self.cmdClearApp()
        
    def clearDeployment(self):
        self.cmdClearDepl()
        
    def update_node_apps(self,clientName,data):
        global cmdLock
        with cmdLock:
            if not data: return
            for item in data:
                appName,actors = item[0],item[1]
                for actorName in actors:
                    self.controller.addToLaunchList(clientName,appName,actorName)
                    
                    
        
