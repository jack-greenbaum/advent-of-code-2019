#!/usr/bin/env python3
from copy import deepcopy
from collections import deque


class Planet:
    # The name of the planet
    name = None

    # The planets that orbit this planet.
    children = None

    # The planets this planet orbits.
    parents = None

    # The number of planets this planet indirectly or directly orbits.
    degree = 0

    # Constructor
    def __init__(self, name):
        self.name = name
        self.children = set()
        self.parents = set()

    def __repr__(self):
        return self.name

    # Defines the hash function, so we can use this as a key to a dictionary.
    def __hash__(self):
        return hash(self.name)

    # Adds a child to this planet.
    def addChild(self, child):
        self.children.add(child)

    # Adds a parent to this planet
    def addParent(self, parent):
        self.parents.add(parent)

    # Given a parent, updates this planet's degree
    def updateDegree(self, parent):
        self.degree = parent.degree + 1


# Creates all planets
def create_planets(orbits):
    planets = {}
    for orbit in orbits:
        for planet in orbit:
            if planet not in planets:
                planets[planet] = Planet(planet)
        planets[orbit[0]].addChild(planets[orbit[1]])
        planets[orbit[1]].addParent(planets[orbit[0]])
    return planets


# Calculate the degree of each planet, using a BFS from COM
def calculate_degree(planets):
    q = deque()
    q.append(planets['COM'])

    while len(q) > 0:
        current = q.pop()
        for child in current.children:
            child.updateDegree(current)
            q.append(child)


# Calculates the minimum distance to get from planet A to planet B
def min_jumps(planetA, planetB, planets):
    explored = {planetA: planetA}
    nextQ = deque()
    nextQ.append(planetA)

    count = 0
    while True:
        currentQ = deepcopy(nextQ)
        nextQ.clear()
        count += 1
        while len(currentQ) > 0:
            current = planets[currentQ.pop()]
            for child in current.children:
                if child.name == 'SAN':
                    return count - 2
                if child.name not in explored:
                    explored[child.name] = child.name
                    nextQ.append(child.name)
            for parent in current.parents:
                if parent.name == 'SAN':
                    return count - 2
                if parent not in explored:
                    explored[parent.name] = parent.name
                    nextQ.append(parent.name)


# Read in the file
def read_from_file(filename="input.txt"):
    f = open("./{}".format(filename), "r+").read().splitlines()

    return [line.split(')') for line in f]


def main():
    orbits = read_from_file()
    planets = create_planets(orbits)
    calculate_degree(planets)

    count = 0
    for planet in planets.values():
        count += planet.degree
    print("Answer for Part A: {}".format(count))

    print("Answer for Part B: {}".format(min_jumps('YOU', 'SAN', planets)))


if __name__ == "__main__":
    main()
