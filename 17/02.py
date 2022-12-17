wind = []
with open('17/input.txt', 'r') as data:
  wind = data.readline().strip()

board = []

shapes = [
  [(0, 0), (0, 1), (0, 2), (0, 3)],
  [(0, 1), (1, 1), (2, 1), (1, 0), (1, 2)],
  [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
  [(0, 0), (1, 0), (2, 0), (3, 0)],
  [(0, 0), (0, 1), (1, 0), (1, 1)],
]

highestIndexSoFar = -1

def canBlow(board, shape, left):
  if left:
    for row, col in shape:
      if col == 0 or board[row][col - 1] == '#':
        return False
  else:
    for row, col in shape:
      if col == len(board[row]) - 1 or board[row][col + 1] == '#':
        return False
  
  return True

def canFall(board, shape):
  for row, col in shape:
    if row == 0 or board[row - 1][col] == '#':
      return False
  
  return True

windIter = 0

def periodic(allHighestIndicesSoFar, period):
  # gotta hand it to eric, the period being a non-one multiple of the LCM is clever
  mostRecent = allHighestIndicesSoFar[-period:]
  for i in range(len(allHighestIndicesSoFar) // period):
    secondMostRecent = allHighestIndicesSoFar[-(2+i)*period:-(1+i)*period]
    delta = mostRecent[0] - secondMostRecent[0]
    secondMostRecent = [x + delta for x in secondMostRecent]
    if mostRecent == secondMostRecent:
      return i + 1
  return False


i = 0
period = len(shapes) * len(wind)
allHighestIndicesSoFar = []
maxDrop = 0

while True:
  if i > period * 10 and 1000000000000 % period == i % period:
    periodMultiplier = periodic(allHighestIndicesSoFar, period)
    if periodMultiplier:
      if (1000000000000 % (periodMultiplier * period)) == (i % (periodMultiplier * period)):
        break
  shapePattern = shapes[i % len(shapes)]
  shape = [(row + highestIndexSoFar + 4, col + 2) for row, col in shapePattern]
  highestRow = max([row for row, _ in shape])
  for _ in range(len(board), highestRow + 1):
    board.append(['.' for _ in range(7)])

  while True:
    # Blow
    if wind[windIter % len(wind)] == '<':
      if canBlow(board, shape, True):
        shape = [(row, col - 1) for row, col in shape]
    else:
      if canBlow(board, shape, False):
        shape = [(row, col + 1) for row, col in shape]
    windIter += 1

    # Fall
    if not canFall(board, shape):
      for row, col in shape:
        board[row][col] = '#'
      highestIndexSoFar = max(highestIndexSoFar, max([row for row, _ in shape]))
      allHighestIndicesSoFar.append(highestIndexSoFar)
      break
    shape = [(row - 1, col) for row, col in shape]
  i += 1

periodMultiplier = periodic(allHighestIndicesSoFar, period)
delta = allHighestIndicesSoFar[-1] - allHighestIndicesSoFar[-1 - periodMultiplier * period]
remainingRounds = 1000000000000 - i
print(highestIndexSoFar + delta * remainingRounds // (period * periodMultiplier) + 1)
