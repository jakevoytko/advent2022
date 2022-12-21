from collections import defaultdict
import heapq

class Monkey:
  def __init__(self, name, operation):
    self.name = name
    self.operation = operation
    self.resetDependencies()
    self.result = None

  def resetDependencies(self):
    self.dependencies = set()
    if len(self.operation) > 1:
      self.dependencies.add(self.operation[0])
      self.dependencies.add(self.operation[2])

  def calculate(self, monkeyOperations):
    if len(self.operation) == 1:
      self.result = int(self.operation[0])
    else:
      lhs = monkeyOperations[self.operation[0]].result
      rhs = monkeyOperations[self.operation[2]].result
      op = self.operation[1]
      if op == '+':
        self.result = lhs + rhs
      elif op == '-':
        self.result = lhs - rhs
      elif op == '/':
        self.result = lhs / rhs
      elif op == '*':
        self.result = lhs * rhs
      else:
        raise ValueError('OH NO')

monkeyOperations = {}
reverseMonkeyDependencies = defaultdict(lambda: [])

with open('./21/input.txt', 'r') as data:
  for line in data:
    name = line[:4]
    operation = line[5:].strip().split(' ')
    monkey = Monkey(name, operation)
    monkeyOperations[name] = monkey
    for dependency in monkey.dependencies:
      reverseMonkeyDependencies[dependency].append(name)

def runWithHumn(monkeyOperations, reverseMonkeyDependencies, num):
  unprocessedMonkeys = set()
  for monkey in monkeyOperations.values():
    if monkey.name == 'humn':
      monkey.operation = [str(num)]
    monkey.resetDependencies()
    unprocessedMonkeys.add(monkey)
  
  while len(unprocessedMonkeys) > 0:
    for monkey in unprocessedMonkeys.copy():
      if len(monkey.dependencies) == 0:
        monkey.calculate(monkeyOperations)
        for other in reverseMonkeyDependencies[monkey.name]:
          if monkey.name in monkeyOperations[other].dependencies:
            monkeyOperations[other].dependencies.remove(monkey.name)
        unprocessedMonkeys.remove(monkey)
  
  root = monkeyOperations['root']
  lhs = monkeyOperations[root.operation[0]]
  rhs = monkeyOperations[root.operation[2]]
  return rhs.result - lhs.result

lowerBounds = -1
upperBounds = 1

# Note: example needs opposite lt/gt checks
while runWithHumn(monkeyOperations, reverseMonkeyDependencies, lowerBounds) > 0:
  lowerBounds *= 2

while runWithHumn(monkeyOperations, reverseMonkeyDependencies, upperBounds) < 0:
  upperBounds *= 2

while lowerBounds <= upperBounds:
  mean = (lowerBounds + upperBounds) // 2
  result = runWithHumn(monkeyOperations, reverseMonkeyDependencies, mean)
  if result == 0:
    print(mean)
    break
  elif result < 0:
    lowerBounds = mean + 1
  else:
    upperBounds = mean - 1
