#!/usr/bin/env python3
from copy import deepcopy
import operator


# Run program
def run_program(intcodes):
    copied_memory = deepcopy(intcodes)

    index = 0
    while(True):
        index = process_instruction(copied_memory, index)


# Gets a value, respecting positional or immidiate parameters
def getValue(intcodes, index, parameters):
    val1 = intcodes[index + 1] if parameters[0] else intcodes[intcodes[index + 1]]
    val2 = intcodes[index + 2] if parameters[1] else intcodes[intcodes[index + 2]]
    return (int(val1), int(val2))


# Runs an instruction, given an operation to perform (add, multipy, less than, equals)
def intcodeOperation(intcodes, index, parameters, operation):
    vals = getValue(intcodes, index, parameters)
    storageLocation = intcodes[index + 3]

    intcodes[storageLocation] = operation(vals[0], vals[1])
    return index + 4


# Runs the input instruction
def intcodeInput(intcodes, index):
    writePos = intcodes[index + 1]
    intcodes[writePos] = input("Enter input: ")
    return index + 2


# Runs the output instruction
def intcodeOutput(intcodes, index, parameters):
    readPos = intcodes[index + 1] if parameters[0] else intcodes[intcodes[index + 1]]
    print(readPos)
    return index + 2


# Runs jump commands.
def intcodeJump(intcodes, index, parameters, jump_on_true):
    vals = getValue(intcodes, index, parameters)

    if jump_on_true and vals[0]:
        return vals[1]
    elif not jump_on_true and not vals[0]:
        return vals[1]

    return index + 3


# Process instruction. Exits the program on halt.
def process_instruction(intcodes, index):
    instr = [x for x in str(intcodes[index])]

    # Get opcode
    opcode = "".join(instr[-2:]).strip("0")

    # Get parameters
    parameters = [int(x) for x in instr[0:-2]]
    parameters.reverse()
    while len(parameters) < 3:
        parameters.append(0)

    if opcode == "1":
        return intcodeOperation(intcodes, index, parameters, operator.add)
    elif opcode == "2":
        return intcodeOperation(intcodes, index, parameters, operator.mul)
    elif opcode == "3":
        return intcodeInput(intcodes, index)
    elif opcode == "4":
        return intcodeOutput(intcodes, index, parameters)
    elif opcode == "5":
        return intcodeJump(intcodes, index, parameters, True)
    elif opcode == "6":
        return intcodeJump(intcodes, index, parameters, False)
    elif opcode == "7":
        return intcodeOperation(intcodes, index, parameters, operator.__lt__)
    elif opcode == "8":
        return intcodeOperation(intcodes, index, parameters, operator.__eq__)
    elif opcode == "99":
        exit()


# Read in the file, and output an array of positions
def read_from_file(filename="input.txt"):
    f = open("./{}".format(filename), "r+")
    return [int(val) for val in f.read().split(',')]


def main():
    intcodes = read_from_file()
    run_program(intcodes)


if __name__ == "__main__":
    main()
