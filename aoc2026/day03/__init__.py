"""Day 03 solution."""

import math
from aoc2026.common import read_input_lines


def part_one():
    """Solve part one."""
    data = read_input_lines(3, 1)
    if data is None:
        return None
    total_joltage = 0
    for line in data:
        line_numbers = list(map(int, line))
        tens = max(line_numbers[:-1])
        units = max(line_numbers[(line_numbers.index(tens) + 1):])
        total_joltage += (tens * 10) + units
    return total_joltage


def part_two():
    """Solve part two."""
    data = read_input_lines(3, 2)
    if data is None:
        return None
    total_joltage = 0
    for line in data:
        line_numbers = list(map(int, line))
        next_digit_position = 0
        for digit in reversed(range(1, 13)):
            digit_value = max(line_numbers[next_digit_position:(1 - digit or None)])
            total_joltage += int(math.pow(10, digit - 1)) * digit_value
            next_digit_position = line_numbers.index(digit_value, next_digit_position) + 1
    return total_joltage
