class Tree(object):
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

    def add(self, key, compare):
        compare += 1
        side = 'left' if key < self.key else 'right'

        node = getattr(self, side)
        
        compare += 1
        if node is None:
            setattr(self, side, Tree(key))
        else:
            node.add(key, compare)
            
        return compare
    
    def find(self, key, compare):
        compare += 1
        if key == self.key:
            return True, compare
        compare += 1
        side = 'left' if key < self.key else 'right'
        node = getattr(self, side)
        compare += 1
        if node is not None:
            return node.find(key, compare)
        else:
            return False, compare
    
    def find_min(self, parent): 
        if self.left: 
            return self.left.find_min(self)
        else:
            return [parent, self]
    
    def delete(self, key, compare):
        compare += 1
        if key == self.key:
            if self.right and self.left: 
                compare += 2
                [psucc, succ] = self.right.find_min(self)	

                compare += 1
                if psucc.left == succ: 
                    psucc.left = succ.right
                else:
                    psucc.right = succ.right

                succ.left = self.left
                succ.right = succ.right

                return succ, compare
            else:
                compare += 2
                if self.left: 
                    return self.left, compare
                else: 
                    return self.right, compare
        
        compare += 1
        side = 'left' if key < self.key else 'right'
        node = getattr(self, side)
        compare += 1
        if node is not None:
            return node.delete(key, compare)
        else:
            return self, compare
    