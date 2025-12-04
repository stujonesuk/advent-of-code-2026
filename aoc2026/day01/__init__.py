"""Day 01 solution."""

import math
from aoc2026.common import read_input_lines

class Dial:
    """Models the Dial"""
    def __init__(self):
        """Initialises the Dial's initial position, counters, and size."""
        self.position = 50
        self._size = 100
        self.zero_count = 0
        self.zero_click = 0

    def turn(self, instruction):
        """
        Simulates a turn instruction, counting clicks through zero and
        instructions that land on zero.
        """
        multiplier = -1 if instruction[0] == 'L' else 1
        distance = int(instruction[1:])
        whole_rotations = math.floor(distance / self._size)
        effective_distance = distance - (whole_rotations * self._size)
        
        original_position = self.position
        new_position = original_position + (multiplier * effective_distance)
        zero_passed = 1 if ((new_position < 0 and original_position > 0) or new_position == 0 or new_position >= self._size) else 0
        
        self.position = new_position % self._size
        self.zero_click += whole_rotations + zero_passed

        if self.position == 0:
            self.zero_count += 1

def part_one():
    """Solve part one."""
    data = read_input_lines(1, 1)
    if data is None:
        return None
    dial = Dial()
    for line in data:
        dial.turn(line)

    return dial.zero_count


def part_two():
    """Solve part two."""
    data = read_input_lines(1, 2)
    if data is None:
        return None
    dial = Dial()
    for line in data:
        dial.turn(line)

    return dial.zero_click
