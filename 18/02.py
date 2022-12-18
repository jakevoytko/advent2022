import math

shape = set()

minX = math.inf
maxX = -math.inf
minY = math.inf
maxY = -math.inf
minZ = math.inf
maxZ = -math.inf

with open('./18/input.txt', 'r') as data:
  for line in data:
    cube = tuple([int(x) for x in line.strip().split(',')])
    shape.add(cube)
    minX = min(minX, cube[0])
    maxX = max(maxX, cube[0])
    minY = min(minY, cube[1])
    maxY = max(maxY, cube[1])
    minZ = min(minZ, cube[2])
    maxZ = max(maxZ, cube[2])

search = [(minX - 1, minY - 1, minZ - 1)]
visited = set()

faces = 0

while len(search) > 0:
  cube = search.pop()
  if cube in visited:
    continue
  visited.add(cube)

  for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
    next = (cube[0] + dx, cube[1] + dy, cube[2] + dz)
    if next in visited:
      continue

    if next in shape:
      faces += 1
    elif next[0] >= minX-1 and next[0] <= maxX+1 and next[1] >= minY-1 and next[1] <= maxY+1 and next[2] >= minZ-1 and next[2] <= maxZ+1:
      search.append(next)

print(faces)