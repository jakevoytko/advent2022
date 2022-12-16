import re
import math

class Valve:
  def __init__(self, label, neighbors, rate):
    self.label = label
    self.neighbors = neighbors
    self.rate = rate
    self.opened = False

allValves = {}

with open('./16/input.txt', 'r') as data:
  for line in data:
    match = re.search(r'Valve (\w\w) has flow rate=(\d+); tunnels? leads? to valves? ((\w\w(, )?)+)', line.strip())
    label = match.group(1)
    rate = int(match.group(2))
    neighbors = match.group(3).split(', ')
    allValves[label] = Valve(label, neighbors, rate)


# Floyd-Warshal algorithm to calculate the distance between each pair of valves.
travelMap = {a:{b:math.inf for b in allValves.keys()} for a in allValves.keys()}
for destinationLabel, valve in allValves.items():
  travelMap[destinationLabel][destinationLabel] = 0
  for neighbor in valve.neighbors:
    travelMap[destinationLabel][neighbor] = 1
for k in allValves.keys():
  for i in allValves.keys():
    for j in allValves.keys():
      if travelMap[i][j] > travelMap[i][k] + travelMap[k][j]:
        travelMap[i][j] = travelMap[i][k] + travelMap[k][j]

# Run multiple simulations in parallel in rounds. In each round, look at each of the simulations
# and calculate how long it takes to traverse to all of the unvisited.
# Deduplicate the simulations by sorting the list of already-visited nodes in each simulation
# and computing hash values. Keep the conflicting simulation with the largest flow value.

class SimulationState:
  def __init__(self, currentValve, alreadyVisited, unvisited, timeRemaining, totalFlow):
    self.currentValve = currentValve

    self.alreadyVisited = alreadyVisited

    self.unvisited = unvisited
    self.timeRemaining = timeRemaining
    self.totalFlow = totalFlow

  def __hash__(self): # Abuse hash out of laziness
    values = list(self.alreadyVisited)
    values.sort()
    return hash(tuple(values))

originState = SimulationState('AA', set(), set([valve.label for valve in allValves.values() if valve.rate > 0]), 26, 0)
simulationStates = {originState: originState}

allStates = {}

# How this differs from part 1:
# Calculate the best times for all the valid traversals. Then, create a list of all of the states
# sorted from max flow to min flow. Then look at all of the elements pairwise, and look for disjoint
# sets. The answer is the sum of the flows of the largest disjoint sets.

while True:
  nextSimulationStates = {}

  for state in simulationStates:
    currentValve = allValves[state.currentValve]
    for destinationLabel in state.unvisited:
      destinationValve = allValves[destinationLabel]
      timeAfterTraversalAndOpen = state.timeRemaining - travelMap[state.currentValve][destinationLabel] - 1
      if timeAfterTraversalAndOpen < 0:
        continue

      alreadyVisited = set(state.alreadyVisited)
      alreadyVisited.add(destinationLabel)
      unvisited = set(state.unvisited)
      unvisited.remove(destinationLabel)

      flow = state.totalFlow + timeAfterTraversalAndOpen * destinationValve.rate

      newState = SimulationState(destinationLabel, alreadyVisited, unvisited, timeAfterTraversalAndOpen, flow)
      if newState in nextSimulationStates:
        if newState.totalFlow > nextSimulationStates[newState]:
          nextSimulationStates[newState] = newState
      else:
        nextSimulationStates[newState] = newState

      if newState in allStates:
        if newState.totalFlow > allStates[newState]:
          allStates[newState] = newState
      else:
        allStates[newState] = newState

  if len(nextSimulationStates) == 0:
    break
  simulationStates = nextSimulationStates

# Calculate the max flow for all disjoint states
sortedStates = list(allStates.values())
sortedStates.sort(key = lambda a: a.totalFlow, reverse=True)
maxFlow = 0
for personState in sortedStates:
  # Just in case the optimal value is done by one person
  maxFlow = max(maxFlow, personState.totalFlow)
  for elephantState in sortedStates:
    if len(personState.alreadyVisited.intersection(elephantState.alreadyVisited)) > 0:
      continue
    maxFlow = max(maxFlow, personState.totalFlow + elephantState.totalFlow)
    if maxFlow - personState.totalFlow - elephantState.totalFlow > 0:
      break

print(maxFlow)