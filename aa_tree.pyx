# -*- Mode: Cython -*-

# see:
#  http://eternallyconfuzzled.com/tuts/datastructures/jsw_tut_andersson.aspx
#  http://en.wikipedia.org/wiki/AA_tree

from libc.stdint cimport uint32_t

cdef class aa_node:
    cdef readonly int level
    cdef readonly aa_node left, right
    cdef readonly int key
    def __cinit__ (self, int level, aa_node left, aa_node right, int key):
        self.level = level
        self.left = left
        self.right = right
        self.key = key


# this global node acts as a sentinel
cdef aa_node tree_nil
tree_nil = aa_node (0, tree_nil, tree_nil, -1)

cdef int compare = 0


cdef aa_node tree_skew (aa_node root):
    cdef aa_node save
    global compare
    compare = compare + 1
    if root.level != 0:
        compare = compare + 1
        if root.left.level == root.level:
            save = root
            root = root.left
            save.left = root.right
            root.right = save
        root.right = tree_skew (root.right)
    return root

cdef aa_node tree_split (aa_node root):
    cdef aa_node save
    global compare
    compare = compare + 2
    if root.right.right.level == root.level and root.level != 0:
        save = root
        root = root.right
        save.right = root.left
        root.left = save
        root.level += 1
        root.right = tree_split (root.right)
    return root


cdef aa_node tree_insert (aa_node root, int key):
    cdef aa_node new_node
    global compare
    compare = compare + 1
    if root == tree_nil:
        return aa_node (1, tree_nil, tree_nil, key)
    elif root.key < key:
        compare = compare + 1
        root.right = tree_insert (root.right, key)
        return tree_split (tree_skew (root))
    else:
        compare = compare + 1
        root.left = tree_insert (root.left, key)
        return tree_split (tree_skew (root))


cdef aa_node tree_remove (aa_node root, int key):
    cdef aa_node heir
    global compare
    compare = compare + 1
    if root != tree_nil:
        compare = compare + 1
        if root.key == key:
            compare = compare + 2
            if root.left != tree_nil and root.right != tree_nil:
                heir = root.left
                compare = compare + 1
                while heir.right != tree_nil:
                    compare = compare + 1
                    heir = heir.right
                root.key = heir.key
                root.left = tree_remove (root.left, root.key)
            elif root.left == tree_nil:
                compare = compare + 1
                root = root.right
            else:
                compare = compare + 1
                root = root.left
        elif root.key < key:
            compare = compare + 1
            root.right = tree_remove (root.right, key)
        else:
            compare = compare + 1
            root.left = tree_remove (root.left, key)
    
    compare = compare + 1
    if (root.left.level < (root.level - 1) or
        root.right.level < (root.level - 1)):
        root.level -= 1
        compare = compare + 1
        if root.right.level > root.level:
            root.right.level = root.level
        root = tree_split (tree_skew (root))
    return root

            
def walk (aa_node n):
    if n.left.level > 0:
        for x in walk (n.left):
            yield x
    yield n
    if n.right.level > 0:
        for x in walk (n.right):
            yield x


cdef class AATree:

    cdef public aa_node root

    def __init__ (self):
        self.root = tree_nil

    def __iter__ (self):
        return walk (self.root)

    def find (self, int key):
        compare = 0
        cdef aa_node search = self.root
        while True:
            compare = compare + 1
            if search == tree_nil:
                raise KeyError (key)
            elif search.key == key:
                compare = compare + 1
                break
            elif search.key < key:
                compare = compare + 2
                search = search.right
            else:
                compare = compare + 2
                search = search.left
        return compare

    def insert (self, int key):
        global compare
        compare = 0
        self.root = tree_insert (self.root, key)
        return compare

    def delete (self, int key):
        # XXX how do we know if it's been removed?
        global compare
        compare = 0
        self.root = tree_remove (self.root, key)
        return compare
