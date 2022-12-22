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
    step = orientationMap[orientation]
    for _ in range(steps):
      nextRow = row + step[0]
      nextCol = col + step[1]

      if nextRow >= len(board) or orientation == 1 and board[nextRow][nextCol] == ' ':
        nextRow = 0
        while board[nextRow][nextCol] == ' ':
          nextRow += 1

      elif nextRow < 0 or orientation == 3 and board[nextRow][nextCol] == ' ':
        nextRow = len(board) - 1
        while board[nextRow][nextCol] == ' ':
          nextRow -= 1

      elif nextCol >= len(board[nextRow]) or orientation == 0 and board[nextRow][nextCol] == ' ':
        nextCol = 0
        while board[nextRow][nextCol] == ' ':
          nextCol += 1

      elif nextCol < 0 or orientation == 2 and board[nextRow][nextCol] == ' ':
        nextCol = len(board[0]) - 1
        while board[nextRow][nextCol] == ' ':
          nextCol -= 1
      
      if board[nextRow][nextCol] == '#':
        break
      
      row = nextRow
      col = nextCol
  else:
    if turn == 'R':
      orientation += 1
    else:
      orientation -= 1
    orientation %= 4

print(1000 * (row + 1) + 4 * (col + 1) + orientation)