def compare(left, right):
  print("comparing", left, right)
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

sum = 0

index = 1
with open('./13/input.txt', 'r') as data:
  while True:
    left = eval(data.readline().strip())
    right = eval(data.readline().strip())
    if compare(left, right) < 0:
      sum += index
    index += 1

    if data.readline() == '':
      break

print(sum)