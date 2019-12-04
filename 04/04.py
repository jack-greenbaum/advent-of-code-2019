#!/usr/bin/env python3
from collections import defaultdict

START = 183564
END = 657474


# Given a number, check that there is at least one pair and consecutives do not decrease.
def matches_criteria(number, exact_doubles=False):
    str_number = str(number)
    current = 0
    digits = defaultdict(int)
    for digit in str_number:
        digit = int(digit)
        if digit < current:
            return False
        elif digit == current:
            digits[digit] += 1
            current = digit
        elif digit > current:
            digits[digit] += 1
            current = digit

    if exact_doubles:
        if 2 in digits.values():
            return True
    else:
        for count in digits.values():
            if count >= 2:
                return True
    return False


def main():
    count = 0
    for num in range(START, END):
        if matches_criteria(num):
            count += 1

    print("Answer for Part 1: {}".format(count))

    count = 0
    for num in range(START, END):
        if matches_criteria(num, True):
            count += 1

    print("Answer for Part 2: {}".format(count))


if __name__ == "__main__":
    main()
