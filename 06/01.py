stream = None
with open('./06/input.txt', 'r') as data:
  stream = data.readline()

for i in range (4, len(stream)):
  if len(set([*stream[i-4:i]])) == 4:
     # +1 because of indexing, -1 because the for loop is one past the range because of python slicing
    print(i)
    break
