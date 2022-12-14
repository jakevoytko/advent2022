import math

paths = []
minCol = math.inf
maxCol = -math.inf
maxRow = -math.inf

with open('./14/input.txt', 'r') as data:
  for line in data:
    newPath = []
    for coordinate in line.strip().split(' -> '):
      col, row = [int(v) for v in coordinate.split(',')]
      minCol = min(minCol, col)
      maxCol = max(maxCol, col)
      maxRow = max(maxRow, row)
      newPath.append((col, row))
    paths.append(newPath)

paths.append([(minCol - maxRow, maxRow + 2), (maxCol + maxRow, maxRow + 2)])
maxRow = maxRow + 2
minCol = minCol - maxRow
maxCol = maxCol + maxRow

# Transform the coordinates to make it easier to make a dense grid
paths = [[(col - minCol + 1, row) for col, row in path] for path in paths]
grid = [['.' for _ in range(maxCol - minCol + 3)] for _ in range(maxRow + 1)]

for path in paths:
  lastCoordinate = None
  for coordinate in path:
    col, row = coordinate
    if lastCoordinate is None:
      lastCoordinate = coordinate
      grid[row][col] = '#'
    else:
      if lastCoordinate[0] == coordinate[0]:
        for i in range(coordinate[1], lastCoordinate[1], [1, -1][coordinate[1] > lastCoordinate[1]]):
          grid[i][col] = '#'
        lastCoordinate = coordinate
      else:
        for i in range(coordinate[0], lastCoordinate[0], [1, -1][coordinate[0] > lastCoordinate[0]]):
          grid[row][i] = '#'
        lastCoordinate = coordinate

origin = 500 - minCol + 1
grid[0][origin] = '+'
# for line in grid:
#   print(''.join(line))
# print('')

count = 0

# Drop each grain
while True:
  # Simulate each grain
  grain = (0, origin)
  while True:
    if grain[0] == len(grid) - 1: # The sand fell off the edge
      raise RuntimeError('should not have hit bottom')
    elif grid[grain[0] + 1][grain[1]] == '.':
      grain = (grain[0] + 1, grain[1])
    elif grid[grain[0] + 1][grain[1] - 1] == '.':
      grain = (grain[0] + 1, grain[1] - 1)
    elif grid[grain[0] + 1][grain[1] + 1] == '.':
      grain = (grain[0] + 1, grain[1] + 1)
    else:
      if grid[0][origin] == 'o': # Sand can no longer flow
        break
      grid[grain[0]][grain[1]] = 'o'
      count += 1
      break
  if grid[0][origin] == 'o':
    break
  
print(count)