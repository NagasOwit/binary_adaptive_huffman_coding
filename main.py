class Node:                  
    def __init__(self, value, propability, left_child, right_child):
        self.value = value
        self.propability = propability
        self.left_child = left_child
        self.right_child = right_child

def AddToTree():
    return 0

#text_to_compress = open("book_of_genesis_to_compress.txt", "r").read()
text_to_compress = "AAABBCCCCCC"

symbols_with_propability = {}  
for keys in text_to_compress:
    symbols_with_propability[keys] = symbols_with_propability.get(keys, 0) + 1

sorted_symbols_with_propability = sorted(symbols_with_propability.items(), key=lambda sort: sort[1])
print(str(sorted_symbols_with_propability[0][0]) + " " + str(sorted_symbols_with_propability[0][1]))