scoring_table = {
  'A': 1,
  'B': 2,
  'C': 3,
  'X': 1,
  'Y': 2,
  'Z': 3,
}
win_table = {
  'X': { # Rock
    'A': 3,
    'B': 0,
    'C': 6,
  },
  'Y': { # Paper
    'A': 6,
    'B': 3,
    'C': 0,
  },
  'Z': { # Scissors
    'A': 0,
    'B': 6,
    'C': 3,
  }
}
score = 0
with open('02/input.txt', 'r') as data:
  for line in data:
    [other, me] = line.strip().split(' ')
    score += scoring_table[me]
    score += win_table[me][other]
print(score)