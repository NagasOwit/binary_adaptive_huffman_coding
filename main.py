class Node:                  
    def __init__(self, data, parent, left_child, right_child, count, index):

        self.data = data
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.count = count
        self.index = index

symbol_list = [] #list of symbols
tree = Node("", None, None, None, 0, 1) #Epsilon, počáteční kořen

def SearchTree(node):
     
    if node is ""  or node.count == 0:
        return node
    
    else:
        return SearchTree(node.right_child)

def AddNewSymbolToTree():
    pass
    

def Recalculate(new_symbol):

    if (new_symbol):
        AddNewSymbolToTree()
        pass
        

    while (tree.value != ""):
        if (tree.left_child.value >= tree.value or tree.right_child.value >= tree.value):
            #switch values
            pass
        tree.value += 1
    tree.value += 1
    return tree

def Compress(input):

    compressed_file = open("compressed_file.txt", "w")

    for element in input:

        new_symbol = not element in symbol_list

        if (new_symbol): #pokud se jedná o nový symbol, dej jej na místo Epsilon a zakóduj
            symbol_list.append(element)
            compressed_file.write(element)

        else: #přiřaď a připočti výskyt do větve
            compressed_file.write(element)
        
        Recalculate(new_symbol)

#text_to_compress = open("book_of_genesis_to_compress.txt", "r").read()
numbers_to_compress = "0101111100001100100010010000011111001001001001110011111010"
text_to_compress = "AABBCCCVDDBBCCVVAA"