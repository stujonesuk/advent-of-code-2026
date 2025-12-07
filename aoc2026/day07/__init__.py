"""Day 07 solution."""

from collections.abc import Hashable
from typing import List, MutableMapping, Self, Set, Tuple
from aoc2026.common import read_input, read_input_lines, Grid, GridObject


class Manifold(Grid):
    """A grid representing a tachyon manifold."""
    
    def __init__(self, data: List[str]) -> None:
        """Initialize a manifold from grid data.
        
        Args:
            data: List of strings representing the manifold grid
        """
        self.start_location : ManifoldLocation
        super().__init__(data, ManifoldLocation)

    def introduce_beam(self):
        """Introduce a tachyon beam into the manifold.
        
        Processes the beam propagation through the manifold, activating splitters
        and tracking paths from the start location.
        """
        current_row : MutableMapping[ManifoldLocation, Set[ManifoldLocation]] = { }
        next_row : MutableMapping[ManifoldLocation, Set[ManifoldLocation]] = {
            self.start_location: set()
        }

        while len(next_row) > 0:
            current_row = next_row
            next_row = {}

            while len(current_row) > 0:
                beam_to, beam_from = current_row.popitem()
                path_count = max(sum(map(lambda x: x.path_count, beam_from)),1)
                for next_beam_to in beam_to.introduce_beam(path_count):
                    if next_beam_to not in next_row:
                        next_row[next_beam_to] = {beam_to}
                    else:
                        next_row[next_beam_to].add(beam_to)
            


class ManifoldLocation(GridObject, Hashable):
    """A location within a tachyon manifold."""

    def __init__(self, grid, value: str, x: int, y: int) -> None:
        """Initialize a manifold location.
        
        Args:
            grid: The parent Manifold grid
            value: Character representing the location type
            x: X-coordinate
            y: Y-coordinate
        """
        super().__init__(grid, value, x, y)
        self._hash = f"{x},{y}".__hash__()
        self.is_splitter = value == "^"
        self.path_count = 0
        if value == "S":
            grid.start_location = self
        self.splitter_activated = False
    
    def introduce_beam(self, path_count: int)-> Set[Self]:
        """Introduce a beam to this location and determine next locations.
        
        Updates the location state and determines which neighboring locations
        the beam should propagate to. Handles splitter activation.
        
        Args:
            path_count: Number of paths reaching this location
            
        Returns:
            Set of ManifoldLocation objects the beam propagates to
        """
        beam_to: Set[Self] = set()
        self.path_count = path_count
        self.value = '|'
        if self.neighbours[7]:
            if self.neighbours[7].is_splitter:
                self.neighbours[7].splitter_activated = True
                if self.neighbours[6]:
                    beam_to.add(self.neighbours[6])
                if self.neighbours[8]:
                    beam_to.add(self.neighbours[8])
            else:
                beam_to.add(self.neighbours[7])
        return beam_to
    
    def __hash__(self) -> int:
        """Return hash value for this location based on coordinates.
        
        Returns:
            Integer hash value
        """
        return self._hash

def part_one():
    """Solve part one."""
    data = read_input_lines(7, 1)
    if data is None:
        return None
    manifold = Manifold(data)
    manifold.introduce_beam()
    return manifold.all_objects_count(lambda o: o.splitter_activated)


def part_two():
    """Solve part two."""
    data = read_input_lines(7, 2)
    if data is None:
        return None
    manifold = Manifold(data)
    manifold.introduce_beam()
    return sum(map(lambda x: x.path_count, manifold.all_objects(lambda o: o.neighbours[7] is None)))
