import re
import math

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


class Coordinate:
  def __init__(self, row, col):
    self.row = row
    self.col = col


class SensorCoverage:
  def __init__(self, coordinate, distance):
    self.coordinate = coordinate
    self.distance = distance
    topCoordinate = Coordinate(coordinate.row - distance, coordinate.col)
    bottomCoordinate = Coordinate(coordinate.row + distance, coordinate.col)
    leftCoordinate = Coordinate(coordinate.row, coordinate.col - distance)
    rightCoordinate = Coordinate(coordinate.row, coordinate.col + distance)

    self.segments = [
      LineSegment(topCoordinate, leftCoordinate),
      LineSegment(topCoordinate, rightCoordinate),
      LineSegment(bottomCoordinate, leftCoordinate),
      LineSegment(bottomCoordinate, rightCoordinate),
    ]

  def budgetIntersections(self, other):
    budgetRows = []
    for segment in self.segments:
      for otherSegment in other.segments:
        intersection = segment.budgetIntersection(otherSegment)
        if intersection is not None:
          if abs(intersection - round(intersection)) < .05: # The results should either be at x.5 or x.0. Account for floating-point math
            intersection = round(intersection)
            budgetRows.extend([intersection - 1, intersection, intersection + 1])
          else:
            budgetRows.extend([math.floor(intersection), math.ceil(intersection)])

    return budgetRows

class LineSegment:
  def __init__(self, c0, c1):
    self.c0 = c0
    self.c1 = c1

  # See if the lines defined by this segment intersect. Easier to calculate and I'm feeling lazy.
  # Also only returns the row because that's all I want.
  def budgetIntersection(self, other):
    y1 = self.c0.row
    y2 = self.c1.row
    y3 = other.c0.row
    y4 = other.c1.row
    x1 = self.c0.col
    x2 = self.c1.col
    x3 = other.c0.col
    x4 = other.c1.col

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
      return None

    row = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    return row / denominator

sensorCoverages = []
#boundingMax = 20
boundingMax = 4000000

with open('./15/input.txt', 'r') as data:
  for line in data:
    match = re.search(r'Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)', line.strip())
    sensorCol, sensorRow, beaconCol, beaconRow = int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
    sensorDistance = distance(sensorRow, sensorCol, beaconRow, beaconCol)
    sensorCoverages.append(SensorCoverage(Coordinate(sensorRow, sensorCol), sensorDistance))

candidateRows = set()
for i in range(len(sensorCoverages)):
  for j in range(i + 1, len(sensorCoverages)):
    for row in sensorCoverages[i].budgetIntersections(sensorCoverages[j]):
      candidateRows.add(row)

for row in candidateRows:
  if row < 0 or row > boundingMax:
    continue

  coverages = [Range(0, boundingMax)]

  for sensor in sensorCoverages:
    distanceToTargetRow = abs(row - sensor.coordinate.row)

    # See if the no-beacon distance can reach the target row.
    if distanceToTargetRow > sensor.distance:
      continue

    # It can. Calculate the affected range.
    noGoDistanceRemaining = sensor.distance - distanceToTargetRow
    removalRange = Range(sensor.coordinate.col - noGoDistanceRemaining, sensor.coordinate.col + noGoDistanceRemaining)

    newCoverages = []

    for coverage in coverages:
      result = coverage.subtract(removalRange)
      if result is not None:
        newCoverages.extend(result)

    coverages = newCoverages

  if len(coverages) > 0:
    print(4000000 * coverages[0].start + row)
