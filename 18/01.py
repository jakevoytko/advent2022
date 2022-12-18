shape = set()

with open('./18/input.txt', 'r') as data:
  for line in data:
    shape.add(tuple([int(x) for x in line.strip().split(',')]))

faces = 0

for cube in shape:
  for dx, dy, dz in [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]:
    if (cube[0] + dx, cube[1] + dy, cube[2] + dz) not in shape:
      faces+=1

print(faces)