# -*- coding: utf-8 -*-

import sqlite3
import platform

from time import sleep

class DataSearch(object):
    """
        Author:  Aline Rodrigues
        Created: 16/11/2021
        Manage data search
    """
    
    def __init__(self, path_dir):
        self.path_dir = path_dir
        self.db       = None
        self.cursor   = None
        self.connect()
        
    def connect(self):
        """
            Connect database sqlite 
        """
        if self.db is None:
            self.db     = sqlite3.connect(self.path_dir + '/data_search.db')
            self.db.row_factory = sqlite3.Row
            self.cursor = self.db.cursor()
            
            #self.cursor.execute("DROP TABLE IF EXISTS environment;")
            #self.cursor.execute("DROP TABLE IF EXISTS search;")
                    
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS environment (
                                        user_name    TEXT,
                                        system       TEXT,
                                        platform     TEXT,
                                        processor    TEXT);""")
            
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS search (
                                        user_name      TEXT,
                                        type_action    TEXT,
                                        type_search    TEXT,
                                        mode_vector    TEXT,
                                        len_vector     INTEGER,
                                        mean_time      DOUBLE,
                                        std_time       DOUBLE,
                                        mean_compare   DOUBLE,
                                        stddev_compare DOUBLE);""")
            

    def insert_environment(self):
        self.cursor.execute(f"DELETE FROM environment WHERE user_name='{platform.uname()[1]}';")
        self.cursor.execute(f"DELETE FROM search WHERE user_name='{platform.uname()[1]}';")
        self.db.commit()
        
        self.cursor.execute(f"""INSERT INTO environment (user_name, system, platform, processor)
                                VALUES ('{platform.uname()[1]}','{platform.system()}','{platform.platform()}','{platform.processor()}');""")
        self.db.commit()
      
               
    def insert(self, len_vector, type_search, mode_vector, type_action, mean_time, std_time, mean_compare, std_compare):
        count_locked = 0
        while True:
            try:
                self.cursor.execute(f"""INSERT INTO search (user_name, type_action, type_search,  mode_vector, len_vector, 
                                                   mean_time, std_time, mean_compare, std_compare)
                                      VALUES ('{platform.uname()[1]}', '{type_action}', '{type_search}', '{mode_vector}', {len_vector}, 
                                              {mean_time}, {std_time}, {mean_compare}, {std_compare});""")
                self.db.commit()
                break
            except sqlite3.OperationalError:
                count_locked += 1
                print (f'SQLite DB locked: {count_locked}')
                sleep(1)

        
    def select_environment(self):
        return self.cursor.execute(f"SELECT * FROM environment WHERE user_name='{platform.uname()[1]}';").fetchall()[0]
    
    
    def select_all_search(self):
        return self.cursor.execute("SELECT * FROM search;").fetchall()
     