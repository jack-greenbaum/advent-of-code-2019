#!/usr/bin/env python3
from math import floor


# Read input from file and split by line.
def read_from_file(filename="input.txt"):
    f = open("./{}".format(filename), "r+")
    return f.read().splitlines()


# Determine fuel for a given module's mass.
# Divide mass by 3, round down, subtract 2.
def get_required_fuel(module_mass, fuel_requires_fuel=False):
    fuel = floor(module_mass / 3) - 2
    if not fuel_requires_fuel or fuel < 0:
        return(max(fuel, 0))
    return(fuel + get_required_fuel(fuel, True))


def main():
    total = 0
    total_with_fuel_mass = 0
    for module_mass in read_from_file():
        total += get_required_fuel(int(module_mass))
        total_with_fuel_mass += get_required_fuel(int(module_mass), True)

    print("Total for Part 1: {}".format(total))
    print("Total for Part 2: {}".format(total_with_fuel_mass))


if __name__ == "__main__":
    main()
