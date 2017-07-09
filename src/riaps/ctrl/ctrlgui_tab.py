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
from _collections import OrderedDict
import re
import logging

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

from threading import RLock

guiLock = RLock()  # Global GUI lock

guiClient = None


class ControlGUIClient_Tab(object):
    '''
    Controller GUI class
    '''

    def __init__(self, port, controller):
        '''
        Builds the GUI, connects it to the server (thread). The GUI is just another client of
        the service.
        '''
        global guiClient
        guiClient = self
        self.logger = logging.getLogger(__name__)
        self.port = port
        self.controller = controller
        self.builder = Gtk.Builder()
        riaps_folder = os.getenv('RIAPSHOME', './')
        try:
            self.builder.add_from_file(join(riaps_folder, "etc/riaps-ctrl-table.glade"))  # GUI construction
        except RuntimeError:
            self.logger.error('Cannot find GUI configuration file')
            raise
        self.builder.connect_signals({"onDeleteWindow": self.on_Quit,
                                      "onConsoleEntryActivate": self.on_ConsoleEntry,
                                      "onSelectApplication": self.on_SelectApplication,
                                      "onSelectDeployment": self.on_SelectDeployment,
                                      "onFolderEntryActivate": self.on_folderEntryActivate,
                                      "onQuit": self.on_Quit,
                                      "onLoadApplication": self.on_LoadApplication
                                      })

        self.conn = rpyc.connect(self.controller.hostAddress, port)  # Local connection to the service
        GLib.io_add_watch(self.conn, 1, GLib.IO_IN, self.bg_server)  # Register the callback with the service
        self.conn.root.login("*gui*", self.on_serverMessage)  # Log in to the service

        self.mainWindow = self.builder.get_object("window1")
        self.messages = self.builder.get_object("messageTextBuffer")
        self.consoleIn = self.builder.get_object("consoleEntryBuffer")
        self.appNameEntry = self.builder.get_object("appNameEntry")
        self.deplNameEntry = self.builder.get_object("deplNameEntry")
        self.folderEntry = self.builder.get_object("folderEntry")
        #self.launchButton = self.builder.get_object("launchButton")
        #self.launchButton.set_sensitive(False)
        #self.stopButton = self.builder.get_object("stopButton")
        #self.stopButton.set_sensitive(False)
        #self.removeButton = self.builder.get_object("removeButton")
        #self.removeButton.set_sensitive(False)
        self.appLaunched = False
        self.appDownLoaded = False

        '''
        Status Table Additions
        '''
        self.cellTextPlaceHolder = '                '
        self.column_cur_size = 8
        self.row_cur_size = 32
        self.appToLoad = None
        self.appSelected = None
        self.gridScrollWindow = self.builder.get_object('scrolledwindow2')
        self.gridTable = Gtk.Grid()
        self.gridScrollWindow.add_with_viewport(self.gridTable)
        self.nodeIDDict = OrderedDict()
        self.appStatusDict = OrderedDict()
        self.init_GridTable()

        self.mainWindow.show_all()

    def bg_server(self, source=None, cond=None):
        '''
        Check if there is something pending from the server thread. Called by the main GUI loop
        '''
        if self.conn:
            self.conn.poll_all()
            return True
        else:
            return False

    def on_serverMessage(self, text):
        '''
        Callback used by the service thread(s): it prints a log message.
        '''
        global guiLock
        with guiLock:
            end = self.messages.get_end_iter()
            text = '> ' + text + '\n'
            self.messages.insert(end, text)
        self.check_server_msg(text)


    def on_ConsoleEntry(self, *args):
        '''
        Called when the console entry receives an 'activate' event
        NOT USED
        '''
        source = self.consoleIn.get_text()
        pass

    def selectFile(self, title, pattern):
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

    def selectFolder(self, title):
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

    def isAppOK(self):
        aName = self.appNameEntry.get_text()
        dName = self.deplNameEntry.get_text()
        return (aName != None and aName != '' and dName != None and dName != '')

    def on_SelectApplication(self, *args):
        '''
        App selection. Sets the app entry and calls the controller to compile the app model.
        '''
        fileName = self.selectFile("application", "*.riaps")
        if fileName != None:
            self.appNameEntry.set_text(os.path.basename(fileName))
            self.controller.compileApplication(fileName, self.folderEntry.get_text())
            #if self.isAppOK():
            #    self.launchButton.set_sensitive(True)
            #    self.removeButton.set_sensitive(True)

    def clearApplication(self):
        '''
        Clears the app entry.
        '''
        self.appNameEntry.set_text('')

    def on_SelectDeployment(self, *args):
        '''
        Deployment selection. Sets the deployment entry and calls the controller
        to compile the deployment model.
        '''
        fileName = self.selectFile("application", "*.depl")
        if fileName != None:
            self.deplNameEntry.set_text(os.path.basename(fileName))
            self.appToLoad = self.controller.compileDeployment(fileName)
            #if self.isAppOK():
            #    self.launchButton.set_sensitive(True)
            #    self.removeButton.set_sensitive(True)

    def clearDeployment(self):
        '''
        Clears the deployment entry
        '''
        self.deplNameEntry.set_text('')

    def on_folderEntryActivate(self, *args):
        '''
        App folder selection. Called when the folder entry or the folder button is activated.
        '''
        folderName = self.selectFolder("application folder")
        if folderName != None:
            self.folderEntry.set_text(folderName)
            self.controller.setAppFolder(folderName)

    def on_Quit(self, *args):
        '''
        Quit the app. Forces a return from the GUI loop
        '''
        self.conn.close()
        Gtk.main_quit()

    """
    Begin Status Table Additions
    """
    def check_server_msg(self, text):
        '''
        Server message parser and dispatcher. Based on the log message received, updates the status grid gui.
        To be deprecated when the server is updated to call directly the status grid gui update functions. 
        '''
        statusList = text.split(' ')
        if statusList[0] == ('>'):
            ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', text)
            #if len(ip) == 0:
            #    return
            ip = ''.join(ip)
            if statusList[1] == ('+'):            # node connected
                self.update_node_connected_status(ip)
                return
            elif statusList[1] == '-':       # node disconnected
                self.update_node_disconnected_status(ip)
                return
            elif statusList[1] == 'R':      # remove status
                self.update_remove_status(statusList[2])
                return
            elif statusList[1] == 'H':      # halt status
                self.update_halt_status(statusList[2], statusList[3])
                return
            elif statusList[1] == 'L':      # launch status
                self.update_launch_status(statusList)

    """ Grid table update functions - to be used as entry points for status grid gui updates  """
    
    def update_node_connected_status(self, ip):
        '''
        A new node connected to the controller
        '''
        self.node_connected(ip)

    def update_node_disconnected_status(self, ip):
        '''
        A node disconnected from the controller
        '''
        self.node_disconnected(ip)

    def update_remove_status(self, app):
        ''' 
        An app has been removed
        '''
        # '> R DistributedAverager
        self.remove_app(app)

    def update_halt_status(self, node, app):
        '''
        An app has been halted on a node
        '''
        #'> H 129.59.105.70 DistributedAverager Averager'
        self.halt_app(node, app)

    def update_launch_status(self, info):
        ''' 
        An app has been launched on a node
        '''
        # '> L 129.59.105.70 DistributedAverager Averager []'
        node = info[2]
        app = info[3]
        actor = info[4]
        self.launch_app(node, app, actor)

    """ Status grid gui update functions - these are the actual update functions """
        
    def node_connected(self, ip):
        '''
        A node connected to the controller
        '''
        self.nodeIDDict[ip] = True
        num_nodes = len(self.nodeIDDict)
        num_node_cols = self.column_cur_size - 1

        if num_nodes > num_node_cols:
            for i in range(self.column_cur_size, num_nodes + 1):
                self.add_table_column(i)
                self.column_cur_size = self.column_cur_size + 1

        keys = list(self.nodeIDDict.keys())
        col_id = keys.index(ip) + 1
        cell = self.gridTable.get_child_at(col_id, 0)
        if cell is not None:
            self.modify_text_cell_color(cell, 'black', 'white')
            self.modify_text_cell_text(cell, ip)

        self.gridTable.show_all()

    def node_disconnected(self, ip):
        '''
        A node disconnected from the controller
        '''
        if ip not in self.nodeIDDict:
            return

        self.nodeIDDict[ip] = False
        col_keys = list(self.nodeIDDict.keys())
        col_idx = col_keys.index(ip) + 1
        c_cell = self.gridTable.get_child_at(col_idx, 0)

        if c_cell is not None:
            self.modify_text_cell_color(c_cell, 'black', 'gray')


            # modify data - reset the data at a particular (col_idx)
            for row_idx, key in enumerate(self.appStatusDict, 1):
                self.appStatusDict[key][col_idx] = ''
                r_cell = self.gridTable.get_child_at(col_idx, row_idx)
                if r_cell is not None:
                    self.modify_text_cell_color(r_cell, 'white')
                    self.modify_text_cell_text(r_cell, self.cellTextPlaceHolder)

        self.gridTable.show_all()

    def remove_app(self, app):
        ''' 
        An app has been removed from the system
        '''
        # modify gui
        index = list(self.appStatusDict.keys()).index(app) + 1
        self.remove_table_row(index)
        self.row_cur_size = self.row_cur_size - 1

        # modify data
        del self.appStatusDict[app]

        self.create_table_row(self.row_cur_size, self.column_cur_size)
        self.row_cur_size = self.row_cur_size + 1
        self.gridTable.show_all()

    def halt_app(self, node, app):
        '''
        An app has been halted
        '''
        if node not in self.nodeIDDict:
            return

        if self.nodeIDDict[node] is True:
            col_map = list(self.nodeIDDict.keys())
            col_id = col_map.index(node) + 1
            row_map = list(self.appStatusDict.keys())
            row_id = row_map.index(app) + 1
            cell = self.gridTable.get_child_at (col_id, row_id)
            self.modify_text_cell_color(cell, 'grey')

    def launch_app(self, node, app, actor):
        '''
        An app has been launched
        '''
        if node not in self.nodeIDDict:
            return

        col_map = list(self.nodeIDDict.keys())
        col_id = col_map.index(node) + 1
        row_map = list(self.appStatusDict.keys())
        row_id = row_map.index(app) + 1

        existing_actor = self.appStatusDict[app][col_id - 1]
        if existing_actor == 'None' or existing_actor == '':
            self.appStatusDict[app][col_id - 1] = actor
        elif actor not in existing_actor:
            self.appStatusDict[app][col_id - 1] = existing_actor + '\n' + actor

        cell = self.gridTable.get_child_at(col_id, row_id)
        if cell is None:
            self.gridTable.attach(self.create_table_cell(self.appStatusDict[app][col_id - 1], 'black', 'lime'), col_id, row_id, 1, 1)
        else:
            self.modify_text_cell_color(cell, 'lime', 'black')
            child_list = cell.get_children()
            child_list[0].set_label(self.appStatusDict[app][col_id - 1])

        self.gridTable.show_all()       # not sure if it's necessary here


    def add_app(self, app):
        if app in self.appStatusDict:
            return

        self.appStatusDict[app] = [''] * self.column_cur_size
        num_apps = len(self.appStatusDict)
        num_app_rows = self.row_cur_size - 1
        if (num_apps > num_app_rows):
            for i in range(self.row_cur_size, num_apps + 1):
                self.create_table_row(i, self.column_cur_size)
                self.row_cur_size = self.row_cur_size + 1

        cell = self.gridTable.get_child_at(0, len(self.appStatusDict))
        cell.destroy()
        self.gridTable.attach(self.create_app_menu_button(app), 0, len(self.appStatusDict), 1, 1)

        self.gridScrollWindow.show_all()

    def on_LoadApplication(self, widget):
        '''
        Load the selected application onto to the network
        '''
        # add a row in the table for the application
        if self.appToLoad is None:
            return

        self.add_app(self.appToLoad)
        self.clearApplication()
        self.clearDeployment()
        self.appToLoad = ''

    ''' Event handlers for widgets(buttons etc) '''
    def on_show_app_ctrl_options(self, widget):
        # set selected app name
        self.appSelected = widget.get_label()
        widget.get_popup().show_all()

    def on_launch_app_press(self, widget):
        appSelected = self.appSelected
        self.appSelected = ''
        self.controller.launchByName(appSelected)

    def on_stop_app_press(self, widget):
        appSelected = self.appSelected
        self.appSelected = ''
        self.controller.haltByName(appSelected)

    def on_remove_app_press(self, widget):
        appSelected = self.appSelected
        self.appSelected = ''
        self.controller.removeAppByName(appSelected)

    ''' Initialize grid table with blank cells '''
    def init_GridTable(self):
        # Add 1st button 
        for c in range(self.row_cur_size):
            self.create_table_row(c, self.column_cur_size)


    def create_table_row(self, row_index, col_length):
        for i in range(col_length):
            cell = self.create_table_cell(self.cellTextPlaceHolder)
            self.gridTable.attach(cell, i, row_index, 1, 1)
            if row_index == 0:
                self.modify_text_cell_color(cell, 'black', 'white')
                if i == 0: 
                    self.modify_text_cell_text(cell, "App \\ Node")

    ''' Utility functions '''
    def create_app_menu_button (self, text):
        menu_button = Gtk.MenuButton(text)
        menu_button.connect('pressed', self.on_show_app_ctrl_options)

        menu = Gtk.Menu()
        menu_button.set_popup(menu)


        item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_MEDIA_PLAY)
        item.get_child().set_text('Launch')
        item.connect('activate', self.on_launch_app_press)
        menu.append(item)
        item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_MEDIA_STOP)
        item.connect('activate', self.on_stop_app_press)
        menu.append(item)
        menu.append(Gtk.SeparatorMenuItem())
        item = Gtk.ImageMenuItem.new_from_stock(Gtk.STOCK_REMOVE)
        item.connect('activate', self.on_remove_app_press)
        menu.append(item)

        return menu_button

    def create_table_cell(self, text, fg_color = 'blue', bg_color = 'white'):
        try:
            frame_box = Gtk.Frame()
            frame_box.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse(fg_color))
            frame_box.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(bg_color))

            text_label = Gtk.Label()
            text_content = '<b>' + ''.join(text) + '</b>'
            text_label.set_markup(text_content)
            text_label.set_justify(Gtk.Justification.CENTER)
            frame_box.add(text_label)
            return frame_box
        except Exception as e:
            message = str(e)
            return None

    def add_table_column(self, col_index):
        for i in range(self.row_cur_size):
            self.gridTable.attach(self.create_table_cell(self.cellTextPlaceHolder, 'black'), col_index, i, 1, 1)

        self.gridTable.show_all()


    def remove_table_row(self, index):
        self.gridTable.remove_row(index)


    ''' Cell helper functions'''
    def modify_text_cell_color(self, cell, bg='', fg=''):
        if cell is not None:
            if bg is not '':
                cell.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse(bg))

            if fg is not '':
                cell.modify_fg(Gtk.StateType.NORMAL, Gdk.color_parse(fg))


    def modify_text_cell_text(self, cell, text=''):
        if cell is not None:
            children = cell.get_children()
            if len(children) > 0:
                children[0].set_label(text)

    def set_cell_bg_color(self, text):
        if 'Actor' in text:
            bg_color = 'lime'
        if 'Stopped' in text:
            bg_color = 'grey'
        return bg_color

    '''
    End Status Table Additions
    '''
