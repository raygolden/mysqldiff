#!/usr/bin/python

import gtk
import os
from Database import Database

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
        
        self.compare_dbs(db1_host, db1_user, db1_pass, db1_db, db2_host, db2_user, db2_pass, db2_db)
    
    def get_fieldname_list(self, tdata):
        data = []
        for row in tdata:
            data.append(row[0])
        return data

    def get_field_from_fieldname(self, fieldname, fields):
        for field in fields:
            if fieldname == field[0]:
                return field
        return False
    
    def compare_dbs(self, db1_host, db1_user, db1_pass, db1_db, db2_host, db2_user, db2_pass, db2_db):
        print db1_host, db1_user, db1_pass, db1_db
        print db2_host, db2_user, db2_pass, db2_db
        
        db1 = Database(db1_host, db1_user, db1_pass, db1_db)
        db2 = Database(db2_host, db2_user, db2_pass, db2_db)
        
        # Check if tables are the same:
        db1_tables = db1.get_tables()
        db2_tables = db2.get_tables()
        diff = list(set(db1_tables) - set(db2_tables))
        
        # Output table diff:
        if diff == []:
            print " - Table names match each other, no tables missing on either server."
        else:
            for db in diff:
                if db1_tables.count(db) == 0:
                    server = db2.get_host()
                else:
                    server = db1.get_host()

            print " ! The table \"%s\" exists only on \"%s\"." % (db, server)
        

        # Get field info for each table and compare:
        for table in db1_tables:
            if table in diff:
                continue

            tdata1 = db1.get_table(table)
            tdata2 = db2.get_table(table)

            if tdata1 == tdata2:
                if args.quiet == 'verbose':
                    print " - \"%s\" is the same on both servers." % table
            else:
                print " ! \"%s\" has differences:" % table
            
                # Get fieldname lists:
                db1_table = get_fieldname_list(tdata1)
                db2_table = get_fieldname_list(tdata2)
                
                diff = list(set(db1_table) - set(db2_table))
                
                if diff == []:
                    for field in db1_table:
                        db1_field = get_field_from_fieldname(field, tdata1)
                        db2_field = get_field_from_fieldname(field, tdata2)
                        
                        # Check datatype:
                        if db1_field[1] != db2_field[1]:
                            print "        - Different datatype with field \"%s\": '%s' on '%s', '%s' on '%s'." % (field, db1_field[1], db1.get_host(), db2_field[1], db2.get_host())
                        
                        # Check NULL status:
                        if db1_field[2] != db2_field[2]:
                            if db1_field[2] == 'NO':
                                db1_null = "set as NOT NULL"
                                db2_null = "it is allowed to be NULL"
                            else:
                                db1_null = "allowed to be NULL"
                                db2_null = "it is set as NOT NULL"
                            
                            print "        - Field \"%s\" on \"%s\" is %s whereas on \"%s\" %s." % (field, db1.get_host(), db1_null, db2.get_host(), db2_null)
                        
                        # Check key:
                        
                        # Check default field:
                        
                        # Check extra field:
                        
                else:
                    for field in diff:
                        if db1_table.count(field) == 0:
                            server = db2.get_host()
                        else:
                            server = db1.get_host()
                        print "        - Field \"%s\" only exists on \"%s\"" % (field, server)
