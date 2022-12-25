import math

digitMap = {
  '2': 2,
  '1': 1,
  '0': 0,
  '-': -1,
  '=': -2,
}

decimalMap = {
  2: '2',
  1: '1',
  0: '0',
  -1: '-',
  -2: '=',
}

def snafuToDecimal(input):
  multiplier = 1
  sum = 0
  for letter in reversed(input):
    sum += multiplier * digitMap[letter]
    multiplier *= 5
  return sum

def decimalToSnafu(input):
  # Add 2s until the number is greater than input
  num = 1
  while snafuToDecimal('2' * num) < input:
    num += 1
  
  tokens = ['2'] * num

  for digit in range(len(tokens)):
    ok = 2
    for test in [2, 1, 0, -1, -2]:
      tokens[digit] = decimalMap[test]
      if snafuToDecimal(''.join(tokens)) >= input:
        ok = test
      else:
        break
    tokens[digit] = decimalMap[ok]
  
  return ''.join(tokens)

sum = 0

with open('./25/input.txt', 'r') as data:
  for line in data:
    sum += snafuToDecimal(line.strip())


print(decimalToSnafu(sum))