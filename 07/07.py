#!/usr/bin/env python3
from copy import deepcopy
from itertools import permutations, cycle
import operator

MACHINE_INPUTS = {
    'A': 'E',
    'B': 'A',
    'C': 'B',
    'D': 'C',
    'E': 'D'
}


# Runs an intcode program
class Machine:

    def __init__(self, name, intcodes):
        self.name = name
        self.input_machine = None
        self.output = 0
        self.intcodes = intcodes
        self.index = 0
        self.phase_setting = None
        self.first_input = True
        self.halted = False

    def set_input_machine(self, input_machine):
        self.input_machine = input_machine

    def set_intcodes(self, intcodes):
        self.intcodes = intcodes

    def set_index(self, index):
        self.index = index

    def set_phase_setting(self, phase_setting):
        self.phase_setting = phase_setting

    def set_first_input(self):
        self.first_input = False

    def halt(self):
        self.halted = True

    # Gets a value, respecting positional or immidiate parameters
    def getValue(self, parameters):
        val1 = self.intcodes[self.index + 1] if parameters[0] else self.intcodes[self.intcodes[self.index + 1]]
        val2 = self.intcodes[self.index + 2] if parameters[1] else self.intcodes[self.intcodes[self.index + 2]]
        return (int(val1), int(val2))

    # Runs an instruction, given an operation to perform
    # (add, multipy, less than, equals)
    def intcodeOperation(self, parameters, operation):
        vals = self.getValue(parameters)
        storageLocation = self.intcodes[self.index + 3]
        self.intcodes[storageLocation] = operation(vals[0], vals[1])
        self.set_index(self.index + 4)

    # Runs the input instruction
    def intcodeInput(self):
        writePos = self.intcodes[self.index + 1]
        if self.first_input:
            self.set_first_input()
            self.intcodes[writePos] = self.phase_setting
        else:
            self.intcodes[writePos] = self.get_current_signal()
        self.set_index(self.index + 2)

    # Runs the output instruction
    def intcodeOutput(self, parameters):
        readPos = self.intcodes[self.index + 1] if parameters[0] else self.intcodes[self.intcodes[self.index + 1]]
        self.set_current_signal(readPos)
        self.set_index(self.index + 2)

    # Runs jump commands.
    def intcodeJump(self, parameters, jump_on_true):
        vals = self.getValue(parameters)

        if jump_on_true and vals[0]:
            self.set_index(vals[1])
            return
        elif not jump_on_true and not vals[0]:
            self.set_index(vals[1])
            return

        self.set_index(self.index + 3)

    # Sets the current signal in signals[A-E].txt
    def set_current_signal(self, signal):
        self.output = int(signal)

    # Gets the current signal from signals[A-E].txt
    def get_current_signal(self):
        return self.input_machine.output

    # Processes a single instruction
    def process_instruction(self):
        instr = [x for x in str(self.intcodes[self.index])]

        # Get opcode
        opcode = "".join(instr[-2:]).strip("0")

        # Get parameters
        parameters = [int(x) for x in instr[0:-2]]
        parameters.reverse()
        while len(parameters) < 3:
            parameters.append(0)

        if opcode == "1":
            self.intcodeOperation(parameters, operator.add)
            return 1
        elif opcode == "2":
            self.intcodeOperation(parameters, operator.mul)
            return 1
        elif opcode == "3":
            self.intcodeInput()
            return 1
        elif opcode == "4":
            self.intcodeOutput(parameters)
            return 0
        elif opcode == "5":
            self.intcodeJump(parameters, True)
            return 1
        elif opcode == "6":
            self.intcodeJump(parameters, False)
            return 1
        elif opcode == "7":
            self.intcode0reintcodeOperation(intcodes, index, parameters, operator.__lt__)
            return 1
        elif opcode == "8":
            self.intcodeOperation(intcodes, index, parameters, operator.__eq__)
            return 1
        elif opcode == "99":
            self.halt()
            return -1

    # Processes instructions until output or halt.
    def run_program(self):
        result = 1
        while(result > 0):
            result = self.process_instruction()


# Read in the file, and output an array of positions
def read_from_file(filename="input.txt"):
    f = open("./{}".format(filename), "r+")
    return [int(val) for val in f.read().split(',')]


# Generate all permutations of [0,4] and output to file.
def generate_permutations():
    return [x for x in permutations([i for i in range(5, 10)])]


# Assigns each machine to a phase setting, given a permutation
def assign_phase_settings(machines, machine_names, phase_settings):
    phase_itr = iter(phase_settings)
    for machine_name in machine_names:
        machines[machine_name].set_phase_setting(next(phase_itr))


# Assigns each machine its input machien
def assign_input_machines(machines, machine_names):
    for machine_name in machine_names:
        machines[machine_name].set_input_machine(machines[MACHINE_INPUTS[machine_name]])


def main():
    phase_settings = generate_permutations()
    intcodes = read_from_file('input.txt')
    machine_names = ['A', 'B', 'C', 'D', 'E']

    highest = 0
    for permutation in phase_settings:
        machines = {machine_name: Machine(machine_name, deepcopy(intcodes)) for machine_name in machine_names for _ in range(0, 5)}
        assign_input_machines(machines, machine_names)
        assign_phase_settings(machines, machine_names, permutation)
        for machine_name in cycle(machine_names):
            if machines['E'].halted:
                break
            machines[machine_name].run_program()
        if machines['E'].output > highest:
            highest = machines['A'].get_current_signal()

    print("Answer for Part B: {}".format(highest))


if __name__ == "__main__":
    main()
