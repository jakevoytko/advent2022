from collections import defaultdict
import math

board = defaultdict(lambda: {})

with open('./23/input.txt', 'r') as data:
  for row, line in enumerate(data):
    for col, letter in enumerate(line):
      if letter == '#':
        board[row][col] = True

movements = [
  ([(-1, -1), (-1, 0), (-1, 1)], (-1, 0)), # North
  ([(1, -1), (1, 0), (1, 1)], (1, 0)), # South
  ([(-1, -1), (0, -1), (1, -1)], (0, -1)), # West
  ([(-1, 1), (0, 1), (1, 1)], (0, 1)), # East
]

def printBoard(board):
  minRow = math.inf
  maxRow = -math.inf
  minCol = math.inf
  maxCol = -math.inf

  for row in board.keys():
    minRow = int(min(minRow, row))
    maxRow = int(max(maxRow, row))
    for col in board[row].keys():
      minCol = int(min(minCol, col))
      maxCol = int(max(maxCol, col))

  for row in range(minRow, maxRow + 1):
    cols = ['.'] * (maxCol - minCol + 1)
    if row in board:
      for c in board[row]:
        cols[c - minCol] = '#'
    print(''.join(cols))

round = 0
while True:
  round += 1
  proposedMoves = defaultdict(lambda: defaultdict(lambda: set()))
  newBoard = defaultdict(lambda: {})
  boardCopy = board.copy()
  # Iterate through the elves.
  for row in boardCopy.keys():
    for col in board[row].keys():
      proposal = None
      # Try to propose moves in each direction.
      for m in range(len(movements)):
        movement = movements[((round - 1) + m) % len(movements)]
        conflict = False
        for check in movement[0]:
          if col + check[1] in board[row + check[0]]:
            conflict = True
            break
        if not conflict:
          proposal = (row + movement[1][0], col + movement[1][1])
          break
      # If a proposal was not found, propose staying where you are.
      if not proposal:
        proposal = (row, col)
      else:
        # If there was a proposal, see if it was because the elf was alone.
        count = 0
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if (col + dc) in board[row + dr]:
              count += 1
        if count == 1:
          proposal = (row, col)
            
      # Map from the new location to the origin, in case the elf needs to stay put.
      proposedMoves[proposal[0]][proposal[1]].add((row, col))
  
  for proposedRow in proposedMoves.keys():
    for proposedCol in proposedMoves[proposedRow].keys():
      candidates = proposedMoves[proposedRow][proposedCol]
      if len(candidates) == 1:
        newBoard[proposedRow][proposedCol] = True
      else:
        for candidate in candidates:
          newBoard[candidate[0]][candidate[1]] = True

  equal = True
  for row in newBoard.keys():
    if not equal:
      break
    for col in newBoard[row].keys():
      if row not in board or col not in board[row]:
        equal = False
        break

  if equal:
    break

  board = newBoard

print(round)