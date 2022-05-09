import bitarray
import sys

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

symbol_list = [] #list of symbols
tree = HuffmanTree() #Epsilon, starts as root
buffer = bytearray() #Starting buffer

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

def FindSymbolInTree(input, node):
    if (input[0] == "0"):
        node.left_child.count += 1 #increase occurence
        symbol_to_return = node.left_child.symbol
        RecalculateTree(node, node.left_child)
        return symbol_to_return
        
    else:
        return "" + FindSymbolInTree(input[1:], node.right_child)

def WriteToBuffer(bit_array, buffer):

    strings = [str(integer) for integer in bit_array]
    a_string = "".join(strings)
    an_integer = int(a_string, 2)
    buffer.append(an_integer)

    #print(a_string)

def WriteStringToBitArrayThenBuffer(bit_array, j, string_to_encode):
    for i in range(len(string_to_encode)):                
                bit_array[j] = int(string_to_encode[i])
                j += 1
                if (j % 8 == 0 and j != 0):
                    WriteToBuffer(bit_array, buffer)
                    j = 0
    return j


def Compress(input):

    string_to_encode = ""
    bit_array = [0] * 8
    j = 0

    print("Compressing...")

    for element in input:        
        new_symbol = not element in symbol_list        
        if (new_symbol):

            string_to_encode = ReturnCodeOfNewSymbol(tree.root)
            j = WriteStringToBitArrayThenBuffer(bit_array, j, string_to_encode)

            character_encoding = bin(ord(element))[2:]
            if (len(character_encoding) < 8):
                character_encoding = character_encoding.zfill(8)
                #print("Code of: " + element + " is: " + character_encoding)
            
            first_part = character_encoding[0:8-j]
            second_part = character_encoding[8-j:8]

            for k in range(len(first_part)):
                bit_array[k+j] = int(first_part[k])

            WriteToBuffer(bit_array, buffer)
    
            original_j = j
            j = -1

            if (second_part):
                for k in range(len(second_part)):
                    bit_array[k] = int(second_part[k])
                j = original_j - 1

            j += 1
            
            AddNewSymbolToTree(element)

        else:
            string_to_encode = IncreaseOccurenceAndReturnCode(element, tree.root)
            j = WriteStringToBitArrayThenBuffer(bit_array, j, string_to_encode)

        if (j % 8 == 0 and j != 0):
            WriteToBuffer(bit_array, buffer)
            j = 0
    
    # Zbytek kódu, co se nemusí vlézt do 1 byte a zároveň zakódování epsilon symbolu.
    for i in range(8-j):
        bit_array[i+j] = "1"


    WriteToBuffer(bit_array, buffer)

    epsilon_code = ReturnCodeOfNewSymbol(tree.root)
    epsilon_code = epsilon_code[8-j:]

    for i in range(len(epsilon_code)):
        if (i + 1 % 8 == 0 and i != 0):
            WriteToBuffer(bit_array, buffer)

    with open("compressed_file", 'bw') as f:
        f.write(buffer)

def Decompress():
    
    print("Decompressing...")
    with open("compressed_file", "rb") as fh:
        
        b = fh.read(1)
        decoded_string = b.decode("utf-8")
        AddNewSymbolToTree(b.decode("utf-8"))
        epsilon_symbol = "1"
        working_byte = ""

        while b:

            b = fh.read(1)
            new_byte = bin(int.from_bytes(b, byteorder=sys.byteorder))[2:]
            new_byte = new_byte.zfill(8)
            #print("Byte, se kterým se pracuje: " + new_byte)

            if (new_byte != "00000000"):
                for i in range(len(new_byte)):

                    working_byte += new_byte[i]
                    if (working_byte == epsilon_symbol):

                        if (i == 7):
                            new_symbol = bin(int.from_bytes(fh.read(1), byteorder=sys.byteorder))[2:]
                        else:
                            new_symbol = new_byte[i+1:]
                            string_byte_to_fill = bin(int.from_bytes(fh.read(1), byteorder=sys.byteorder))[2:]
                            string_byte_to_fill = string_byte_to_fill.zfill(8)
                            new_symbol += string_byte_to_fill[:i+1]
                            new_byte = string_byte_to_fill

                        new_symbol = chr(int(new_symbol, 2))
                        decoded_string += new_symbol
                        AddNewSymbolToTree(new_symbol)
                        epsilon_symbol += "1"
                        working_byte = ""

                    elif (new_byte[i] == "0"):
                        decoded_string += FindSymbolInTree(working_byte, tree.root)
                        working_byte = ""

        print(decoded_string)


#Testing part of the application

#text_to_compress = open("fullBible.txt", "r").read()
text_to_compress = open("book_of_genesis.txt", "r").read()
#text_to_compress = open("book_of_genesis_without_numbers.txt", "r").read()
#text_to_compress = "tom marta at"
#text_to_compress = "taat"

Compress(text_to_compress)

symbol_list = [] #list of symbols
tree = HuffmanTree() #Epsilon, starts as root

Decompress()