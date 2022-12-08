grid = []
cache = []

with open('./08/input.txt', 'r') as data:
  for line in data:
    grid.append([int(x) for x in line.strip()])
    cache.append([1 for x in line.strip()])

for row in range(len(grid)):
  stack = []
  for col in range(len(grid[row])):
    while len(stack) > 0 and grid[row][col] > grid[row][stack[-1]]:
      stack.pop()
    if len(stack) == 0:
      cache[row][col] *= col
    else:
      cache[row][col] *= col - stack[-1]
    stack.append(col)

for row in range(len(grid)):
  stack = []
  for col in range(len(grid[row]) - 1, -1, -1):
    while len(stack) > 0 and grid[row][col] > grid[row][stack[-1]]:
      stack.pop()
    if len(stack) == 0:
      cache[row][col] *= (len(grid[row]) - 1) - col
    else:
      cache[row][col] *= stack[-1] - col
    stack.append(col)

for col in range(len(grid[0])):
  stack = []
  for row in range(len(grid)):
    while len(stack) > 0 and grid[row][col] > grid[stack[-1]][col]:
      stack.pop()
    if len(stack) == 0:
      cache[row][col] *= row
    else:
      cache[row][col] *= row - stack[-1]
    stack.append(row)

for col in range(len(grid[0])):
  stack = []
  for row in range(len(grid)-1, -1, -1):
    while len(stack) > 0 and grid[row][col] > grid[stack[-1]][col]:
      stack.pop()
    if len(stack) == 0:
      cache[row][col] *= (len(grid) - 1) - row
    else:
      cache[row][col] *= stack[-1] - row
    stack.append(row)

answer = -1
for row in cache:
  for val in row:
    answer = max(val, answer)

print(answer)