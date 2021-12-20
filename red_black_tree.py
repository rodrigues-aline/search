#   Red Black Tree implementaion in Python
#   Created By Manpreet Singh

BLACK = 0
RED = 1

global compare_del
compare_del = 0

class RBNode(object):

    def __init__(self, key = None, color = RED):
        self.left = self.right = self.parent = None
        self.color = color
        self.key = key
        self.nonzero = 1

    def __str__(self):
        return repr(self.key)

    def __nonzero__(self):
        return self.nonzero

    def __len__(self):
        """imitate sequence"""
        return 2

    def __getitem__(self, index):
        """imitate sequence"""
        if index==0:
            return self.key
        raise IndexError('only key and value as sequence')


class RBTreeIter(object):

    def __init__ (self, tree):
        self.tree = tree
        self.index = -1  # ready to iterate on the next() call
        self.node = None
        self.stopped = False

    def __iter__ (self):
        """ Return the current item in the container
        """
        return self.node.key

    def next (self):
        """ Return the next item in the container
            Once we go off the list we stay off even if the list changes
        """
        if self.stopped or (self.index + 1 >= self.tree.__len__()):
            self.stopped = True
            raise StopIteration
        #
        self.index += 1
        if self.index == 0:
            self.node = self.tree.firstNode()
        else:
            self.node = self.tree.nextNode (self.node)
        return self.node.key


