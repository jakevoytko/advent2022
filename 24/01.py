from queue import PriorityQueue
from collections import defaultdict
import math

blizzards = defaultdict(lambda: defaultdict(lambda: set()))

rows = 0
cols = 0

with open('./24/input.txt', 'r') as data:
  for row, line in enumerate(data):
    line = line.strip()
    cols = len(line)
    rows = row + 1
    for col, letter in enumerate(line):
      if letter == '#' or letter == '.':
        continue
      blizzards[row][col].add(letter)

blizzardsByMinute = {
  0: blizzards,
}

def simulate(blizzards):
  nextBlizzards = defaultdict(lambda: defaultdict(lambda: set()))

  for row, line in blizzards.items():
    for col, colBlizzards in line.items():
      for blizzard in colBlizzards:
        if blizzard == '>':
          if col == cols - 2:
            nextBlizzards[row][1].add(blizzard)
          else:
            nextBlizzards[row][col + 1].add(blizzard)
        elif blizzard == '<':
          if col == 1:
            nextBlizzards[row][cols - 2].add(blizzard)
          else:
            nextBlizzards[row][col - 1].add(blizzard)
        elif blizzard == 'v':
          if row == rows - 2:
            nextBlizzards[1][col].add(blizzard)
          else:
            nextBlizzards[row + 1][col].add(blizzard)
        elif blizzard == '^':
          if row == 1:
            nextBlizzards[rows - 2][col].add(blizzard)
          else:
            nextBlizzards[row - 1][col].add(blizzard)
        else:
          raise RuntimeError('Where did you get that blizzard')

  return nextBlizzards

def makeQueueEntry(coordinate, minute, rows, cols):
  goalRow = rows - 1
  goalCol = cols - 2

  distance = (goalRow - coordinate[0]) + (goalCol - coordinate[1])
  return (distance, minute, coordinate)

queue = PriorityQueue()
queue.put(makeQueueEntry((0, 1), 0, rows, cols))

def inBounds(row, col, rows, cols):
  if col <= 0 or col >= cols - 1 or row < 0 or row >= rows:
    return False
  elif row == 0:
    return col == 1
  elif row == rows - 1:
    return col == cols - 2
  return True

minMinute = math.inf
timeCoordinateCache = defaultdict(lambda: set())

while not queue.empty():
  distance, minute, (row, col) = queue.get()
  if (row, col) in timeCoordinateCache[minute]:
    continue
  timeCoordinateCache[minute].add((row, col))
  if minute >= minMinute:
    continue

  if row == rows - 1 and col == cols - 2:
    minMinute = min(minMinute, minute)
    continue
  else:
    if distance + minute >= minMinute:
      continue

  if (minute + 1) not in blizzardsByMinute:
    blizzardsByMinute[len(blizzardsByMinute)] = simulate(blizzardsByMinute[len(blizzardsByMinute) - 1])
  
  nextBlizzard = blizzardsByMinute[minute + 1]

  # Up
  if col not in nextBlizzard[row - 1] and inBounds(row - 1, col, rows, cols):
    queue.put(makeQueueEntry((row - 1, col), minute + 1, rows, cols))
  # Down
  if col not in nextBlizzard[row + 1] and inBounds(row + 1, col, rows, cols):
    queue.put(makeQueueEntry((row + 1, col), minute + 1, rows, cols))
  # Left
  if col - 1 not in nextBlizzard[row] and inBounds(row, col - 1, rows, cols):
    queue.put(makeQueueEntry((row, col - 1), minute + 1, rows, cols))
  # Right
  if col + 1 not in nextBlizzard[row] and inBounds(row, col + 1, rows, cols):
    queue.put(makeQueueEntry((row, col + 1), minute + 1, rows, cols))
  # Stay
  if col not in nextBlizzard[row]:
    queue.put(makeQueueEntry((row, col), minute + 1, rows, cols))

print(minMinute)