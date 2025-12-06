"""Day 06 solution."""

from aoc2026.common import read_input_lines
from operator import add, mul
from functools import reduce


OPS = {
    "+" : (add, 0),
    "*" : (mul, 1)
}

def part_one():
    """Solve part one."""
    data = read_input_lines(6, 1)
    if data is None:
        return None

    rows = list(map(lambda x: x.split(), data))

    return sum(
        (
            reduce(
                OPS[operator][0], 
                (
                    int(v[ix])
                    for v in rows[:-1]
                ), 
                OPS[operator][1])
            for ix, operator in enumerate(rows[-1])
        )
    )


def part_two():
    """Solve part two."""
    data = read_input_lines(6, 2)
    if data is None:
        return None

    total = 0
    current_operator = None
    current_operand = 0
    for i in range(0, len(data[0])):
        if not current_operator:
            current_operator, current_operand = OPS[data[-1][i]]
        if all(map(lambda r: r[i] == " ",data[:-1])):
            current_operator = None
            total += current_operand
            current_operand = 0
        else:
            current_operand = current_operator(current_operand, int(reduce(lambda s, r: s + r[i], data[:-1], "")))
    total += current_operand
    return total
