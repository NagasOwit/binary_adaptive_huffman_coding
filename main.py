class Node:

    def __init__(self, symbol, parent, left_child, right_child, count, index):
        self.symbol = symbol
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.count = count
        self.index = index

class HuffmanTree:
    escape_symbol = Node("", None, None, None, 0, 0, "")
    root = escape_symbol

symbol_list = [] #list of symbols
tree = HuffmanTree() #Epsilon, starts as root

def RecalculateTree(node):
    pass

def AddNewSymbolToTree(symbol):

    new_node = tree.escape_symbol
    new_node.left_child =  Node(symbol, new_node, None, None, 0, new_node.index + 1)
    new_node.right_child = Node("", new_node, None, None, 0, new_node.index + 2)
    tree.escape_symbol = new_node.right_child

def IncreaseOccurenceAndReturnCode(symbol, node, outputcode):

    if (node.symbol == symbol):
        outputcode += "0"
        node.left_child.count += 1
        RecalculateTree(node)
        return outputcode
    else:
        outputcode += "1"
        IncreaseOccurenceAndReturnCode(symbol, node.right_child, outputcode)


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
            IncreaseOccurence(element)
            compressed_file.write(element)        
        Recalculate(new_symbol) #adjust the tree if it was changed

#text_to_compress = open("book_of_genesis_to_compress.txt", "r").read()
numbers_to_compress = "0101111100001100100010010000011111001001001001110011111010"
text_to_compress = "barbaraabarboraubaru"

def Test():
    for element in text_to_compress:
        AddNewSymbolToTree(element)

Test()