class RBTree(object):

    def __init__(self):
        self.sentinel = RBNode()
        self.sentinel.left = self.sentinel.right = self.sentinel
        self.sentinel.color = BLACK
        self.sentinel.nonzero = 0
        self.root = self.sentinel
        self.count = 0
    
    def __cmp(self, a, b):
        return (a > b) - (a < b)

    def __len__(self):
        return self.count
    
    def __del__(self):
        # unlink the whole tree
        global compare_del
        compare_del = 0
        s = [ self.root ]
        compare_del += 1
        if self.root is not self.sentinel:
            compare_del += 1
            while s:
                compare_del += 1
                cur = s[0]
                if cur.left and cur.left != self.sentinel:
                    compare_del += 2
                    s.append(cur.left)
                else:
                    compare_del += 1
                if cur.right and cur.right != self.sentinel:
                    compare_del += 2
                    s.append(cur.right)
                else:
                    compare_del += 2
                cur.right = cur.left = cur.parent = None
                cur.key = cur.value = None
                s = s[1:]

        self.root = None
        self.sentinel = None

    def __str__(self):
        return "<RBTree object>"

    def __repr__(self):
        return "<RBTree object>"

    def __iter__ (self):
        return RBTreeIter (self)

    def rotateLeft(self, x, compare):
        y = x.right

        # establish x.right link
        x.right = y.left
        if y.left != self.sentinel:
            y.left.parent = x

        # establish y.parent link
        if y != self.sentinel:
            y.parent = x.parent

        compare += 1
        if x.parent:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
            compare += 1
        else:
            self.root = y

        # link x and y
        y.left = x
        if x != self.sentinel:
            x.parent = y
            
        compare += 4
        return compare

    def rotateRight(self, x, compare):
        #***************************
        #  rotate node x to right
        #***************************

        y = x.left

        # establish x.left link
        x.left = y.right
        if y.right != self.sentinel:
            y.right.parent = x

        # establish y.parent link
        if y != self.sentinel:
            y.parent = x.parent
        compare += 1
        if x.parent:
            if x == x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y
            compare += 1
        else:
            self.root = y

        # link x and y
        y.right = x
        if x != self.sentinel:
            x.parent = y
        compare += 4
        return compare

    def insertFixup(self, x, compare):
        #************************************
        #  maintain Red-Black tree balance  *
        #  after inserting node x           *
        #************************************

        # check Red-Black properties
        compare += 2
        while x != self.root and x.parent.color == RED:
            compare += 2
            # we have a violation
            compare += 1
            if x.parent == x.parent.parent.left:
                y = x.parent.parent.right
                compare += 1
                if y.color == RED:
                    # uncle is RED
                    x.parent.color = BLACK
                    y.color = BLACK
                    x.parent.parent.color = RED
                    x = x.parent.parent
                else:
                    # uncle is BLACK
                    compare += 1
                    if x == x.parent.right:
                        # make x a left child
                        x = x.parent
                        compare = self.rotateLeft(x, compare)

                    # recolor and rotate
                    x.parent.color = BLACK
                    x.parent.parent.color = RED
                    compare = self.rotateRight(x.parent.parent, compare)
            else:
                # mirror image of above code
                y = x.parent.parent.left
                compare += 1
                if y.color == RED:
                    # uncle is RED
                    x.parent.color = BLACK
                    y.color = BLACK
                    x.parent.parent.color = RED
                    x = x.parent.parent
                else:
                    # uncle is BLACK
                    compare += 1
                    if x == x.parent.left:
                        x = x.parent
                        compare = self.rotateRight(x, compare)
                    
                    x.parent.color = BLACK
                    x.parent.parent.color = RED
                    compare = self.rotateLeft(x.parent.parent, compare)
                
        self.root.color = BLACK
        return compare

    def insertNode(self, key, compare):
        #**********************************************
        #  allocate node for data and insert in tree  *
        #**********************************************

        # we aren't interested in the value, we just
        # want the TypeError raised if appropriate
        hash(key)

        # find where node belongs
        current = self.root
        parent = None
        compare += 1
        while current != self.sentinel:
            compare += 1
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            rc = self.__cmp(key, current.key)
            if rc == 0:
                compare += 1
                return current
            parent = current
            if rc < 0:
                compare += 2
                current = current.left
            else:
                compare += 2
                current = current.right
                
        # setup new node
        x = RBNode(key)
        x.left = x.right = self.sentinel
        x.parent = parent

        self.count = self.count + 1

        # insert node in tree
        compare += 1
        if parent:
            if self.__cmp(key, parent.key) < 0:
                parent.left = x
            else:
                parent.right = x
            compare += 1
        else:
            self.root = x

        compare = self.insertFixup(x, compare)
        return compare, x

    def deleteFixup(self, x, compare):
        #************************************
        #  maintain Red-Black tree balance  *
        #  after deleting node x            *
        #************************************
        compare += 1
        while x.color == BLACK and x != self.root:
            compare += 3
            if x == x.parent.left:
                w = x.parent.right
                compare += 1
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    compare = self.rotateLeft(x.parent, compare)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    compare += 2
                    w.color = RED
                    x = x.parent
                else:
                    compare += 2
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        compare = self.rotateRight(w, compare)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    compare = self.rotateLeft(x.parent, compare)
                    x = self.root
            else:
                w = x.parent.left
                compare += 1
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    compare = self.rotateRight(x.parent, compare)
                    w = x.parent.left
                if w.right.color == BLACK and w.left.color == BLACK:
                    compare += 2
                    w.color = RED
                    x = x.parent
                else:
                    compare += 2
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        compare = self.rotateLeft(w, compare)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    compare = self.rotateRight(x.parent, compare)
                    x = self.root

        x.color = BLACK
        return compare

    def deleteNode(self, key, compare):
        #****************************
        #  delete node z from tree  *
        #****************************
        
        z, compare = self.findNode(key, compare)
        
        compare += 1
        if not z or z == self.sentinel:
            return compare
        if z.left == self.sentinel or z.right == self.sentinel:
            compare += 1
            # y has a self.sentinel node as a child
            y = z
        else:
            compare += 2
            # find tree successor with a self.sentinel node as a child
            y = z.right
            compare += 1
            while y.left != self.sentinel:
                compare += 1
                y = y.left

        # x is y's only child
        if y.left != self.sentinel:
            x = y.left
        else:
            x = y.right
        compare += 1

        # remove y from the parent chain
        x.parent = y.parent
        compare += 1
        if y.parent:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
            compare += 1
        else:
            self.root = x

        if y != z:
            z.key = y.key
        compare += 1

        if y.color == BLACK:
            compare = self.deleteFixup(x, compare)
        compare += 1
        del y
        global compare_del
        compare += compare_del
        self.count = self.count - 1
        
        return compare

    def findNode(self, key, compare):
        #******************************
        #  find node containing data
        #******************************

        # we aren't interested in the value, we just
        # want the TypeError raised if appropriate
        hash(key)

        current = self.root
        compare += 1
        while current != self.sentinel:
            compare += 1
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            rc = self.__cmp(key, current.key)
            compare += 1
            if rc == 0:
                
                return current, compare
            else:
                compare += 1
                if rc < 0:
                    current = current.left
                else:
                    current = current.right

        return None, compare

    def traverseTree(self, f):
        if self.root == self.sentinel:
            return
        s = [ None ]
        cur = self.root
        while s:
            if cur.left:
                s.append(cur)
                cur = cur.left
            else:
                f(cur)
                while not cur.right:
                    cur = s.pop()
                    if cur is None:
                        return
                    f(cur)
                cur = cur.right
        # should not get here.
        return

    def nodesByTraversal(self):
        """return all nodes as a list"""
        result = []
        def traversalFn(x, K=result):
            K.append(x)
        self.traverseTree(traversalFn)
        return result

    def nodes(self):
        """return all nodes as a list"""
        cur = self.firstNode()
        result = []
        while cur:
            result.append(cur)
            cur = self.nextNode(cur)
        return result

    def firstNode(self):
        cur = self.root
        while cur.left:
            cur = cur.left
        return cur

    def lastNode(self):
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur

    def nextNode(self, prev):
        """returns None if there isn't one"""
        cur = prev
        if cur.right:
            cur = prev.right
            while cur.left:
                cur = cur.left
            return cur
        while True:
            cur = cur.parent
            if not cur:
                return None
            if self.__cmp(cur.key, prev.key)>=0:
                return cur

    def prevNode(self, next):
        """returns None if there isn't one"""
        cur = next
        if cur.left:
            cur = next.left
            while cur.right:
                cur = cur.right
            return cur
        while True:
            cur = cur.parent
            if cur is None:
                return None
            if self.__cmp(cur.key, next.key) < 0:
                return cur
