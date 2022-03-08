f = open("book_of_genesis_to_compress.txt", "r").read()

res = {}
  
for keys in f:
    res[keys] = res.get(keys, 0) + 1

print ("Count of all characters is :\n " + str(res))