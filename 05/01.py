stacks = {a:[] for a in range(0, 10)}

with open('./05/input.txt', 'r') as data:
  while True:
    line = data.readline()

    if line[1].isdigit():
      break

    for stackIndex, stringIndex in enumerate(range(1, len(line), 4)):
      if line[stringIndex].isalpha():
        stacks[stackIndex].append(line[stringIndex])
    
  data.readline()

  for _, v in stacks.items():
    v.reverse()

  for line in data:
    _, howMany, _, origin, _, destination = line.strip().split(' ')
    for i in range(int(howMany)):
      stacks[int(destination) - 1].append(stacks[int(origin) - 1].pop())

answer = [stacks[i][-1] for i in range(len(stacks)) if len(stacks[i]) > 0]
print(''.join(answer))
