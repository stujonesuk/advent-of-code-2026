"""Day 08 solution."""

from collections.abc import Hashable
from typing import MutableMapping, Self, Set
from math import pow, sqrt
from itertools import combinations, islice
from functools import reduce
from operator import mul
from aoc2026.common import read_input_lines

class Point(Hashable):
    """A 3D point that can be connected to other points in circuits.
    
    Attributes:
        x: X-coordinate
        y: Y-coordinate
        z: Z-coordinate
        circuit: Reference to the circuit this point belongs to (the root Point)
    """

    def __init__(self, data: str) -> None:
        """Initialize a point from comma-separated coordinates.
        
        Args:
            data: String in format 'x,y,z'
        """
        self.x, self.y, self.z = map(int,data.split(','))
        self._hash = data.__hash__()
        self.circuit = None

    def __hash__(self) -> int:
        """Return hash value for this point.
        
        Returns:
            Integer hash value based on coordinate string
        """
        return self._hash
    

    def distance(self, other: Self) -> float:
        """Calculate Euclidean distance to another point.
        
        Args:
            other: Another Point instance
            
        Returns:
            Float distance between this point and the other point
        """
        return sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2) + pow(self.z - other.z, 2))
    
    def connect(self, other: Self):
        """Connect this point to another point, managing circuit membership.
        
        Handles four cases:
        1. Neither point in a circuit: create new circuit
        2. Only other point in a circuit: add this point to that circuit
        3. Only this point in a circuit: add other point to this circuit
        4. Both in different circuits: merge the circuits
        
        Args:
            other: Another Point instance to connect to
        """
        if not self.circuit and not other.circuit:
            circuits[self] = {other}
            self.circuit = self
            other.circuit = self
        elif not self.circuit and other.circuit:
            circuits[other.circuit].add(self)
            self.circuit = other.circuit
        elif self.circuit and not other.circuit:
            circuits[self.circuit].add(other)
            other.circuit = self.circuit
        elif self.circuit and other.circuit and self.circuit != other.circuit:
            # Merge circuits and update references
            update = circuits[other.circuit].union({other.circuit})
            remove = other.circuit
            for circuit in update:
                circuit.circuit = self.circuit
            circuits[self.circuit].update(update)
            del(circuits[remove])
            remove.circuit = self.circuit
            other.circuit = self.circuit

circuits : MutableMapping[Point, Set[Point]]  = {}

def part_one():
    """Solve part one."""
    data = read_input_lines(8, 1)
    if data is None:
        return None
    connect_count = 1000
    circuits.clear()
    for x, _ in islice(
        sorted(
            map(
                lambda x: (x, x[0].distance(x[1])), 
                combinations(map(Point, data), 2)
            ), 
            key = lambda x: x[1]
        ), 
        connect_count
    ):
        x[0].connect(x[1])

    return reduce(
        mul,
        islice(
            sorted(
                map(
                    lambda x: len(x[1]) + 1,
                    circuits.items()
                ), 
                reverse=True
            ),
            3
        ),
        1
    )


def part_two():
    """Solve part two."""
    data = read_input_lines(8, 2)
    if data is None:
        return None
    circuits.clear()
    points = set(map(Point, data))
    for x, _ in sorted(
        map(
            lambda x: (x, x[0].distance(x[1])), 
            combinations(points, 2)
        ), 
        key = lambda x: x[1]
    ):
        x[0].connect(x[1])
        if len(points) > 0:
            if x[0] in points:
                points.remove(x[0])
            if x[1] in points:
                points.remove(x[1])
        if len(points) == 0 and len(circuits) == 1:
            return x[0].x * x[1].x
    return None
