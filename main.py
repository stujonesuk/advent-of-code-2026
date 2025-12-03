#!/usr/bin/env python3
"""Advent of Code 2026 - Main Entry Point."""

import sys
import argparse
import importlib
import time


def print_usage():
    """Print usage message."""
    print("Usage: uv run main.py [DAY] [PART]")
    print()
    print("Arguments:")
    print("  DAY     Day number (1-12), optional")
    print("  PART    Part number (1 or 2), optional")
    print()
    print("Examples:")
    print("  uv run main.py           # Run all days, all parts")
    print("  uv run main.py 1         # Run day 1, both parts")
    print("  uv run main.py 1 1       # Run day 1, part 1 only")
    print()
    print("Note: Specifying PART without DAY is not allowed.")


def run_solution(day: int, part: int):
    """Run a specific day and part solution."""
    try:
        module_name = f"aoc2026.day{day:02d}"
        module = importlib.import_module(module_name)
        
        if part == 1:
            func = getattr(module, "part_one")
            print(f"Day {day:02d}, Part 1: ", end="", flush=True)
        else:
            func = getattr(module, "part_two")
            print(f"Day {day:02d}, Part 2: ", end="", flush=True)
        
        start_time = time.perf_counter()
        result = func()
        elapsed = time.perf_counter() - start_time
        
        result_str = result if result is not None else "Not implemented"
        print(f"{result_str} ({elapsed*1000:.3f}ms)")
        
    except (ImportError, AttributeError) as e:
        print(f"Error running day {day}, part {part}: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('day', type=int, nargs='?', default=None)
    parser.add_argument('part', type=int, nargs='?', default=None)
    
    try:
        args = parser.parse_args()
    except:
        print_usage()
        sys.exit(1)
    
    # Validate inputs
    if args.day is not None and (args.day < 1 or args.day > 12):
        print("Error: Day must be between 1 and 12")
        print()
        print_usage()
        sys.exit(1)
    
    if args.part is not None and (args.part < 1 or args.part > 2):
        print("Error: Part must be 1 or 2")
        print()
        print_usage()
        sys.exit(1)
    
    # Check for invalid combination: part specified without day
    if args.part is not None and args.day is None:
        print("Error: Cannot specify PART without DAY")
        print()
        print_usage()
        sys.exit(1)
    
    # Run based on parameters
    start_time = time.perf_counter()
    
    if args.day is not None and args.part is not None:
        # Run specific day and part
        run_solution(args.day, args.part)
    elif args.day is not None:
        # Run both parts of specific day
        run_solution(args.day, 1)
        run_solution(args.day, 2)
    else:
        # Run all days, all parts
        for day in range(1, 13):
            run_solution(day, 1)
            run_solution(day, 2)
    
    total_elapsed = time.perf_counter() - start_time
    print(f"\nTotal time: {total_elapsed*1000:.3f}ms")


if __name__ == "__main__":
    main()
