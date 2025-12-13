"""Day 09 solution."""

from collections.abc import Hashable
from collections import deque, namedtuple
from itertools import combinations, pairwise, chain
from typing import List, Self, Tuple
from aoc2026.common import ascending_range_exclusive, ascending_range_inclusive, read_input_lines


class Point:
    """A simple 2D point with x and y coordinates."""
    __slots__ = ('x', 'y')
    
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, other: Self) -> 'Point':
        """Add two points together.
        
        Args:
            other: The point to add
            
        Returns:
            A new Point with the sum of coordinates
        """
        return Point(self.x + other.x, self.y + other.y)


class Coord(Hashable):
    """A 2D coordinate with support for compression.
    
    Attributes:
        x: Original x-coordinate
        y: Original y-coordinate
        x_compressed: Compressed x-coordinate for grid optimisation
        y_compressed: Compressed y-coordinate for grid optimisation
    """
    
    # Class variables
    coords: List['Coord'] = []
    max_compressed_x: int = 0
    max_compressed_y: int = 0
    
    # Named tuple types
    AreaCandidate = namedtuple('AreaCandidate', ['area', 'candidate'])
    
    # Constants for coordinate compression
    COMPRESSION_START_INDEX = -2
    COMPRESSION_START_VALUE = -1
    COMPRESSION_STEP = 2
    
    def __init__(self, data: str) -> None:
        parts = data.split(',')
        self.x = int(parts[0])
        self.y = int(parts[1])
        self._hash = data.__hash__()
        self.x_compressed = 0
        self.y_compressed = 0

    def __hash__(self) -> int:
        return self._hash
    
    def area(self, other: Self) -> int:
        return ((abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1))

    def __repr__(self) -> str:
        return f"{self.x},{self.y}"
    
    @property
    def compressed_point(self) -> Point:
        """Get the compressed point representation.
        
        Returns:
            Point with compressed coordinates
        """
        return Point(self.x_compressed, self.y_compressed)
    
    @classmethod
    def load_coords(cls, data: List[str], compress: bool = False) -> None:
        """Load coordinates from input data into class variable.
        
        Args:
            data: List of coordinate strings
            compress: If True, compress coordinates and store max values
        """
        cls.coords = list(map(Coord, data))
        if compress:
            cls._compress_coordinates()
    
    @classmethod
    def _compress_coordinates(cls) -> None:
        """Compress coordinates to reduce grid size while maintaining relationships.
        
        Stores max_compressed_x and max_compressed_y in class variables.
        """
        x_sorted = sorted(cls.coords, key=lambda c: c.x)
        compressed_x_index = cls.COMPRESSION_START_INDEX
        last_x_value = cls.COMPRESSION_START_VALUE
        for coord in x_sorted:
            if coord.x != last_x_value:
                compressed_x_index += cls.COMPRESSION_STEP
                last_x_value = coord.x
            coord.x_compressed = compressed_x_index

        y_sorted = sorted(cls.coords, key=lambda c: c.y)
        compressed_y_index = cls.COMPRESSION_START_INDEX
        last_y_value = cls.COMPRESSION_START_VALUE
        for coord in y_sorted:
            if coord.y != last_y_value:
                compressed_y_index += cls.COMPRESSION_STEP
                last_y_value = coord.y
            coord.y_compressed = compressed_y_index
        
        cls.max_compressed_x = compressed_x_index
        cls.max_compressed_y = compressed_y_index
    
    @classmethod
    def create_polygon(cls) -> 'Polygon':
        """Create a Polygon using the compressed coordinates from class variables.
        
        Returns:
            Polygon instance created from compressed coordinates
        """
        return Polygon(cls.max_compressed_x, cls.max_compressed_y, cls.coords)
    
    @classmethod
    def create_area_candidates(cls) -> List['Coord.AreaCandidate']:
        """Create sorted list of area candidates from coordinate pairs.
        
        Returns:
            List of AreaCandidate objects sorted by area (largest first)
        """
        return sorted(
            (cls.AreaCandidate(pair[0].area(pair[1]), pair) for pair in combinations(cls.coords, 2)),
            key=lambda x: x.area,
            reverse=True
        )

