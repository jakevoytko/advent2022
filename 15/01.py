import re

def distance(row0, col0, row1, col1):
  return abs(row0 - row1) + abs(col0 - col1)


class Range:
  def __init__(self, start, end):
    self.start = start
    self.end = end

  def __repr__(self):
    return "[Range: start={} end={}]".format(self.start, self.end)

  def intersects(self, other):
    return self.start <= other.start and self.end >= other.start or\
           self.start <= other.end and self.end >= other.end or\
           other.start <= self.start and other.end >= self.start or\
           other.start <= self.end and other.end >= self.end

  def merge(self, other):
    if not self.intersects(other):
      raise RuntimeError('Should intersect')
    return Range(min(self.start, other.start), max(self.end, other.end))

  def subtract(self, other):
    if not self.intersects(other):
      return [self]

    if self.start >= other.start:
      if self.end <= other.end: # Subtract the whole thing
        return []

      # Subtract prefix
      return [Range(other.end + 1, self.end)]

    else:
      if other.end < self.end: # Subtract from the middle of the range
        return [Range(self.start, other.start - 1), Range(other.end + 1, self.end)]

      # Subtract suffix
      return [Range(self.start, other.start - 1)]

  def length(self):
    return self.end - self.start + 1


ranges = []
beacons = []
#targetRow = 10
targetRow = 2000000

with open('./15/input.txt', 'r') as data:
  for line in data:
    match = re.search(r'Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)', line.strip())
    sensorCol, sensorRow, beaconCol, beaconRow = int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
    sensorDistance = distance(sensorRow, sensorCol, beaconRow, beaconCol)
    # Calculate distance to the target row.
    distanceToTargetRow = abs(targetRow - sensorRow)
    # See if the no-beacon distance can reach the target row.
    if distanceToTargetRow > sensorDistance:
      continue

    # It can. Calculate the affected range.
    noGoDistanceRemaining = sensorDistance - distanceToTargetRow
    ranges.append(Range(sensorCol - noGoDistanceRemaining, sensorCol + noGoDistanceRemaining))
    beacons.append((beaconRow, beaconCol))

finalRanges = []

while len(ranges) > 0:
  nextRange = ranges.pop()
  i = len(ranges) - 1
  while i >= 0:
    if nextRange.intersects(ranges[i]):
      nextRange = nextRange.merge(ranges[i])
      del ranges[i]
      i = len(ranges) - 1
    else:
      i-=1
  finalRanges.append(nextRange)

for beacon in beacons:
  if beacon[0] != targetRow:
    continue
  newFinalRanges = []
  for finalRange in finalRanges:
    newFinalRanges.extend(finalRange.subtract(Range(beacon[1], beacon[1])))
  finalRanges = newFinalRanges

print(sum(x.length() for x in finalRanges))