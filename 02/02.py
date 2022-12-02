scoring_table = {
  'A': {
    'X': 3,
    'Y': 1,
    'Z': 2,
  },
  'B': {
    'X': 1,
    'Y': 2,
    'Z': 3,
  },
  'C': {
    'X': 2,
    'Y': 3,
    'Z': 1,
  }
}
win_table = {
  'X': 0,
  'Y': 3,
  'Z': 6,
}
score = 0
with open('02/input.txt', 'r') as data:
  for line in data:
    [other, strategy] = line.strip().split(' ')
    score += win_table[strategy]
    score += scoring_table[other][strategy]
print(score)