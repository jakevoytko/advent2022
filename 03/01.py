prioritySum = 0

with open('./03/input.txt', 'r') as data:
  for line in data:
    strippedLine = line.strip()
    presence = set()

    for letter in strippedLine[0 : int(len(strippedLine) / 2)]:
      presence.add(letter)

    for letter in strippedLine[int(len(strippedLine) / 2) : len(strippedLine)]:
      if letter in presence:
        if letter >= 'a' and letter <= 'z':
          prioritySum += ord(letter) - ord('a') + 1
        else:
          prioritySum += ord(letter) - ord('A') + 27
        presence.remove(letter)

print(prioritySum)