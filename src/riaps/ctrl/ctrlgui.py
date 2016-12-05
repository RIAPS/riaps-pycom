'''
Controller GUI
Created on Nov 7, 2016

@author: riaps
'''
import gi
import rpyc
import time
import sys
import os
from os.path import join

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from threading import RLock
guiLock = RLock()               # Global GUI lock

guiClient = None

class ControlGUIClient(object):
    '''
    Controller GUI class
    '''
    def __init__(self,port,controller):
        '''
        Builds the GUI, connects it to the server (thread). The GUI is just another client of
        the service. 
        '''
        global guiClient
        guiClient = self
        self.port = port
        self.controller = controller
        self.builder = Gtk.Builder()
        riaps_folder = os.getenv('RIAPSHOME', './')
        self.builder.add_from_file(join(riaps_folder,"etc/riaps-ctrl.glade"))  # GUI construction
        self.builder.connect_signals({"onDeleteWindow" : self.on_Quit, 
                                      "onConsoleEntryActivate" : self.on_ConsoleEntry,
                                      "onSelectApplication" : self.on_SelectApplication,
                                      "onSelectDeployment" : self.on_SelectDeployment,
                                      "onFolderEntryActivate" : self.on_folderEntryActivate,
                                      "onQuit" : self.on_Quit,
                                      "onLaunch" : self.on_Launch,
                                      })

        self.conn = rpyc.connect("localhost",port)  # Local connection to the service
        GLib.io_add_watch(self.conn,1,GLib.IO_IN,self.bg_server)    # Register the callback with the service
        self.conn.root.login("*gui*",self.on_serverMessage)         # Log in to the service
        
        self.mainWindow = self.builder.get_object("window1")
        self.messages = self.builder.get_object("messageTextBuffer")
        self.consoleIn  = self.builder.get_object("consoleEntryBuffer")
        self.appNameEntry = self.builder.get_object("appNameEntry")
        self.deplNameEntry = self.builder.get_object("deplNameEntry")
        self.folderEntry = self.builder.get_object("folderEntry")
        self.launchButton = self.builder.get_object("launchButton")
        self.appLaunched = False
        self.mainWindow.show_all()
        
    def bg_server(self, source = None, cond = None):
        '''
        Check if there is something pending from the server thread. Called by the main GUI loop 
        '''
        if self.conn:
            self.conn.poll_all()
            return True
        else:
            return False
           
    def on_serverMessage(self,text):
        '''
        Callback used by the service thread(s): it prints a log message. 
        '''
        global guiLock
        with guiLock:
            end = self.messages.get_end_iter()
            text = '> ' + text + '\n'
            self.messages.insert(end,text)


    def on_ConsoleEntry(self,*args):
        '''
        Called when the console entry receives an 'activate' event
        NOT USED 
        '''
        source = self.consoleIn.get_text()
        pass
    
    def selectFile(self,title,pattern):
        '''
        File selection dialog
        '''
        self.fcd = Gtk.FileChooserDialog("Select " + str(title),
                                         None,
                                         Gtk.FileChooserAction.OPEN,
                                         (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                          Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        filterR = Gtk.FileFilter()
        filterR.set_name("%s" % pattern)
        filterR.add_pattern(pattern)
        self.fcd.add_filter(filterR)

        filterA = Gtk.FileFilter()
        filterA.set_name("All files")
        filterA.add_pattern("*")
        self.fcd.add_filter(filterA)
           
        self.fcd.set_transient_for(self.mainWindow)
                                  
        self.response = self.fcd.run()
        fileName = None
        if self.response == Gtk.ResponseType.OK:
            fileName = self.fcd.get_filename()
        self.fcd.destroy()
        return fileName
    
    def selectFolder(self,title):
        '''
        Folder selection dialog
        '''
        self.fcd = Gtk.FileChooserDialog("Select " + str(title),
                                         None,
                                         Gtk.FileChooserAction.SELECT_FOLDER,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                         "Select", Gtk.ResponseType.OK))
        

        self.fcd.set_transient_for(self.mainWindow)
                          
        self.response = self.fcd.run()
        folderName = None
        if self.response == Gtk.ResponseType.OK:
            folderName = self.fcd.get_filename()
        self.fcd.destroy()
        return folderName
            
    def on_SelectApplication(self,*args):
        '''
        App selection. Sets the app entry and calls the controller to compile the app model. 
        '''
        fileName = self.selectFile("application","*.riaps")
        if fileName != None:
            self.appNameEntry.set_text(os.path.basename(fileName))
            self.controller.compileApplication(fileName)

    def clearApplication(self):
        '''
        Clears the app entry.
        '''
        self.appNameEntry.set_text('')
        
    def on_SelectDeployment(self,*args):
        '''
        Deployment selection. Sets the deployment entry and calls the controller 
        to compile the deployment model. 
        '''
        fileName = self.selectFile("application","*.depl")
        if fileName != None:
            self.deplNameEntry.set_text(os.path.basename(fileName))
            self.controller.compileDeployment(fileName)
            
    def clearDeployment(self):
        '''
        Clears the deployment entry
        '''
        self.deplNameEntry.set_text('')

    def on_folderEntryActivate(self,*args):
        '''
        App folder selection. Called when the folder entry or the folder button is activated.  
        '''
        folderName = self.selectFolder("application folder")
        if folderName != None:
            self.folderEntry.set_text(folderName)
            self.controller.setAppFolder(folderName)
    
    def on_Quit(self,*args):
        '''
        Quit the app. Forces a return from the GUI loop
        '''
        self.conn.close()
        Gtk.main_quit()
    
    def on_Launch(self,*args):
        '''
        Application launch or halt. Called when the Launch/Halt button is activated.
        For success, the app name and deployment name has to be set.    
        '''
        aName = self.appNameEntry.get_text()
        dName = self.deplNameEntry.get_text()
        if self.appLaunched == False:
            if aName != None and aName != '' and dName != None and dName != '':
                ok = self.controller.launch()
                if not ok:
                    return
                else:
                    self.launchButton.set_label("Stop")
                    self.appLaunched = True
        else:
            self.controller.halt()
            self.launchButton.set_label("Launch")
            self.appLaunched = False
            
        


