# -*- coding: utf-8 -*-


from abc            import ABCMeta, abstractmethod
from time           import process_time
from statistics     import stdev
from sys            import setrecursionlimit
from tree           import Tree
from avl_tree       import AVLTree as AVL_Tree
from red_black_tree import RBTree
from aa_tree        import AATree as AA_Tree

setrecursionlimit(100000)


class Search(object):
    """
        Author:  Aline Rodrigues
        Created: 16/11/2021
        Manage search execute
    """
    def __init__(self):
        self.types = [
                      #['LinearSearch', LinearSearch], 
                      #['BinarySearch', BinarySearch], 
                      #['BinarySearchTree', BinarySearchTree], 
                      #['AVLTree', AVLTree],          
                      #['ReadBlackTree', ReadBlackTree],
                      ['AATree', AATree],
                      ]
    
    def execute(self, vector, type_search, mode_vector, db):
        search = type_search[1]()
        # Insert
        print (f'INIT INSERT {type_search[0]} ({len(vector)}) {mode_vector}')
        times = []
        for v in vector:
            time_start = process_time()
            search.insert(v, len(vector))
            time_end = process_time() - time_start
            times.append(time_end)
        
        db.insert(len(vector), type_search[0], mode_vector, 'insert', 
                  sum(times) / len(times), stdev(times), 
                  sum(search.compare) / len(search.compare), stdev(search.compare))
        
        print (f'END INSERT {type_search[0]} ({len(vector)}) {mode_vector}')
        
        # Search
        print (f'INIT SEARCH {type_search[0]} ({len(vector)}) {mode_vector}')
        times = []
        search.compare = []
        for v in vector:
            time_start = process_time()
            search.search(v)
            time_end = process_time() - time_start
            times.append(time_end)
        
        db.insert(len(vector), type_search[0], mode_vector, 'search', 
                  sum(times)/len(times), stdev(times), 
                  sum(search.compare)/len(search.compare), stdev(search.compare))
        
        print (f'END SEARCH {type_search[0]} ({len(vector)}) {mode_vector}')

        # Remove
        print (f'INIT REMOVE {type_search[0]} ({len(vector)}) {mode_vector}')
        times = []
        search.compare = []
        for v in vector:
            time_start = process_time()
            search.remove(v)
            time_end = process_time() - time_start
            times.append(time_end)

        db.insert(len(vector), type_search[0], mode_vector, 'remove', 
                  sum(times)/len(times), stdev(times), 
                  sum(search.compare)/len(search.compare), stdev(search.compare))
        
        print (f'END REMOVE {type_search[0]} ({len(vector)}) {mode_vector}')


class AbstractSearch(object):
    """
        Author:  Aline Rodrigues
        Created: 16/11/2021
        Template Method to execute searches
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.compare = []

    @abstractmethod
    def insert(self, item, len_vector):          
        pass
    
    @abstractmethod
    def search(self, item):          
        pass 
    
    @abstractmethod
    def remove(self, item):          
        pass
             

class LinearSearch(AbstractSearch):
    
    def __init__(self):
        AbstractSearch.__init__(self)
        self.vector = []
        
    def insert(self, item, len_vector = None):
        self.vector.append(item)   
        self.compare.append(0)   
        
    def search(self, item): 
        compare = 0 
        for v in self.vector:
            compare += 1
            if v == item:
                break
        self.compare.append(compare)
    
    def remove(self, item):
        compare = 0 
        index = 0
        for i in range(0, len(self.vector)):
            compare += 1
            if self.vector[i] == item:
                index = i
                break
        
        for i in range(index, len(self.vector)-1):
            self.vector[i] = self.vector[i + 1]
        
        self.vector.pop()
        self.compare.append(compare)

class BinarySearch(AbstractSearch):

    def __init__(self):
        AbstractSearch.__init__(self)
        self.vector = []
        self.n = 0
        self.compare_search = 0
        
    def binary_search(self, low, high, item):
        if high >= low:
            mid = (high + low) // 2

            if self.vector[mid] == item:
                self.compare_search += 1
                return mid
            elif self.vector[mid] > item:
                self.compare_search += 2
                return self.binary_search(low, mid - 1, item)
            else:
                self.compare_search += 2
                return self.binary_search(mid + 1, high, item)
        else:
            return -1

    def insert(self, item, len_vector):
        if len(self.vector) == 0:
            self.vector = [ 0 for i in range(0, len_vector)]    
        i = self.n - 1
        compare = 1
        
        while i >= 0 and self.vector[i] > item:
            compare += 1
            self.vector[i + 1] = self.vector[i]
            i -= 1
  
        self.vector[i + 1] = item
        self.n += 1
        self.compare.append(compare)
  
        
    def search(self, item): 
        self.compare_search = 0
        self.binary_search(0, len(self.vector), item)
        self.compare.append(self.compare_search)
    
    def remove(self, item): 
        self.compare_search = 0
        index = self.binary_search(0, len(self.vector), item)
        self.compare.append(self.compare_search)
        for i in range(index, len(self.vector)-1):
            self.vector[i] = self.vector[i + 1]
        self.vector.pop()
    
class BinarySearchTree(AbstractSearch):
    def __init__(self):
        AbstractSearch.__init__(self)
        self.tree = None
        
    def insert(self, item, len_vector = None):
        if self.tree is None: 
            self.tree = Tree(item)
            self.compare.append(0) 
        else:
            compare = self.tree.add(item, 0)
            self.compare.append(compare) 
    
    def search(self, item):
        status, compare = self.tree.find(item, 0)
        self.compare.append(compare) 
    
    def remove(self, item):
        status, compare = self.tree.delete(item, 0)
        self.compare.append(compare)
                       
    

class AVLTree(AbstractSearch):
    
    def __init__(self):
        AbstractSearch.__init__(self)
        self.avl_tree = AVL_Tree()
        self.root = None
        
    def insert(self, item, len_vector = None):
        self.root, compare = self.avl_tree.insert(self.root, item, 0)
        self.compare.append(compare)
    
    def search(self, item):
        compare = self.avl_tree.find(self.root, item)
        self.compare.append(compare)
    
    def remove(self, item):
        self.root, compare = self.avl_tree.delete(self.root, item, 0)
        self.compare.append(compare)
            
class ReadBlackTree(AbstractSearch):
    def __init__(self):
        AbstractSearch.__init__(self)
        self.red_black_tree = RBTree()
        
    def insert(self, item, len_vector = None):
        compare, x = self.red_black_tree.insertNode(item, 0)
        self.compare.append(compare)
            
    def search(self, item):
        status, compare = self.red_black_tree.findNode(item, 0)
        self.compare.append(compare)

    def remove(self, item):
        compare = self.red_black_tree.deleteNode(item, 0)
        self.compare.append(compare)

class AATree(AbstractSearch):
    def __init__(self):
        AbstractSearch.__init__(self)
        self.aa_tree = AA_Tree()
        
    def insert(self, item, len_vector = None):
        compare = self.aa_tree.insert(item)
        self.compare.append(compare)
            
    def search(self, item):
        compare = self.aa_tree.find(item)
        self.compare.append(compare)

    def remove(self, item):
        compare = self.aa_tree.delete(item)
        self.compare.append(compare)
