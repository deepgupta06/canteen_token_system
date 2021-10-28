# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 11:45:47 2021

@author: deep.g
"""

import sqlite3

'''q1 = """CREATE TABLE empinfo (
                                empid int PRIMARY KEY,
                                first_name varchar(255), 
                                last_name varchar(255), 
                                userid varchar(255),
                                password varchar(255),
                                usergroup varchar(255))"""'''

class DatabaseOp:
    def __init__(self, database_name):
        self.database_name = database_name
        
        self.conn = sqlite3.connect(self.database_name)
        self.mycurser = self.conn.cursor()
        
    def inserting_values(self, table_name, values):
        for value in values:
            quiery = "INSERT INTO {} VALUES{}".format(table_name, value)
            self.mycurser.execute(quiery)
            self.conn.commit()
            self.conn.close()
            
    def deletion_of_values(self, table_name, condition):
        '''condition format =(columan_name, matching_value)'''
        quiery = "DELETE FROM {} where {}=={}".format(table_name,condition[0],condition[1])
        self.mycurser.execute(quiery)
        self.conn.commit()
        
    def get_userid_pw(self, table_name,input_userid):
        quiery = "SELECT * FROM {} where userid == 'deep.g'".format(table_name)
        data = self.mycurser.execute(quiery)
        return data

database = DatabaseOp("canteen_new1.db")
data_fatching = database.get_userid_pw("empinfo","deep.g")
for i in data_fatching:
    login_user_emp = i[0]
    login_user_fname = i[1]
    login_user_lname = i[2]
    login_user_id = i[3]
    login_user_pw = i[4]
    login_group = i[5]