stream = None
with open('./06/input.txt', 'r') as data:
  stream = data.readline()

for i in range (15, len(stream)):
  if len(set([*stream[i-14:i]])) == 14:
     # +1 because of indexing, -1 because the for loop is one past the range because of python slicing
    print(i)
    break
