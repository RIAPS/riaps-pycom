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
import readline
import cmd
import traceback
import socket
import threading
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

from threading import RLock

cmdLock = RLock()  # Global GUI lock
cmdClient = None


class ControlCLITerm(threading.Thread):
    endpoint = "inproc://riaps-cli"
    
    def __init__(self,context):
        threading.Thread.__init__(self,name='ControlCLITerm',daemon=False)
        self.context = context
        
    def run(self):
        self.cmdSocket = self.context.socket(zmq.PAIR)
        self.cmdSocket.connect(ControlCLITerm.endpoint)
        while True:
            try:
                command = input('? ')
                self.cmdSocket.send_pyobj(command)
            except EOFError:
                self.cmdSocket.send_pyobj('EOF')
            _r = self.cmdSocket.recv_pyobj()
            if _r == 'quit': break
        self.cmdSocket.disconnect(ControlCLITerm.endpoint)
        self.cmdSocket.close()
        
class ControlCLIClient(object):
    '''
    Controller GUI class
    '''

    TRACEBACK = True
    
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
        self.stdout = sys.stdout
        (self.stdin,self.echo) = (sys.stdin,False) if self.script == '-' else (open(script,'r'),True)
        
        self.ctrlSocket = self.context.socket(zmq.PULL)
        self.ctrlSocket.bind(self.controller.endpoint)
        GLib.io_add_watch(self.ctrlSocket.fileno(), GLib.IO_IN, self.on_serverMessage)        

        if self.script == '-':
            self.echo = False
            self.terminal = ControlCLITerm(self.context)
            self.termSocket = self.context.socket(zmq.PAIR)
            self.termSocket.bind(ControlCLITerm.endpoint)
            GLib.io_add_watch(self.termSocket.fileno(), GLib.IO_IN, self.on_termMessage)
            self.terminal.start()
        else:
            self.echo = True
            self.terminal = None
            self.termSocket = None 
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
            
        def do_a(self,arg):
            '''Select app folder: a[pp] path'''
            self.parent.cmdSelectApp(arg)
            
        def do_m(self,arg):
            '''Select app model: m[odel] app.riaps'''
            self.parent.cmdSelectModel(arg)
        
        def do_d(self,arg):
            '''Select deployment model: d[eployment] app.depl '''
            self.parent.cmdSelectDepl(arg)
            
        def do_i(self,arg):
            '''Install app: i[nstall] app'''
            self.parent.cmdInstallApp(arg)
            
        def do_l(self,arg):
            '''Launch app: l[aunch] app'''
            self.parent.cmdLaunchApp(arg)
            
        def do_h(self,arg):
            '''Halt app: h[alt] app'''
            self.parent.cmdHaltApp(arg)
        
        def do_u(self,arg):
            '''Uninstall app: u[ninstall] app'''
            self.parent.cmdUninstallApp(arg)
                 
        def do_r(self,_arg):
            '''Reset all nodes: r{eset}'''
            self.parent.cmdResetNodes()
            
        def do_s(self,arg):
            '''Stop all nodes s{top}'''
            self.parent.cmdStopNodes()
            
        def do_w(self,arg):
            '''Wait: w[ait] sec'''
            # self.parent.conn.poll_all(int(arg))
            #             poller = zmq.Poller()
            #             poller.register(self.parent.socket, zmq.POLLIN)
            #             socks = dict(poller.poll(int(arg)))
            #             if self.parent.socket in socks:
            #                 self.parent.on_serverMessage()
            if arg.isnumeric():
                delay = abs(int(arg))
                time.sleep(delay)
            else:
                raise RuntimeError(f'wait "{arg}" - int expected')

        def do_e(self,arg):
            ''' Echo argument: e[cho] message'''
            self.stdout.write(arg + '\r\n')
            self.stdout.flush()
                
        def do_fab(self,arg):
            '''Execute fab command: f[ab] args*'''
            self.parent.cmdFab(arg)
        
        def do_shell(self,arg):
            ''' Execute command: shell ls -l'''
            try:
                subprocess.call(arg.split())
            except:
                raise
        
        def do_j(self,args):
            ''' Join host(s): j[oin] [hosts]+ [timeout]'''
            items = args.split()
            tout = 60                   # Default timeout value
            if len(items) >= 2:
                last = items[-1]
                if last.isnumeric(): tout = abs(int(last)); items = items[0:-1]
                elif last == '-': tout = None; items = items[0:-1]
            expected = { socket.gethostbyname(host) for host in set(items) }
            while(True):
                clients = set(self.parent.controller.getClients())
                time.sleep(1.0)
                if expected.issubset(clients):
                    break
                elif tout is not None: 
                    if tout > 0: tout -= 1
                    else: raise RuntimeError(f'join {args} - timeout')                     
            
        def do_q(self,arg):
            ''' Quit: q[uit] '''
            self.parent.cmdQuit()
        
    def run(self):
        self.shell = self.CtrlCmdShell(self)
        self.loop.run()
    
