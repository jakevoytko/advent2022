#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <sstream>
#include <vector>
#include <algorithm>

using std::ifstream;
using std::cout;
using std::endl;
using std::string;
using std::stringstream;
using std::getline;
using std::vector;

// I'd like to start off by saying that I don't really know C++ and I hope you
// can forgive my many sins.

struct Blueprint {
  unsigned int blueprintID;
  unsigned int oreBotOreCost;
  unsigned int clayBotOreCost;
  unsigned int obsBotOreCost;
  unsigned int obsBotClayCost;
  unsigned int geodeBotOreCost;
  unsigned int geodeBotObsCost;

  Blueprint(
    unsigned int blueprintID_,
    unsigned int oreBotOreCost_,
    unsigned int clayBotOreCost_,
    unsigned int obsBotOreCost_,
    unsigned int obsBotClayCost_,
    unsigned int geodeBotOreCost_,
    unsigned int geodeBotObsCost_
  ): blueprintID(blueprintID_), oreBotOreCost(oreBotOreCost_), clayBotOreCost(clayBotOreCost_), obsBotOreCost(obsBotOreCost_), obsBotClayCost(obsBotClayCost_), geodeBotOreCost(geodeBotOreCost_), geodeBotObsCost(geodeBotObsCost_) {};
};

unsigned int max(std::initializer_list<unsigned int> args) {
  unsigned int max = 0;
  for (unsigned int arg : args) {
    if (arg > max) {
      max = arg;
    }
  }
  return max;
}

unsigned int dfs(unsigned int bestSoFar, unsigned int time, const Blueprint &blueprint, unsigned int ore, unsigned int clay, unsigned int obs, unsigned int geode, unsigned int oreBot, unsigned int clayBot, unsigned int obsBot, unsigned int geodeBot) {
  if (time == 33) {
    return geode > bestSoFar ? geode : bestSoFar;
  }

  // See if it's possible to best the record by building a geode bot every minute, otherwise give up.
  unsigned int possibleGeode = geode;
  // I'm too lazy to do the closed-form solution for this.
  for (unsigned int t = time; t < 33; t++) {
    possibleGeode += geodeBot + (t - time);
    if (possibleGeode >= bestSoFar) {
      break;
    }
  }
  if (possibleGeode < bestSoFar) {
    return bestSoFar;
  }

  time++;
  unsigned int nextOre = ore + oreBot;
  unsigned int nextClay = clay + clayBot;
  unsigned int nextObs = obs + obsBot;
  unsigned int nextGeode = geode + geodeBot;

  if (blueprint.geodeBotOreCost <= ore && blueprint.geodeBotObsCost <= obs) {
    bestSoFar = max({
      bestSoFar,
      dfs(
        bestSoFar, time, blueprint,
        nextOre - blueprint.geodeBotOreCost, nextClay, nextObs - blueprint.geodeBotObsCost, nextGeode,
        oreBot, clayBot, obsBot, geodeBot + 1
      )});
  }

  if (blueprint.obsBotOreCost <= ore && blueprint.obsBotClayCost <= clay && obsBot < blueprint.geodeBotObsCost) {
    bestSoFar = max({
      bestSoFar,
      dfs(
        bestSoFar, time, blueprint,
        nextOre - blueprint.obsBotOreCost, nextClay - blueprint.obsBotClayCost, nextObs, nextGeode,
        oreBot, clayBot, obsBot + 1, geodeBot
      )});
  }

  if (blueprint.clayBotOreCost <= ore && clayBot < blueprint.obsBotClayCost) {
    bestSoFar = max({
      bestSoFar,
      dfs(
        bestSoFar, time, blueprint,
        nextOre - blueprint.clayBotOreCost, nextClay, nextObs, nextGeode,
        oreBot, clayBot + 1, obsBot, geodeBot
      )});
  }

  if (blueprint.oreBotOreCost <= ore && oreBot < max({blueprint.oreBotOreCost, blueprint.clayBotOreCost, blueprint.obsBotOreCost, blueprint.geodeBotOreCost})) {
    bestSoFar = max({
      bestSoFar,
      dfs(
        bestSoFar, time, blueprint,
        nextOre - blueprint.oreBotOreCost, nextClay, nextObs, nextGeode,
        oreBot + 1, clayBot, obsBot, geodeBot
      )});
  }

  bestSoFar = max({
    bestSoFar,
    dfs(
      bestSoFar, time, blueprint,
      nextOre, nextClay, nextObs, nextGeode,
      oreBot, clayBot, obsBot, geodeBot
    )
  });

  return bestSoFar;
}

int main() {
  ifstream data("./input.txt");
  string line;

  auto blueprints = vector<Blueprint>();

  while (getline(data, line)) {
    string token;
    stringstream stream(line);

    // Blueprint %d:
    stream >> token >> token;
    unsigned int blueprintID = atoi(token.c_str());

    // Each clay robot costs %d
    stream >> token >> token >> token >> token >> token;
    unsigned int oreBotOreCost = atoi(token.c_str());

    // ore. Each clay robot costs %d
    stream >> token >> token >> token >> token >> token >> token;
    unsigned int clayBotOreCost = atoi(token.c_str());

    // ore. Each obsidian robot costs %d
    stream >> token >> token >> token >> token >> token >> token;
    unsigned int obsBotOreCost = atoi(token.c_str());

    // ore and %d
    stream >> token >> token >> token;
    unsigned int obsBotClayCost = atoi(token.c_str());

    // clay. Each geode robot costs %d
    stream >> token >> token >> token >> token >> token >> token;
    unsigned int geodeBotOreCost = atoi(token.c_str());

    // ore and %d obsidian.
    stream >> token >> token >> token;
    unsigned int geodeBotObsCost = atoi(token.c_str());

    blueprints.push_back(Blueprint(
      blueprintID, oreBotOreCost, clayBotOreCost, obsBotOreCost, obsBotClayCost, geodeBotOreCost, geodeBotObsCost)
    );
  }
  cout << "blueprint 0" << endl;
  unsigned int zero = dfs(0, 1, blueprints[0], 0, 0, 0, 0, 1, 0, 0, 0);
  cout << "blueprint 1" << endl;
  unsigned int one = dfs(0, 1, blueprints[1], 0, 0, 0, 0, 1, 0, 0, 0);
  cout << "blueprint 2" << endl;
  unsigned int two = dfs(0, 1, blueprints[2], 0, 0, 0, 0, 1, 0, 0, 0);

  cout << (zero * one * two) << endl;
}