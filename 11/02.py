import re
import math

class Monkey:
  def __init__(self, id, items, operation, test, trueMonkey, falseMonkey):
    self.id = id
    self.items = items
    self.operation = operation
    self.test = test
    self.trueMonkey = trueMonkey
    self.falseMonkey = falseMonkey
    self.inspectionCount = 0
 
  def __repr__(self) -> str:
    return '[monkey {}: {}\n'.format(self.id, self.items)

  def examine(self):
    if len(self.items) == 0:
      return None
    self.inspectionCount += 1

    item = self.items[0]
    self.items = self.items[1:]

    lhs = int([self.operation[0], item][self.operation[0] == 'old'])
    rhs = int([self.operation[2], item][self.operation[2] == 'old'])
    if self.operation[1] == '+':
      item = lhs + rhs
    else:
      item = lhs * rhs
    
    if item % self.test == 0:
      return [item, self.trueMonkey]
    else:
      return [item, self.falseMonkey]

monkeys = []

with open('./11/input.txt', 'r') as data:
  while True:
    monkeyHeader = data.readline()
    if len(monkeyHeader.strip()) == 0:
      break
    id = int(re.findall('Monkey (\d):', monkeyHeader.strip())[0])
    startingItemsLine = data.readline()
    startingItems = [int(x) for x in startingItemsLine.split(':')[1].strip().split(', ')]
    operationLine = data.readline()
    operation = operationLine.strip().split(' ')[3:]
    testLine = data.readline()
    test = int(testLine.strip().split(' ')[-1])
    trueLine = data.readline()
    trueMonkey = int(trueLine.strip().split(' ')[-1])
    falseLine = data.readline()
    falseMonkey = int(falseLine.strip().split(' ')[-1])
    monkeys.append(Monkey(id, startingItems, operation, test, trueMonkey, falseMonkey))
    data.readline()

moduloValue = math.prod([monkey.test for monkey in monkeys])

for round in range(10000):
  for monkey in monkeys:
    while len(monkey.items) != 0:
      [newValue, newMonkey] = monkey.examine()
      newValue = newValue % moduloValue
      monkeys[newMonkey].items.append(newValue)

sortedMonkeys = sorted(monkeys, key = lambda a: a.inspectionCount, reverse=True)
monkeyBusiness = sortedMonkeys[0].inspectionCount * sortedMonkeys[1].inspectionCount
print(monkeyBusiness)