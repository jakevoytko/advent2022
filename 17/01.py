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

def printBoard(board):
  for line in reversed(board):
    print(''.join(line))

def printBoardWithShape(board, shape):
  for row, col in shape:
    board[row][col] = '@'
  for line in reversed(board):
    print(''.join(line))
  for row, col in shape:
    board[row][col] = '.'

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

for i in range(2022):
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

      break
    shape = [(row - 1, col) for row, col in shape]

print(highestIndexSoFar + 1)