class Node:                  
    def __init__(self, symbol, parent, left_child, right_child, count, index, code):
        self.symbol = symbol
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.count = count
        self.index = index
        self.code = code

class HuffmanTree:
    escape_symbol = Node("", None, None, None, 0, 0, "")
    root = escape_symbol

symbol_list = [] #list of symbols
tree = HuffmanTree() #Epsilon, starts as root
tree_list = [Node("", None, None, None, 0, 0, "")] #list containing the Huffman tree

def AdjustTreeViaTraversal(node, code):
    if node:
        node.code += code
        AdjustTreeViaTraversal(node.left_child, code + "0")
        AdjustTreeViaTraversal(node.right_child, code + "1")

def AddNewSymbolToTree(symbol):
    new_node = tree.escape_symbol
    new_node.symbol = symbol
    new_node.left_child =  Node(symbol, new_node, None, None, 0, new_node.index + 1, new_node.code + "0")
    tree.escape_symbol = Node("", new_node, None, None, 0, new_node.index + 2, new_node.code + "1")
    new_node.right_child =  tree.escape_symbol
    return new_node.right_child.code
    

def Recalculate(new_symbol):
    if (new_symbol):
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
        if (new_symbol): #if the symbol is new, create new node and encode the symbol
            symbol_list.append(element)
            element += AddNewSymbolToTree(element)
            compressed_file.write(element)
        else: #increase occurrence of the symbol in the tree
            compressed_file.write(element)        
        Recalculate(new_symbol) #adjust the tree if it was changed

#text_to_compress = open("book_of_genesis_to_compress.txt", "r").read()
numbers_to_compress = "0101111100001100100010010000011111001001001001110011111010"
text_to_compress = "barbaraabarboraubaru"

def TestTraversal(node):
    if node:
        print(node.symbol)
        print(node.index)
        TestTraversal(node.left_child)
        TestTraversal(node.right_child)

def Test():
    for element in text_to_compress:
        AddNewSymbolToTree(element)

Test()
TestTraversal(tree.root)