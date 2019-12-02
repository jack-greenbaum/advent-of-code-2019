#!/usr/bin/env python3
from copy import deepcopy


# Run program
def run_program(intcodes, noun, verb):
    copied_memory = deepcopy(intcodes)
    copied_memory[1] = noun
    copied_memory[2] = verb

    index = 0
    while (process_opcode(copied_memory, index)):
        index += 4
    return copied_memory[0]


# Process opcode. Return 1 if an operation ran, 0 if the program should halt.
def process_opcode(intcodes, index):
    opcode = intcodes[index]
    if opcode == 99:
        return 0

    result = 0
    operands = (intcodes[intcodes[index + 1]], intcodes[intcodes[index + 2]])
    if opcode == 1:
        result = operands[0] + operands[1]
    if opcode == 2:
        result = operands[0] * operands[1]

    intcodes[intcodes[index + 3]] = result
    return 1


# Read in the file, and output an array of positions
def read_from_file(filename="input.txt"):
    f = open("./{}".format(filename), "r+")
    return [int(val) for val in f.read().split(',')]


def main():
    intcodes = read_from_file()

    print("Answer for Part 1: {}".format(run_program(intcodes, 12, 2)))

    for noun in range(0, 150):
        for verb in range(0, 150):
            if run_program(intcodes, noun, verb) == 19690720:
                print("Answer for Part 2: {}".format(100 * noun + verb))
                return


if __name__ == "__main__":
    main()
