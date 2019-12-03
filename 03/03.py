#!/usr/bin/env python3
from collections import defaultdict


# Read in the file, and output an array of instructions
def read_from_file(filename="input.txt"):
    f = open("./{}".format(filename), "r+")
    wire1, wire2 = f.read().splitlines()
    return [wire1.split(','), wire2.split(',')]


# Calculates Manhattan Distance
def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


# Given a single input, extract the direction and steps
def parse_direction(value):
    return (value[0], int(value[1:]))


# Given path input, finds all the points the wire intersects
def generate_wire_path(path_input):
    current = [0, 0]
    steps = 0

    coordinates = defaultdict(int)
    for instruction in path_input:
        direction, number = parse_direction(instruction)

        if direction == "R":
            for i in range(1, number + 1):
                steps += 1
                if (current[0], current[1] + i) not in coordinates.keys():
                    coordinates[(current[0], current[1] + i)] = steps
            current[1] += number
        elif direction == "D":
            for j in range(1, number + 1):
                steps += 1
                if (current[0] - j, current[1]) not in coordinates.keys():
                    coordinates[(current[0] - j, current[1])] = steps
            current[0] -= number
        elif direction == "L":
            for k in range(1, number + 1):
                steps += 1
                if (current[0], current[1] - k) not in coordinates.keys():
                    coordinates[(current[0], current[1] - k)] = steps
            current[1] -= number
        elif direction == "U":
            for l in range(1, number + 1):
                steps += 1
                if (current[0] + l, current[1]) not in coordinates.keys():
                    coordinates[(current[0] + l, current[1])] = steps
            current[0] += number

    return coordinates


# Find shortest manhattan distance of all points to the origin
def shortest_manhattan_distance(points):
    min_distance = float("inf")
    for point in points:
        man_dist = manhattan_distance((0, 0), point)
        if man_dist < min_distance:
            min_distance = man_dist
    return min_distance


# Finds the point with the shortest signal delay
def shortest_signal_delay(intersection, points1, points2):
    min_delay = float("inf")
    for coordinate in intersection:
        delay = points1[coordinate] + points2[coordinate]
        if delay < min_delay:
            min_delay = delay
    return min_delay


def main():
    wire1, wire2 = read_from_file("input.txt")

    path1 = generate_wire_path(wire1)
    path2 = generate_wire_path(wire2)

    path1_keys = set(path1.keys())
    path2_keys = set(path2.keys())

    intersection_points = path1_keys.intersection(path2_keys)

    print("Answer to Part 1: {}".format(
      shortest_manhattan_distance(intersection_points)))

    print("Answer to Part 2: {}".format(
      shortest_signal_delay(intersection_points, path1, path2)
    ))


if __name__ == "__main__":
    main()
