#!/usr/bin/python

import MySQLdb

class Database:
    def __init__(self, host, username, password, database):
        self.host = host

        try:
            self.db = MySQLdb.connect(host=host, user=username, passwd=password, db=database)
        except:
            print "Could not connect to %s with that username and password." % host
            exit(1)
        self.cursor = self.db.cursor()
    
    def get_tables(self):
        tables = self.get_array("SHOW TABLES")
        results = []
        for table in tables:
            results.append(table[0])
        return results
    
    def get_host(self):
        return self.host
    
    def get_table(self, table):
        sql = "EXPLAIN " + table
        table = self.get_array(sql)
        data = []
        for row in table:
            data.append(row[0:6])
        return data
    
    def get_array(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        results = []
        for record in result:
            results.append(record)
