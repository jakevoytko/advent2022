grid = []
cache = []

with open('./08/input.txt', 'r') as data:
  for line in data:
    grid.append([int(x) for x in line.strip()])
    cache.append([False for x in line.strip()])

for row in range(len(grid)):
  largest = -1
  for col in range(len(grid[row])):
    if grid[row][col] > largest:
      cache[row][col] = True
    largest = max(largest, grid[row][col])

for row in range(len(grid)):
  largest = -1
  for col in range(len(grid[row]) - 1, -1, -1):
    if grid[row][col] > largest:
      cache[row][col] = True
    largest = max(largest, grid[row][col])

for col in range(len(grid[0])):
  largest = -1
  for row in range(len(grid)):
    if grid[row][col] > largest:
      cache[row][col] = True
    largest = max(largest, grid[row][col])

for col in range(len(grid[0])):
  largest = -1
  for row in range(len(grid)-1, -1, -1):
    if grid[row][col] > largest:
      cache[row][col] = True
    largest = max(largest, grid[row][col])

answer = 0
for row in cache:
  for visible in row:
    if visible:
      answer+=1

print(answer)