import heapq
import math

board = []
targetLetter = chr(ord('z') + 1)

startingPositions = []

with open('./12/input.txt', 'r') as data:
  for i, line in enumerate(data):
    board.append(list(line.strip()))
    index = line.find('S')
    if index >= 0:
      startRow = i
      startCol = index
      board[startRow][startCol] = chr(ord('a'))

    index = line.find('a')
    while index >= 0:
      startingPositions.append((i, index))
      index = line.find('a', index + 1)
    
    index = line.find('E')
    if index >= 0:
      board[i][index] = targetLetter

def find(board, seen, queue):
  while len(queue) > 0:
    cost, location = heapq.heappop(queue)
    row, col = location

    if board[row][col] == targetLetter:
      return cost

    if location in seen:
      continue
    seen.add(location)

    if row > 0 and ord(board[row-1][col]) - 1 <= ord(board[row][col]):
      heapq.heappush(queue, (cost + 1, (row - 1, col)))
    if col > 0 and ord(board[row][col-1]) - 1 <= ord(board[row][col]):
      heapq.heappush(queue, (cost + 1, (row, col-1)))
    if row < len(board) - 1 and ord(board[row+1][col]) - 1 <= ord(board[row][col]):
      heapq.heappush(queue, (cost + 1, (row+1, col)))
    if col < len(board[0]) - 1 and ord(board[row][col+1]) - 1 <= ord(board[row][col]):
      heapq.heappush(queue, (cost + 1, (row, col+1)))
  return math.inf

lowestCost = math.inf
for position in startingPositions:
  queue = []
  heapq.heappush(queue, (0, position))
  seen = set()
  lowestCost = min(lowestCost, find(board, seen, queue))

print(lowestCost)