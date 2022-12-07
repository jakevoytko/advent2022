import math

filesystem = {}
currentPosition = []
totalSize = 0

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
      totalSize += int(parsedLine[0])
    else:
      raise RuntimeError('Parse error, unrecognized line ', line)

threshold = 30000000 - (70000000 - totalSize)

# Side effects are fun, let's do more of them
smallest = math.inf

def findCleanupDirectorySize(directory):
  global smallest
  global threshold
  size = 0
  for value in directory.values():
    if type(value) is dict:
      innerSize = findCleanupDirectorySize(value)
      size += innerSize
      if innerSize >= threshold:
        smallest = min(smallest, innerSize)
    else:
      size += value
  return size
  
findCleanupDirectorySize(filesystem)
print(smallest)