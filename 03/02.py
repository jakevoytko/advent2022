prioritySum = 0

contents = None
with open('./03/input.txt', 'r') as data:
  contents = data.readlines()
for i in range(len(contents)):
  contents[i] = contents[i].strip()

prioritySum = 0

for i in range(0, len(contents), 3):
  presence = set([*contents[i]]).intersection(set([*contents[i+1]])).intersection(set([*contents[i+2]]))
  badge = presence.pop()
  if badge >= 'a' and badge <= 'z':
    prioritySum += ord(badge) - ord('a') + 1
  else:
    prioritySum += ord(badge) - ord('A') + 27

print(prioritySum)