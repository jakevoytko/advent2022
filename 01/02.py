amounts = []

sum = 0

with open('01/input.txt', 'r') as data:
  for line in data:
    stripped_line = line.strip()
    if len(stripped_line) == 0:
      amounts.append(sum)
      sum = 0
    else:
      sum += int(stripped_line)

amounts.append(sum)

amounts.sort(reverse=True)

print(amounts[0] + amounts[1] + amounts[2])