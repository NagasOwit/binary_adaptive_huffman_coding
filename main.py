import sys
import numpy as np

class Node:

    def __init__(self, symbol, index, left_child, right_child, count, code):
        self.symbol = symbol
        self.index = index
        self.left_child = left_child
        self.right_child = right_child
        self.count = count
        self.code = code

escape_symbol = Node("", 0, None, None, 0, "")
symbol_list = [] #list of symbols
symbol_list.append(escape_symbol)
buffer = bytearray() #Starting buffer
all_symbols = []

def UpdateTree(index):
    
    while (index != 0):

        node_to_raise = symbol_list[index]        
        filter_list = []
        highest_value = 0

        for i in range(index):

            if (symbol_list[i].count == node_to_raise.count):
                filter_list.append(symbol_list[i])

        highest_value = min(node.index for node in filter_list)

        if (highest_value):

            tmp_node = symbol_list[highest_value]
            symbol_list[highest_value].symbol = node_to_raise.symbol
            symbol_list[index].symbol = tmp_node.symbol
            symbol_list[index].count = tmp_node.count
            index = highest_value

        symbol_list[index].count += 1
        
        for j in range(index):
            if (symbol_list[j].left_child == index or symbol_list[j].right_child == index):
                index = j
                break    

def ReturnCodeOfNewSymbol():
    return symbol_list[-1].code
    

def AddNewSymbolToTree(symbol):

    epsilon_symbol = symbol_list[-1]
    end_index = epsilon_symbol.index

    new_symbol = Node("", end_index, end_index + 1, end_index + 2, 0, epsilon_symbol.code)
    left_child = Node(symbol, end_index + 1, None, None, 0, epsilon_symbol.code + "0")
    right_child = Node("", end_index + 2, None, None, 0, epsilon_symbol.code + "1")

    symbol_list[-1] = new_symbol    
    symbol_list.append(left_child)
    symbol_list.append(right_child)  

    UpdateTree(left_child.index)

def IncreaseOccurenceAndReturnCode(symbol):
    
    for x in range(len(symbol_list)):
        if (symbol_list[x].symbol == symbol):
            code = symbol_list[x].code
            UpdateTree(symbol_list[x].index)
            return code

def FindSymbolInTree(input):

    for x in symbol_list:
        if (x.code == input):
            returning_symbol = x.symbol
            return returning_symbol
    

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

        new_symbol = not element in all_symbols    

        if (new_symbol):
            
            all_symbols.append(element)
            string_to_encode = ReturnCodeOfNewSymbol()
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
            string_to_encode = IncreaseOccurenceAndReturnCode(element)
            j = WriteStringToBitArrayThenBuffer(bit_array, j, string_to_encode)

        if (j % 8 == 0 and j != 0):
            WriteToBuffer(bit_array, buffer)
            j = 0
    
    # Zbytek kódu, co se nemusí vlézt do 1 byte a zároveň zakódování epsilon symbolu.
    for i in range(8-j):
        bit_array[i+j] = "1"


    WriteToBuffer(bit_array, buffer)

    epsilon_code = ReturnCodeOfNewSymbol()
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
                        decoded_string += FindSymbolInTree(working_byte)
                        working_byte = ""

        print(decoded_string)


#Testing part of the application

#text_to_compress = open("fullBible.txt", "r").read()
#text_to_compress = open("book_of_genesis.txt", "r").read()
#text_to_compress = open("book_of_genesis_without_numbers.txt", "r").read()
text_to_compress = "barbaraabarboraubaru"
#text_to_compress = "tom marta at"
#text_to_compress = "taat"

Compress(text_to_compress)

for x in symbol_list:
    print("symbol: " + "{}".format(x.symbol) + " count: " + "{}".format(x.count))


escape_symbol = Node("", 0, None, None, 0, "")
symbol_list = [] #list of symbols
symbol_list.append(escape_symbol)
Decompress()