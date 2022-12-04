answer = 0
with open('./04/input.txt', 'r') as data:
  for line in data:
    first, second = line.strip().split(',')
    begin0, end0 = [int(x) for x in first.split('-')]
    begin1, end1 = [int(x) for x in second.split('-')]
    if (begin0 <= begin1 and end0 >= end1) or (begin0 >= begin1 and end0 <= end1):
      answer += 1

print(answer)
