rope = [[0, 0] for _ in range(10)]
visited = {0: set([0])}

with open('09/input.txt', 'r') as data:
  for line in data:
    direction, count = line.strip().split(' ')

    for i in range(int(count)):
      if direction == 'R':
        rope[0][1] += 1
      elif direction == 'L':
        rope[0][1] -= 1
      elif direction == 'U':
        rope[0][0] += 1
      elif direction == 'D':
        rope[0][0] -= 1

      for i in range(len(rope) - 1):
        current = rope[i]
        next = rope[i + 1]

        rowAdjustment = 0
        colAdjustment = 0
        if abs(current[0] - next[0]) > 1 or abs(current[1] - next[1]) > 1:
          if current[0] == next[0]:
            colAdjustment = current[1] - next[1]
          elif current[1] == next[1]:
            rowAdjustment = current[0] - next[0]
          else:
            colAdjustment = current[1] - next[1]
            rowAdjustment = current[0] - next[0]
        
        next[0] += max(-1, min(1, rowAdjustment))
        next[1] += max(-1, min(1, colAdjustment))

      if rope[-1][0] not in visited:
        visited[rope[-1][0]] = set()
      visited[rope[-1][0]].add(rope[-1][1])

print(sum([len(row) for row in visited.values()]))
