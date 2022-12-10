register = 1
addPipeline = None

cyclicAnswers = []
cycle = 0

display = [
  list('........................................'),
  list('........................................'),
  list('........................................'),
  list('........................................'),
  list('........................................'),
  list('........................................'),
]
crtIterator = -1

def bookkeeping():
  global display
  crtCol = crtIterator % 40
  crtRow = crtIterator // 40
  if abs(register - crtCol) <= 1:
    display[crtRow][crtCol] = '#'

def noop():
  bookkeeping()

def tick():
  global cycle
  global crtIterator
  cycle += 1
  crtIterator += 1

def addx(value):
  global register
  bookkeeping()
  tick()
  bookkeeping()
  register += value

with open('./10/input.txt', 'r') as data:
  for line in data:
    tick()
    instructions = line.strip().split(' ')
    if instructions[0] == 'noop':
      noop()
    else:
      addx(int(instructions[1]))

for line in display:
  print(''.join(line))