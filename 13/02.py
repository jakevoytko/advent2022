import functools

def compare(left, right):
  iter = 0

  while iter < len(left) and iter < len(right):
    leftval = left[iter]
    rightval = right[iter]
    if isinstance(leftval, int):
      if isinstance(rightval, int):
        if rightval != leftval:
          #return leftval < rightval
          return leftval - rightval
      else:
        result = compare([leftval], rightval)
        if result != 0:
          return result
    else:
      if isinstance(rightval, int):
        result = compare(leftval, [rightval])
        if result != 0:
          return result
      else:
        result = compare(leftval, rightval)
        if result != 0:
          return result
    iter+=1

  if iter == len(left) and iter != len(right):
    # return True 
    return -1
  elif iter != len(left) and iter == len(right):
    # return False
    return 1
  return 0

packets = [[[2]],[[6]]]
with open('./13/input.txt', 'r') as data:
  while True:
    packets.append(eval(data.readline().strip()))
    packets.append(eval(data.readline().strip()))

    if data.readline() == '':
      break
answer = 1
for i, packet in enumerate(sorted(packets, key = functools.cmp_to_key(compare))):
  if "{}".format(packet) in ["[[2]]","[[6]]"]:
    answer *= (i+1)
print(answer)