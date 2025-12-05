"""Shared utilities for Advent of Code solutions."""

import os
from pathlib import Path
from typing import Any, List


def get_input_path(day: int, part: int) -> Path | None:
    """Get the path to the input file for a given day and part.
    
    Logic:
    - Look for day##-part#.txt first
    - If that doesn't exist, look for day##.txt
    - If neither exists, return None
    
    Args:
        day: The day number (1-12)
        part: Part number (1 or 2)
        
    Returns:
        Path to the input file, or None if not found
    """
    input_dir = Path(__file__).parent.parent.parent / "input"
    
    # Try part-specific file first
    part_file = input_dir / f"day{day:02d}-part{part}.txt"
    if part_file.exists():
        return part_file
    
    # Try the general day file
    day_file = input_dir / f"day{day:02d}.txt"
    if day_file.exists():
        return day_file
    
    return None


def read_input(day: int, part: int) -> str | None:
    """Read input file for a given day.
    
    Args:
        day: The day number (1-12)
        part: Part number (1 or 2)
        
    Returns:
        The contents of the input file as a string, or None if file not found
    """
    path = get_input_path(day, part)
    if path is None:
        return None
    with open(path) as f:
        return f.read()


def read_input_lines(day: int, part: int) -> list[str] | None:
    """Read input file for a given day as a list of lines.
    
    Args:
        day: The day number (1-12)
        part: Part number (1 or 2)
        
    Returns:
        List of lines from the input file (stripped of trailing whitespace), or None if file not found
    """
    content = read_input(day, part)
    if content is None:
        return None
    return content.strip().split('\n')


class Grid:
    """A 2D grid structure for storing and accessing grid objects.
    
    Attributes:
        max_y: Maximum y-coordinate (0-indexed)
        max_x: Maximum x-coordinate (0-indexed)
        objects: Dictionary of grid objects indexed by y then x coordinates
    """
    
    def __init__(self, data: List[str], data_object_type) -> None:
        """Initialize a grid from string data.
        
        Args:
            data: List of strings representing rows of the grid
            data_object_type: Class to instantiate for each grid position
        """
        self.max_y = len(data) - 1
        self.max_x = len(data[0]) - 1
        self.objects = {
            y: {
                x: data_object_type(self, data[y][x], x, y)
                for x in range(0, self.max_x + 1)
            }
            for y in range(0, self.max_y + 1)
        }

        for obj in self._all_objects_generator():
            obj.populate_neighbours()

    def _all_objects_generator(self, criteria = None):
        """Generate all grid objects, optionally filtered by criteria.
        
        Args:
            criteria: Optional function to filter objects
            
        Yields:
            Grid objects matching the criteria
        """
        for row in self.objects.values():
            for obj in row.values():
                if criteria is None or criteria(obj):
                    yield obj
    
    def all_objects(self, criteria = None):
        """Get all grid objects as a list.
        
        Args:
            criteria: Optional function to filter objects
            
        Returns:
            List of grid objects matching the criteria
        """
        return list(self._all_objects_generator(criteria))
    
    def all_objects_count(self, criteria = None):
        """Count all grid objects.
        
        Args:
            criteria: Optional function to filter objects
            
        Returns:
            Count of grid objects matching the criteria
        """
        return len(self.all_objects(criteria))

class GridObject:
    """An object at a specific position in a grid.
    
    Attributes:
        grid: The parent Grid instance
        value: The value stored at this position
        x: X-coordinate in the grid
        y: Y-coordinate in the grid
        neighbours: List of 9 neighbouring objects (including self at index 4)
    """
    
    def __init__(self, grid, value: str, x: int, y: int) -> None:
        """Initialize a grid object.
        
        Args:
            grid: The parent Grid instance
            value: The value at this grid position
            x: X-coordinate
            y: Y-coordinate
        """
        self.grid = grid
        self.value = value
        self.x = x
        self.y = y
        self.neighbours: List[Any] = [None] * 9
        self.neighbours[4] = self

    def populate_neighbours(self):
        """Populate the neighbours list with adjacent grid objects.
        
        Neighbours are indexed as follows:
        0 1 2
        3 4 5
        6 7 8
        
        Where 4 is self, and None is used for positions outside the grid.
        """
        if self.y > 0:
            if self.x > 0:
                self.neighbours[0] = self.grid.objects[self.y - 1][self.x - 1]
            self.neighbours[1] = self.grid.objects[self.y - 1][self.x]
            if self.x < self.grid.max_x:
                self.neighbours[2] = self.grid.objects[self.y - 1][self.x + 1]
        if self.x > 0:
            self.neighbours[3] = self.grid.objects[self.y][self.x - 1]
        if self.x < self.grid.max_x:
            self.neighbours[5] = self.grid.objects[self.y][self.x + 1]
        if self.y < self.grid.max_y:
            if self.x > 0:
                self.neighbours[6] = self.grid.objects[self.y + 1][self.x - 1]
            self.neighbours[7] = self.grid.objects[self.y + 1][self.x]
            if self.x < self.grid.max_x:
                self.neighbours[8] = self.grid.objects[self.y + 1][self.x + 1]
     