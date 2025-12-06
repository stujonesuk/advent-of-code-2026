"""Day 05 solution."""

from typing import Self
from collections.abc import Container, Sized
from aoc2026.common import read_input, read_input_lines
from itertools import combinations

class Range(Container, Sized):
    """A numeric range with inclusive lower and upper bounds.
    
    Attributes:
        lower_bound: The minimum value in the range (inclusive)
        upper_bound: The maximum value in the range (inclusive)
    """

    @classmethod
    def composite(cls, one: Self, two: Self) -> Self | None:
        """Create a composite range from two overlapping ranges.
        
        Args:
            one: First range
            two: Second range
            
        Returns:
            A new Range spanning both inputs if they overlap, None otherwise
        """
        if two.upper_bound >= one.lower_bound and two.lower_bound <= one.upper_bound:
            return cls(f"{min(one.lower_bound, two.lower_bound)}-{max(one.upper_bound, two.upper_bound)}")
        return None

    def __init__(self, data) -> None:
        """Initialize a range from a string like '5-10'.
        
        Args:
            data: String in format 'lower-upper'
        """
        bounds = tuple(map(int, data.split('-')))
        self.lower_bound = bounds[0]
        self.upper_bound = bounds[1]

    def __contains__(self, value: object):
        """Check if a value is within the range.
        
        Args:
            value: Integer value to check
            
        Returns:
            True if value is within bounds (inclusive)
        """
        return type(value) is int and self.lower_bound <= value <= self.upper_bound
    
    def __len__(self) -> int:
        """Get the number of integers in the range.
        
        Returns:
            Count of integers from lower_bound to upper_bound (inclusive)
        """
        return (self.upper_bound - self.lower_bound) + 1


class Ingredients:
    """Container for ingredient ranges and available ingredient values.
    
    Attributes:
        ranges: List of Range objects defining valid ingredient ranges
        available: List of available ingredient values
    """
    
    def __init__(self, data) -> None:
        """Initialize ingredients from input data.
        
        Args:
            data: String with two sections separated by blank line:
                  - First section: ranges (one per line, format 'lower-upper')
                  - Second section: available ingredient values (one per line)
        """
        ranges, ingredients = data.split('\n\n')
        self.ranges = list(map(lambda x: Range(x), ranges.split('\n')))
        self.available = list(map(int, ingredients.split('\n')))

def part_one():
    """Solve part one."""
    data = read_input(5, 1)
    if data is None:
        return None
    ingredients = Ingredients(data)

    return len(
        list(
            filter(
                lambda ingredient: any(
                    map(lambda range: ingredient in range, ingredients.ranges)
                ), ingredients.available
            )
        )
    )


def part_two():
    """Solve part two."""
    data = read_input(5, 2)
    if data is None:
        return None
    ingredients = Ingredients(data)

    # Deduplicate overlaps in ranges
    changes = True
    while changes:
        changes = False
        for (one, two) in combinations(ingredients.ranges, 2):
            if comp := Range.composite(one, two):
                ingredients.ranges.remove(one)
                ingredients.ranges.remove(two)
                ingredients.ranges.append(comp)
                changes = True
                break
    return sum(map(len, ingredients.ranges))
