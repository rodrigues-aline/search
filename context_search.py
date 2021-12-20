# -*- coding: utf-8 -*-

from abc       import ABCMeta, abstractmethod
from random    import shuffle
from time      import sleep
from search    import Search
from db        import DataSearch
from threading import Thread, stack_size

import os
import pandas as pd

stack_size(134217728)


class ContextSearch(object):
    """
        Author:  Aline Rodrigues
        Created: 16/11/2021
        Initialize and manage search
    """
    
    def __init__(self):
        self.path_dir    = os.path.dirname(os.path.realpath(__file__))
        self.db          = DataSearch(self.path_dir)
        self.search      = Search()
        self.mode_vector = [['Arranjos Ordenados (ASC)',   SortedVector()], 
                             ['Arranjos Desordenados',     NotSortedVector()], 
                             ['Arranjos Ordenados (DESC)', ReverseSortedVector()],
                             ['Arranjos Quase Ordenados',  AlmostSortedVector(5)]]
 
        self.threads         = []
        self.status_thread   = False
        self.status_thread_s = [False for i in range(0, len(self.search.types) * len(self.mode_vector) * 6)]
        self.len_vector      = [10, 100, 1000, 10000, 100000, 1000000]
        
        
    def init_search(self):
        self.db.insert_environment()

        for mode in self.mode_vector:
            for type_search in self.search.types:
                for i in range(0, len(self.len_vector)):
                    #self.init_thread(type_search, mode, len(self.threads), i,  )
                    self.threads.append(Thread(target=self.init_thread, args=(type_search, mode, len(self.threads), i,  )))
                    self.threads[len(self.threads)-1].start()
        
        while False in self.status_thread_s:
            sleep(60) 
            index = 0
            print()
            for mode in self.mode_vector:
                for type_search in self.search.types:
                    for i in range(0, len(self.len_vector)):
                        if self.status_thread_s[index]  == False:
                            print (f'Runing: {type_search[0]} ({self.len_vector[i]}) {mode[0]}')
                        index += 1
            print()
        self.status_thread = True
        
    
    def init_thread(self, type_search, mode_search, thread, v):
        db = DataSearch(self.path_dir)
        vector = mode_search[1].create_mode_vector(self.len_vector[v])
        self.search.execute(vector, type_search, mode_search[0], db)
        self.status_thread_s[thread] = True
        
    
    def convert_data_to_csv(self):
        path_data = self.path_dir + '/dataset'
        
        try:
            os.makedirs(path_data)
        except OSError:
            print (f'Already exists path: {path_data}')
        
        data = self.db.select_all_search()
        df = pd.DataFrame(data, columns=data[0].keys())
        print(df.head())
        df.to_csv(path_data + '/tree_search.csv')
            
        

class AbstractModeVector(object):
    """
        Author:  Aline Rodrigues
        Created: 16/11/2021
        Template Method to create mode vector
    """
    __metaclass__ = ABCMeta

    
    @abstractmethod
    def create_mode_vector(self, size):          
        pass 
    
class SortedVector(AbstractModeVector):
    
    def create_mode_vector(self, size):
        return list(range(1, size + 1))


class NotSortedVector(AbstractModeVector):
    
    def create_mode_vector(self, size):
        vector = list(range(1, size + 1))
        shuffle(vector)
        return  vector
    
    
class ReverseSortedVector(AbstractModeVector):
    
    def create_mode_vector(self, size):
        return list(range(size, 0, -1))


class AlmostSortedVector(AbstractModeVector):
    def __init__(self, steep):
        self.steep = steep
    
    def create_mode_vector(self, size):
        vector = list(range(1, size + 1))
        index = self.steep
        while (index + self.steep) <= size:
            aux = vector[index-1]
            vector[index-1] = vector[(index-1) + self.steep]
            vector[(index-1) + self.steep] = aux
            index = index + self.steep
        return vector
            
    