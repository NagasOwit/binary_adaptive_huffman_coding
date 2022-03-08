class Node:                  
    def __init__(self, value, propability, left_child, right_child):
        self.value = value
        self.propability = propability
        self.left_child = left_child
        self.right_child = right_child

text_to_compress = open("book_of_genesis_to_compress.txt", "r").read()

symbols_with_propability = {}  
for keys in text_to_compress:
    symbols_with_propability[keys] = symbols_with_propability.get(keys, 0) + 1

print ("Count of all characters is :\n " + str(symbols_with_propability))