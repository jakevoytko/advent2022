import re
import math

board = []
instructions = None

with open('./22/input.txt', 'r') as data:
  for line in data:
    if len(line.strip()) == 0:
      break
    board.append(line[:-1])
  instructions = [(a, b) for _, a, b in re.findall(r'((\d+)|([RL]))', data.readline().strip())]

# Fill out the map to make wrapping easier
longest = max([len(row) for row in board])
for i in range(len(board)):
  board[i] = board[i] + ' ' * (longest - len(board[i]))

orientationMap = {
  0: (0, 1),
  1: (1, 0),
  2: (0, -1),
  3: (-1, 0),
}

orientation = 0
col = board[0].index('.')
row = 0

for steps, turn in instructions:
  if len(steps) > 0:
    steps = int(steps)
    for _ in range(steps):
      step = orientationMap[orientation]
      nextRow = row + step[0]
      nextCol = col + step[1]
      nextOrientation = orientation

      # If you're not cheating, you're not trying
      if nextRow >= len(board) or orientation == 1 and board[nextRow][nextCol] == ' ':
        if nextRow == 50:
          dRow = nextCol - 100
          nextRow = 50 + dRow
          nextCol = 99
          nextOrientation = 2
        elif nextRow == 150:
          dRow = nextCol - 50
          nextRow = 150 + dRow
          nextCol = 49
          nextOrientation = 2
        elif nextRow == 200:
          nextRow = 0
          nextCol += 100
        else:
          raise RuntimeError('o no')

      elif nextRow < 0 or orientation == 3 and board[nextRow][nextCol] == ' ':
        if nextCol <= 49:
          dRow = nextCol
          nextRow = 50 + dRow
          nextCol = 50
          nextOrientation = 0
        elif nextCol <= 99:
          dRow = nextCol - 50
          nextRow = 150 + dRow
          nextCol = 0
          nextOrientation = 0
        elif nextCol <= 149:
          nextRow = 199
          nextCol -= 100
        else:
          raise RuntimeError('o no')

      elif nextCol >= len(board[nextRow]) or orientation == 0 and board[nextRow][nextCol] == ' ':
        if nextRow <= 49:
          dRow = 49 - nextRow
          nextRow = 100 + dRow
          nextCol = 99
          nextOrientation = 2
        elif nextRow <= 99:
          dCol = nextRow - 50
          nextCol = 100 + dCol
          nextRow = 49
          nextOrientation = 3
        elif nextRow <= 149:
          dRow = 149 - nextRow
          nextRow = dRow
          nextCol = 149
          nextOrientation = 2
        elif nextRow <= 199:
          dCol = nextRow - 150
          nextCol = 50 + dCol
          nextRow = 149
          nextOrientation = 3

        else:
          raise RuntimeError('o no')

      elif nextCol < 0 or orientation == 2 and board[nextRow][nextCol] == ' ':
        if nextRow <= 49:
          dRow = 49 - nextRow
          nextRow = 100 + dRow
          nextCol = 0
          nextOrientation = 0
        elif nextRow <= 99:
          dCol = nextRow - 50
          nextCol = dCol
          nextRow = 100
          nextOrientation = 1
        elif nextRow <= 149:
          dRow = 149 - nextRow
          nextRow = dRow
          nextCol = 50
          nextOrientation = 0
        elif nextRow <= 199:
          dCol = nextRow - 150
          nextCol = 50 + dCol
          nextRow = 0
          nextOrientation = 1
        else:
          raise RuntimeError('o no')

      if board[nextRow][nextCol] == '#':
        break
      elif board[nextRow][nextCol] == ' ':
        raise RuntimeError('Ended on a space, check your math')

      row = nextRow
      col = nextCol
      orientation = nextOrientation
  else:
    if turn == 'R':
      orientation += 1
    else:
      orientation -= 1
    orientation %= 4

print(1000 * (row + 1) + 4 * (col + 1) + orientation)