#     def bg_server(self, source=None, cond=None):
#         '''Check if there is something pending from the server thread.'''
#         if self.conn:
#             self.conn.poll_all()
#             return True
#         else:
#             return False

    def cmd_script(self,fname,fnames=[]):
        '''
        Execute a script from file 'fname', save file name to 'fnames'
        '''
        fnames.append(fname)
        with open(fname) as f:
            for line in f.readlines():
                try:
                    self.cmd_line(line.rstrip('\r\n'),fnames)
                except:
                    if self.TRACEBACK: traceback.print_exc()
                    else: print(f"(err): {traceback.format_exc().splitlines()[-1]}")
                    self.cmdQuit()
    
    def cmd_line(self,line,fnames=[]):
        '''
        Execute one line. Skip comments (#), launch script if line starts
        with '@' - keep track of script names to avoid infinite recursion.    
        '''
        if self.echo: print(f"(cmd) {line}")
        if not len(line): return
        first = line[0]
        if first == '#':
            pass                # Comment
        elif first == '@':
            line = line.lstrip('@ ')
            if line in fnames:
                self.log(f"(inf) recursive script {line} - ignored")
                pass                            
            else:
                echo = self.echo
                self.echo = True
                self.cmd_script(line,fnames)    # Run the script
                self.echo = echo
        else:
            self.shell.onecmd(line)
            
    def cmd_server(self, source=None, _cond=None):
        '''
        Callback used by the service thread: reads one line from the script (file)
        and executes it. Terminates on error. 
        '''
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
                if self.TRACEBACK: traceback.print_exc()
                else: print(f"Error: {traceback.format_exc().splitlines()[-1]}")
                self.cmdQuit()
            self.stdout.flush()
            source.flush()
        return True

    def log(self,text):
        global cmdLock
        with cmdLock:
            print(f"(log) {text}")
            
    def on_termMessage(self, _channel=None, _cond=None):
        '''
        Callback used by the service thread: it receives the command from the terminal.
        Does not terminate on error. 
        '''
        while True:
            try:
                line = self.termSocket.recv_pyobj(flags=zmq.NOBLOCK)
                if line == 'EOF':
                    self.cmdQuit()
                    return False
                else:
                    try:
                        self.cmd_line(line)
                    except Exception:
                        if self.TRACEBACK: traceback.print_exc()
                        else: print(f"Error: {traceback.format_exc().splitlines()[-1]}")
                self.termSocket.send_pyobj('_')
            except zmq.error.ZMQError:
                break
        return True
        
    def on_serverMessage(self, _channel=None, _cond=None):
        '''
        Callback used by the service thread: it prints a log message.
        '''
        while True:
            try:
                text = self.ctrlSocket.recv_pyobj(flags=zmq.NOBLOCK)
                self.log(text)
                if text.startswith('* '):
                    self.cmdQuit()
            except zmq.error.ZMQError:
                break
        return True

    def isAppOK(self):
        aName = self.appName
        dName = self.deplName
        return (aName != None and aName != '' and dName != None and dName != '')
    
    def cmdSelectApp(self,folderName):
        '''
        Select app folder
        '''
        if folderName != None:
            self.controller.setAppFolder(folderName)
            self.appFolder = folderName
    
    def cmdSelectModel(self,fileName):
        if fileName != None:
            # Check if file exists
            self.appName = fileName
            res = self.controller.compileApplication(fileName, self.appFolder)
            if res is None:
                raise RuntimeError(f'error(s) compiling app model {fileName}')
        
    def cmdClearApp(self):
        '''
        Clears the app entry.
        '''
        self.appName = ''
          
    def cmdSelectDepl(self,fileName):
        if fileName != None:
            self.deplName = fileName
            res = self.controller.compileDeployment(fileName)
            if res is None:
                raise RuntimeError(f'error(s) compiling deployment model {fileName}')

    def cmdClearDepl(self):
        '''
        Clears the deployment entry
        '''
        self.deplName = ''

    def cmdQuit(self):
        '''
        Quit the app. Forces a return from the CMD loop
        '''
        # self.conn.close()
        if self.terminal:
            self.termSocket.send_pyobj('quit')
            time.sleep(0.01)
            self.termSocket.close()
            
        self.ctrlSocket.close()
        self.loop.quit()   

    def cmdInstallApp(self,appSelected):
        res = self.controller.loadByName(appSelected)
        if res is False:
            raise RuntimeError(f'error(s) installing app {appSelected}')    
        
    def cmdLaunchApp(self,appSelected):
        res = self.controller.launchByName(appSelected)
        if res is False:
            raise RuntimeError(f'error(s) launching app {appSelected}')    
              
    def cmdHaltApp(self,appSelected):
        res = self.controller.haltByName(appSelected)
        if res is False:
            raise RuntimeError(f'error(s) halting app {appSelected}')
        
    def cmdUninstallApp(self,appSelected):
        res = self.controller.removeAppByName(appSelected)
        if res is False:
            raise RuntimeError(f'error(s) uninstalling app {appSelected}')
            
    def cmdResetNodes(self):
        res = self.controller.cleanAll()
        if res is False:
            raise RuntimeError(f'error(s) resetting nodes')
    
    def cmdStopNodes(self):
        res = self.controller.cleanAll()
        self.controller.killAll()
        if res is False:
            raise RuntimeError(f'error(s) killing apps/nodes')

    def cmdFab(self,arg):
        print(f'fab:  {arg}')
        self.controller.executeFabCommand(arg)
        
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
                    
                    
        
