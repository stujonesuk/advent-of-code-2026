"""Day 04 solution."""

from typing import List
from aoc2026.common import Grid, GridObject, read_input_lines

class Room(Grid):
    """A grid representing a room with locations."""
    
    def __init__(self, data: List[str]) -> None:
        super().__init__(data, RoomLocation)

class RoomLocation(GridObject):
    """A location within a room grid."""
    
    def count_neighbours(self, matching):
        """Count the number of neighbours matching a specific value.
        
        Args:
            matching: The value to match against
            
        Returns:
            Count of matching neighbours
        """
        return len(list(filter(lambda neighbour: neighbour != self and neighbour is not None and neighbour.value == matching, self.neighbours)))

def part_one():
    """Solve part one."""
    data = read_input_lines(4, 1)
    if data is None:
        return None
    room = Room(data)
    return room.all_objects_count(lambda obj: obj.value == "@" and obj.count_neighbours("@") < 4)


def part_two():
    """Solve part two."""
    data = read_input_lines(4, 2)
    if data is None:
        return None
    room = Room(data)
    initial_count = room.all_objects_count(lambda obj: obj.value == "@")
    while True:
        to_remove = room.all_objects(lambda obj: obj.value == "@" and obj.count_neighbours("@") < 4)
        if len(to_remove) == 0:
            return initial_count - room.all_objects_count(lambda obj: obj.value == "@")
        for obj in to_remove:
            obj.value = "."