class Polygon:
    """A polygon represented as a 2D grid for efficient area checking.
    
    The polygon is constructed from a list of coordinates and uses flood fill
    to mark all interior points as filled.
    
    Attributes:
        grid: 2D boolean grid where True represents filled cells
        max_x: Maximum x-coordinate in the compressed grid
        max_y: Maximum y-coordinate in the compressed grid
    """
    
    # Neighbour offsets for flood fill (8-directional)
    NEIGHBOUR_OFFSETS = [
        Point(-1, -1), Point(0, -1), Point(1, -1),
        Point(-1, 0),                Point(1, 0),
        Point(-1, 1),  Point(0, 1),  Point(1, 1)
    ]
    
    # Constants for seed location pattern (looking for: empty, filled, empty)
    SEED_OFFSET_LEFT = -1
    SEED_OFFSET_RIGHT = 1
    SEED_START_OFFSET = 1
    
    def __init__(self, max_x: int, max_y: int, coords: List[Coord]) -> None:
        self.max_x = max_x
        self.max_y = max_y
        self.grid: List[List[bool]] = [[False] * (max_x + 1) for _ in range(max_y + 1)]

        # Draw polygon edges
        for pair in chain(pairwise(coords), [(coords[-1], coords[0])]):
            self._draw_edge(pair[0], pair[1])
        
        seed = self._find_seed_location()
        self._flood_fill(seed)
    
    def _draw_edge(self, start: Coord, end: Coord) -> None:
        """Draw an edge between two coordinates on the grid.
        
        Args:
            start: Starting coordinate
            end: Ending coordinate
        """
        p1, p2 = start.compressed_point, end.compressed_point
        
        if p1.y == p2.y:
            # Horizontal edge
            for x in ascending_range_inclusive(p1.x, p2.x):
                self.grid[p1.y][x] = True
        else:
            # Vertical edge
            for y in ascending_range_inclusive(p1.y, p2.y):
                self.grid[y][p1.x] = True
    
    def _find_seed_location(self) -> Point:
        """Find a seed location inside the polygon for flood fill.
        
        Searches for a pattern where a filled cell is bordered by empty cells on the left and right,
        then returns a point one step to the right as the seed for interior filling.
        
        Returns:
            Point with (x, y) coordinates for the seed location
            
        Raises:
            ValueError: If no suitable seed location is found
        """
        for y in range(1, self.max_y):
            for x in range(1, self.max_x):
                left_empty = not self.grid[y][x + self.SEED_OFFSET_LEFT]
                current_filled = self.grid[y][x]
                right_empty = not self.grid[y][x + self.SEED_OFFSET_RIGHT]
                
                if left_empty and current_filled and right_empty:
                    return Point(x + self.SEED_START_OFFSET, y)
        
        raise ValueError("No seed location found for flood fill")
    
    def _flood_fill(self, seed: Point) -> None:
        """Perform flood fill from seed location to mark all interior points.
        
        Args:
            seed: Starting Point with (x, y) coordinates for flood fill
        """
        process: deque = deque([seed])
        
        while process:
            point = process.popleft()
            if not self.grid[point.y][point.x]:
                self.grid[point.y][point.x] = True
                for offset in self.NEIGHBOUR_OFFSETS:
                    process.append(point + offset)

    def check_candidate(self, candidate: Tuple[Coord, Coord]) -> bool:
        """Check if a rectangular candidate defined by opposing corners fits entirely within the polygon.
        
        Args:
            candidate: Tuple of two Coord objects representing opposing corners
            
        Returns:
            True if the rectangular area is entirely within the polygon
        """
        p1 = candidate[0].compressed_point
        p2 = candidate[1].compressed_point
        
        # Check vertical edges
        if not all(self.grid[y][p1.x] and self.grid[y][p2.x] 
                   for y in ascending_range_inclusive(p1.y, p2.y)):
            return False
        
        # Check horizontal edges
        if not all(self.grid[p1.y][x] and self.grid[p2.y][x] 
                   for x in ascending_range_inclusive(p1.x, p2.x)):
            return False
        
        # Check interior points
        return all(self.grid[y][x] 
                   for y in ascending_range_exclusive(p1.y, p2.y) 
                   for x in ascending_range_exclusive(p1.x, p2.x))


def part_one():
    """Solve part one."""
    data = read_input_lines(9, 1)
    if data is None:
        return None
    Coord.load_coords(data)
    candidates = Coord.create_area_candidates()
    return candidates[0].area


def part_two():
    """Solve part two."""
    data = read_input_lines(9, 2)
    if data is None:
        return None
    Coord.load_coords(data, compress=True)
    polygon = Coord.create_polygon()
    candidates = filter(lambda ac: polygon.check_candidate(ac.candidate), Coord.create_area_candidates())
    return next(candidates).area
