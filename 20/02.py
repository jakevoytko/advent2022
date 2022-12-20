class Node:
  def __init__(self, val):
    self.val = val
    self.left = None
    self.right = None

def cllToList(node):
  results = [node.val]
  iter = node.right
  while iter != node:
    results.append(iter.val)
    iter = iter.right
  return results

head = None
nodes = []

with open('./20/input.txt', 'r') as data:
  for line in data:
    node = Node(811589153 * int(line.strip()))
    nodes.append(node)
    if head is None:
      head = node
      head.left = node
      head.right = node
    else:
      node.left = head.left
      node.left.right = node
      node.right = head
      head.left = node

for _ in range(10):
  for node in nodes:
    other = node
    if node.val % (len(nodes) - 1)== 0:
      continue
    if node.val > 0:
      if head == node:
        head = node.right
      other = node.right
      node.left.right = node.right
      node.right.left = node.left

      for _ in range(node.val % (len(nodes) - 1) - 1):
        other = other.right

    elif node.val < 0:
      if head == node:
        head = node.right
      other = node.left
      node.left.right = node.right
      node.right.left = node.left
      for _ in range(-node.val % (len(nodes) - 1) - 1):
        other = other.left
      other = other.left

    node.left = other
    node.right = other.right
    other.right.left = node
    other.right = node

iter = head
while iter.val != 0:
  iter = iter.right

sum = 0
for i in range(3000):
  iter = iter.right
  if (i + 1) in [1000, 2000, 3000]:
    sum += iter.val

print(sum)
