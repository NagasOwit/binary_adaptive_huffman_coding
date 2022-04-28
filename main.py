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

def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]

def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])

# s = 'Hello, World!'
# b = string2bits(s)
# s2 = bits2string(b)

# print ('String:')
# print (s)

# print ('\nList of Bits:')
# for x in b:
#     print (x)

# print ('\nString:')
# print (s2)

def TestEncoding():

    s = "t1o11m111 1101111a11111r101111011110110110"
    buffer = bytearray()
    bit_array = [0] * 8
    j = 0

    for i in range(len(s)):
        
        if (s[i].isnumeric()):
            bit_array[j] = int(s[i])

        else:
            character_encoding = bin(ord(s[i]))[2:]
            first_part = character_encoding[0:7-j]
            second_part = character_encoding[7-j:7]

            for k in range(len(first_part)):
                bit_array[k+j] = int(first_part[k])


            strings = [str(integer) for integer in bit_array]
            a_string = "".join(strings)
            an_integer = int(a_string, 2)
            buffer.append(an_integer)
            
            print(an_integer)

            if (second_part):
                for k in range(len(second_part)):
                    bit_array[k] = int(second_part[k])

        j += 1
        if ((i + 1) % 8 == 0):
            strings = [str(integer) for integer in bit_array]
            a_string = "".join(strings)
            an_integer = int(a_string, 2)

            print(an_integer)

            buffer.append(an_integer)
            j = 0
        i += 1

    # now write your buffer to a file
    with open("uncompressed_file", 'bw') as f:
        f.write(buffer)

def TestDecoding():

    print("Decoding")

    with open("uncompressed_file", "rb") as fh:
        b = fh.read(1)
        print(b)
        while b:
            b = fh.read(1)
            print(bin(int.from_bytes(b, byteorder=sys.byteorder))[2:])
            #...do something with b

def Test():

    unicode_value = ord('t')

    print("The Unicode value of the character", "t", "is", str(unicode_value))
    print(bin(unicode_value))

TestEncoding()
TestDecoding()
Test()

# compressed_file = open("compressed_file", "r").read()
# Decompress(compressed_file)