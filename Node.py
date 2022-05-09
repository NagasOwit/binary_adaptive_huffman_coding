class Node:

    def __init__(self, symbol, parent, left_child, right_child, count, index):
        self.symbol = symbol
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.count = count
        self.index = index