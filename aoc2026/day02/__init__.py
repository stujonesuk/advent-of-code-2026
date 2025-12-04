"""Day 02 solution."""

from typing import Set, MutableMapping, List, Tuple, Iterator
from aoc2026.common import read_input

class Ranges:
    """Models the Ranges"""
    def __init__(self, data: str, allowed_splits : Set[int] | None = None):
        """Parses the data to get the ranges."""
        ranges = data.split(',')
        self.ranges = [tuple(map(int, r.split('-'))) for r in ranges]
        self._allowed_splits = allowed_splits
        self._segments: MutableMapping[int, List[List[Tuple[int,int]]]] = {}

    def _get_segments(self, length: int) -> List[List[Tuple[int,int]]]:
        """Gets the sets of segments of equal length that a string of {length} can be carved up into."""
        if not length in self._segments:
            divisors = [r for r in range(2, length + 1) if (self._allowed_splits is None or r in self._allowed_splits) and length % r == 0]
            segment_lengths = {d : length // d for d in divisors}
            self._segments[length] = [[(n, n + segment_lengths[d]) for n in reversed(range(0, length - segment_lengths[d] + 1, segment_lengths[d]))] for d in divisors]
        return self._segments[length]

    def get_repeated_values(self) -> Iterator[int]:
        """Returns an Iterator that yields values within ranges if they are made up of repeated values."""
        for r in self.ranges:
            for n in range(r[0],r[1]+1):
                n_text = str(n)
                n_text_length = len(n_text)
                for segment_set in self._get_segments(n_text_length):
                    previous = None
                    include = True
                    for s in segment_set:
                        next = n_text[s[0]:s[1]]
                        if previous and previous != next:
                            include = False
                            break
                        else:
                            previous = next
                    if include:
                        yield n
                        break

def part_one():
    """Solve part one."""
    data = read_input(2, 1)
    if data is None:
        return None
    ranges = Ranges(data, {2})
    return sum(ranges.get_repeated_values())

def part_two():
    """Solve part two."""
    data = read_input(2, 2)
    if data is None:
        return None
    ranges = Ranges(data)
    return sum(ranges.get_repeated_values())
