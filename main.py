f = open("book_of_genesis_to_compress.txt", "r").read()

all_freq = {}  
for i in f:
    if i in all_freq:
        all_freq[i] += 1
    else:
        all_freq[i] = 1

print ("Count of all characters in GeeksforGeeks is :\n " + str(all_freq))