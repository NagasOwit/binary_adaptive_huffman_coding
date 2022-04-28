import bitarray

class Node:

    def __init__(self, symbol, parent, left_child, right_child, count, index):
        self.symbol = symbol
        self.parent = parent
        self.left_child = left_child
        self.right_child = right_child
        self.count = count
        self.index = index

class HuffmanTree:
    escape_symbol = Node("", None, None, None, 0, 0)
    root = escape_symbol

def RecalculateTree(node, node_added):

    if (node.parent is None):
        return
    elif (node_added.count > node.parent.left_child.count):
        node.left_child = node.parent.left_child
        node.left_child.parent = node
        node.parent.left_child = node_added
        node_added.parent = node.parent
        RecalculateTree(node.parent, node_added)
    else:
        return

def ReturnCodeOfNewSymbol(node):

    if (node.right_child is None):
       return ""

    else:
        return "1" + ReturnCodeOfNewSymbol(node.right_child)

def AddNewSymbolToTree(symbol):

    symbol_list.append(symbol)    
    new_node = tree.escape_symbol
    new_node.left_child =  Node(symbol, new_node, None, None, 0, new_node.index + 1)
    new_node.right_child = Node("", new_node, None, None, 0, new_node.index + 2)
    tree.escape_symbol = new_node.right_child

def IncreaseOccurenceAndReturnCode(symbol, node):

    if (node.left_child.symbol == symbol):
        node.left_child.count += 1
        RecalculateTree(node, node.left_child)
        return "0"
        
    else:
        return "1" + IncreaseOccurenceAndReturnCode(symbol, node.right_child)

def Compress(input):

    compressed_file = open("compressed_file", "wb")

    for element in input:        
        new_symbol = not element in symbol_list        
        if (new_symbol):
            compressed_file.write(ReturnCodeOfNewSymbol(tree.root).encode())
            compressed_file.write(element.encode())
            AddNewSymbolToTree(element)
        else:
            compressed_file.write(IncreaseOccurenceAndReturnCode(element, tree.root).encode())

#Testing part of the application

symbol_list = [] #list of symbols
tree = HuffmanTree() #Epsilon, starts as root

#text_to_compress = open("fullBible.txt", "r").read()
#text_to_compress = open("book_of_genesis_to_compress.txt", "r").read()
text_to_compress = "tom marta at"

Compress(text_to_compress)

# initializing string 
s = "t1o11m111 1101111a11111r101111011110110110"
i = 0
buffer = bytearray()
while i < len(s):
    if (s[i].isnumeric()):
        buffer.append(int(s[i]))
        i += 1
    else:
        buffer.append(ord(s[i]))
        i += 1

# now write your buffer to a file
with open("uncompressed_file", 'bw') as f:
    f.write(buffer)


# compressed_file = open("compressed_file", "r").read()
# Decompress(compressed_file)