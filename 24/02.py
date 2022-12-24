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

goals = [(rows - 1, cols - 2), (0, 1), (rows - 1, cols - 2)]

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

def manhattanDistance(row0, col0, row1, col1):
  return abs((row0 - row1)) + abs((col0 - col1))

def makeQueueEntry(coordinate, goals, goal, minute):
  distance = 0
  measurementPoint = coordinate
  for i in range(goal, len(goals)):
    nextGoal = goals[i]
    distance += manhattanDistance(nextGoal[0], nextGoal[1], measurementPoint[0], measurementPoint[1])
    measurementPoint = nextGoal

  return (distance, -goal, minute, coordinate)

queue = PriorityQueue()
queue.put(makeQueueEntry((0, 1), goals, 0, 0))

def inBounds(row, col, rows, cols):
  if col <= 0 or col >= cols - 1 or row < 0 or row >= rows:
    return False
  elif row == 0:
    return col == 1
  elif row == rows - 1:
    return col == cols - 2
  return True

minMinute = math.inf
timeGoalCoordinateCache = defaultdict(lambda: defaultdict(lambda: set()))

while not queue.empty():
  distance, goal, minute, (row, col) = queue.get()
  goal = -goal
  if (row, col) in timeGoalCoordinateCache[minute][goal]:
    continue
  timeGoalCoordinateCache[minute][goal].add((row, col))
  if minute >= minMinute:
    continue

  if row == goals[goal][0] and col == goals[goal][1]:
    goal += 1
    if goal == len(goals):
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
    queue.put(makeQueueEntry((row - 1, col), goals, goal, minute + 1))
  # Down
  if col not in nextBlizzard[row + 1] and inBounds(row + 1, col, rows, cols):
    queue.put(makeQueueEntry((row + 1, col), goals, goal, minute + 1))
  # Left
  if col - 1 not in nextBlizzard[row] and inBounds(row, col - 1, rows, cols):
    queue.put(makeQueueEntry((row, col - 1), goals, goal, minute + 1))
  # Right
  if col + 1 not in nextBlizzard[row] and inBounds(row, col + 1, rows, cols):
    queue.put(makeQueueEntry((row, col + 1), goals, goal, minute + 1))
  # Stay
  if col not in nextBlizzard[row]:
    queue.put(makeQueueEntry((row, col), goals, goal, minute + 1))

print(minMinute)