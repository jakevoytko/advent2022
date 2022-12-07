filesystem = {}
currentPosition = []

def iterateTo():
  current = filesystem
  for directory in currentPosition:
    current = current[directory]
  return current

def addDirectory(name):
  currentDirectory = iterateTo()
  currentPosition.append(name)
  if name in currentDirectory:
    raise RuntimeError('Duplicate directory {} added to {}'.format(name, currentDirectory))
  currentDirectory[name] = {}

def addFile(size, name):
  currentDirectory = iterateTo()
  currentDirectory[name] = size

with open('./07/input.txt', 'r') as data:
  for line in data:
    parsedLine = line.strip().split(' ')
    if parsedLine[0] == '$':
      if parsedLine[1] == 'cd':
        if parsedLine[2] == '..':
          currentPosition.pop()
        else:
          addDirectory(parsedLine[2])
      elif parsedLine[1] == 'ls':
        pass
    elif parsedLine[0] == 'dir':
      pass
    elif parsedLine[0].isnumeric():
      addFile(int(parsedLine[0]), parsedLine[1])
    else:
      raise RuntimeError('Parse error, unrecognized line ', line)

def findSmallDirectories(directory):
  totalSize = 0
  smallDirectorySum = 0

  for value in directory.values():
    if type(value) is dict:
      subAnswer, subSmallDirectorySum = findSmallDirectories(value)
      totalSize += subAnswer
      smallDirectorySum += subSmallDirectorySum
      if subAnswer < 100000:
        smallDirectorySum += subAnswer
    else:
      totalSize += value
  
  return totalSize, smallDirectorySum

_, answer = findSmallDirectories(filesystem)
print(answer)