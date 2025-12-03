"""Shared utilities for Advent of Code solutions."""

import os
from pathlib import Path


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
