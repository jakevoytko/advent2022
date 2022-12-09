head = [0, 0]
tail = [0, 0]
visited = {0: set([0])}

with open('09/input.txt', 'r') as data:
  for line in data:
    direction, count = line.strip().split(' ')
    for i in range(int(count)):
      if direction == 'R':
        head[1] += 1
        if head[0] == tail[0]:
          if head[1] > tail[1] + 1:
            tail[1] = head[1] - 1
        else:
          if head[1] > tail[1] + 1:
            tail[1] = head[1] - 1
            tail[0] = head[0]

      elif direction == 'L':
        head[1] -= 1
        if head[0] == tail[0]:
          if head[1] < tail[1] - 1:
            tail[1] = head[1] + 1
        else:
          if head[1] < tail[1] - 1:
            tail[1] = head[1] + 1
            tail[0] = head[0]

      elif direction == 'U':
        head[0] += 1
        if head[1] == tail[1]:
          if head[0] > tail[0] + 1:
            tail[0] = head[0] - 1
        else:
          if head[0] > tail[0] + 1:
            tail[0] = head[0] - 1
            tail[1] = head[1]

      elif direction == 'D':
        head[0] -= 1
        if head[1] == tail[1]:
          if head[0] < tail[0] - 1:
            tail[0] = head[0] + 1
        else:
          if head[0] < tail[0] - 1:
            tail[0] = head[0] + 1
            tail[1] = head[1]

      if tail[0] not in visited:
        visited[tail[0]] = set()
      visited[tail[0]].add(tail[1])

print(sum([len(row) for row in visited.values()]))
