import sys

class Node(object):
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree(object):

    # Function to insert a node
    def insert(self, root, key, compare):
        # Find the correct location and insert the node
        compare += 1
        if not root:
            return Node(key), compare
        elif key < root.key:
            root.left, compare = self.insert(root.left, key, compare + 1)
        else:
            root.right, compare = self.insert(root.right, key, compare + 1)

        compare += 1
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            compare += 1
            if key < root.left.key:
                return self.rightRotate(root, compare)
            else:
                root.left, compare = self.leftRotate(root.left, compare)
                return self.rightRotate(root, compare)

        if balanceFactor < -1:
            compare += 1
            if key > root.right.key:
                return self.leftRotate(root, compare)
            else:
                root.right, compare = self.rightRotate(root.right, compare)
                return self.leftRotate(root, compare)

        return root, compare
    
    
    def find(self, root, key):
        compare = 0
        while True:
            compare += 1
            if not root:
                return compare
            elif key == root.key:
                compare += 1
                return compare
            elif key < root.key:
                compare += 2
                root = root.left
            else:
                compare += 2
                root = root.right
            

    # Function to delete a node
    def delete(self, root, key, compare):
        # Find the node to be deleted and remove it
        compare += 1
        if not root:
            return root
        elif key == root.key:
            compare += 2
            if root.left is None:
                temp = root.right
                root = None
                return temp, compare
            compare += 1
            if root.right is None:
                temp = root.left
                root = None
                return temp, compare
            temp, compare = self.getMinValueNode(root.right, compare)
            root.key = temp.key
            root.right, compare = self.delete(root.right, temp.key, compare)
        elif key < root.key:
            root.left, compare = self.delete(root.left, key, compare + 2)
        else:
            root.right, compare = self.delete(root.right, key, compare + 2)
            
        # Update the balance factor of nodes
        compare += 1
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root, compare)
            else:
                root.left, compare = self.leftRotate(root.left, compare)
                return self.rightRotate(root, compare)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root, compare)
            else:
                root.right, compare = self.rightRotate(root.right, compare)
                return self.leftRotate(root, compare)
        return root, compare

    # Function to perform left rotation
    def leftRotate(self, z, compare):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        compare += 1
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        compare += 1
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y, compare

    # Function to perform right rotation
    def rightRotate(self, z, compare):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        compare += 1
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        compare += 1
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y, compare

    # Get the height of the node
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factore of the node
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def getMinValueNode(self, root, compare):
        compare += 1
        if root is None or root.left is None:
            return root, compare
        return self.getMinValueNode(root.left, compare)

    def preOrder(self, root):
        if not root:
            return
        print("{0} ".format(root.key), end="")
        self.preOrder(root.left)
        self.preOrder(root.right)

    # Print the tree
    def printHelper(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.key)
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)
