from collections import defaultdict
import heapq

class Monkey:
  def __init__(self, name, operation):
    self.name = name
    self.operation = operation
    self.dependencies = set()
    if len(operation) > 1:
      self.dependencies.add(operation[0])
      self.dependencies.add(operation[2])
    self.result = None

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
unprocessedMonkeys = set()
reverseMonkeyDependencies = defaultdict(lambda: [])

with open('./21/input.txt', 'r') as data:
  for line in data:
    name = line[:4]
    operation = line[5:].strip().split(' ')
    monkey = Monkey(name, operation)
    monkeyOperations[name] = monkey
    unprocessedMonkeys.add(monkey)
    for dependency in monkey.dependencies:
      reverseMonkeyDependencies[dependency].append(name)

root = None
while len(unprocessedMonkeys) > 0:
  print(len(unprocessedMonkeys))
  for monkey in unprocessedMonkeys.copy():
    if len(monkey.dependencies) == 0:
      monkey.calculate(monkeyOperations)
      for other in reverseMonkeyDependencies[monkey.name]:
        monkeyOperations[other].dependencies.remove(monkey.name)
      unprocessedMonkeys.remove(monkey)

print(monkeyOperations['root'].result)