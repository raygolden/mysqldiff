#!/usr/bin/python

import gtk
import os

class MainWindow (gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        
        # Create builder:
        builder = gtk.Builder()
        builder.add_from_file("gui.ui")
        
        # Get main layout:
        builder.get_object('main_layout').reparent(self)
        self.builder = builder
        
        # Set some window attributes:
        self.set_default_size(500, 700)
        
        # Get widgets:
        quit_button = builder.get_object('quit_button')
        connect_button = builder.get_object('connect_button')
        
        # Set callbacks:
        self.connect('destroy', gtk.main_quit)
        quit_button.connect('clicked', gtk.main_quit)
        connect_button.connect('clicked', self.connect_click_callback)
        
    def connect_click_callback(self, widget=None, data=None):
        # Get widgets for values:
        
        db1_host = self.builder.get_object('db1_host').get_text()
        db1_user = self.builder.get_object('db1_user').get_text()
        db1_pass = self.builder.get_object('db1_pass').get_text()
        db1_db = self.builder.get_object('db1_db').get_text()
        db2_host = self.builder.get_object('db2_host').get_text()
        db2_user = self.builder.get_object('db2_user').get_text()
        db2_pass= self.builder.get_object('db2_pass').get_text()
        db2_db = self.builder.get_object('db2_db').get_text()
        
        cmd = "./mysqldiff -h1 %s -u1 %s -d1 %s -p1 %s -h2 %s -u2 %s -d2 %s -p2 %s" % (db1_host, db1_user, db1_db, db1_pass, db2_host, db2_user, db2_db, db2_pass)
        print cmd
        os.system(cmd + ' > .tmpOutput')
        
        output = open('.tmpOutput', 'r').read()
        
        os.system('rm .tmpOutput')
        
        print output
