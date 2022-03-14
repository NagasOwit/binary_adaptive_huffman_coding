from asyncio.windows_events import NULL

class Node:                  
    def __init__(self, value, left_child, right_child, count, index):
        self.value = value
        self.left_child = left_child
        self.right_child = right_child
        self.count = count
        self.index = index

def Recalculate(tree):
    while (tree.value != ""):
        if (tree.left_child.value >= tree.value or tree.right_child.value >= tree.value):
            #switch values
            NULL
        tree.value += 1
    tree.value += 1
    return tree

def Compress(nodes):    
    tree = Node("", Node(), Node(), 0, 1) #Epsilon, počáteční kořen
    while(len(nodes) > 0): 
        if False: #pokud se jedná o nový symbol, dej jej na místo Epsilon a zakóduj TODO funkce na prohledání stromu, zda je symbol přítomen
            NULL
        else: #přiřaď a připočti výskyt do větve
            NULL
            tree = Recalculate(tree)

#text_to_compress = open("book_of_genesis_to_compress.txt", "r").read()
text_to_compress = "0101111100001100100010010000011111001001001001110011111010"