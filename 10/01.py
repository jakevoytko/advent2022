register = 1
addPipeline = None

cyclicAnswers = []
cycle = 0

def bookkeeping():
  if (cycle - 20) % 40 == 0:
    cyclicAnswers.append(cycle * register)

def noop():
  bookkeeping()

def addx(value):
  global cycle
  global register
  bookkeeping()
  cycle += 1
  bookkeeping()
  register += value

with open('./10/input.txt', 'r') as data:
  for line in data:
    cycle += 1
    instructions = line.strip().split(' ')
    if instructions[0] == 'noop':
      noop()
    else:
      addx(int(instructions[1]))

print(sum(cyclicAnswers))