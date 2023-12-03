import sys

from typing import List, Tuple

# Type definitions
NumberLocation = Tuple[str, int, int]

"""
This function finds numbers within a grid of characters.

It returns a list of tuples. Each tuple contains the string
representation of a found number, its row index, and the index
of the column the number starts on.
"""
def locateNumbers(grid: List[str]) -> List[NumberLocation]:
    locations: List[NumberLocation] = []
    curNum: str = ""

    x: int = 0
    y: int = 0
    line: str = ""
    char: str = ""

    # Go through the grid one character at a time. Read left to right,
    # then top to bottom
    for y, line in enumerate(grid):
        for x, char in enumerate(line):

            # If the current character is a digit, add it to whatever number we're currently building up
            if char.isdigit():
                curNum += char

            # If it's not a digit, we might've hit the end of a number we were already reading, or we're
            # reading a bunch of characters we don't care about (either spaces or symbols)
            else:
                # If we were previously reading a number but found the end, make a note of this number's
                # value and position in the grid, then reset the "current" number
                if len(curNum) > 0:
                    locations.append((curNum, y, x - len(curNum)))
                    curNum = ""

        # If we get to the end of the line and were reading a number, make a note of the number's value
        # and position in the grid, then reset the "current" number
        if len(curNum) > 0:
            locations.append((curNum, y, x - len(curNum) + 1))
            curNum = ""

    return locations

"""
This function takes in a grid and a list of numbers in the grid (and their locations),
then filters out any numbers that aren't adjacent to a symbol

The returned list contains all elements of the "location" parameter that are located in
the given grid that are adjacent to a symbol
"""
def filterNumbers(grid: List[str], locations: List[NumberLocation]) -> List[NumberLocation]:
    toRemove: List[NumberLocation] = []

    num: str = ""
    x: int = 0
    y: int = 0
    row: int = 0
    column: int = 0

    # Iterate through all the found numbers in the grid
    for num, y, x in locations:

        # Get all of the neighboring grid cells around this number. That's all cells above, below, to the side of,
        # and diagonally adjacent to the current number
        neighbors = [(row, column) for row in range(y - 1, y + 2) for column in range(x - 1, x + len(num) + 1)]

        # Remove any of the neighbors that are outside the grid
        filtered = [(row, column) for (row, column) in neighbors if row >= 0 and column >= 0 and row < len(grid) and column < len(grid[0])]

        # Iterate through all of the neighboring cells of the current number in the grid. Assume we need to remove the
        # current number from the list of valid numbers
        keep = False
        for row, column in filtered:
            cell = grid[row][column]

            # If we've found a valid symbol that isn't "empty" (a '.'), we can stop searching neighboring cells. We know
            # we need to keep this number
            if not cell.isdigit() and not cell.isalpha() and cell != '.':
                keep = True
                break

        # If we didn't find a neighboring symbol, mark the current number for removal
        if not keep:
            toRemove.append((num, y, x))

    # Return all items in the original "locations" list that we haven't marked for removal
    return [l for l in locations if l not in toRemove]

"""
Main function
"""
if __name__ == "__main__":
    file: str = sys.argv[1]
    lines: List[str] = []

    # Read input file
    with open(file, 'r') as f:
        lines = [l.strip() for l in f if len(l) > 0]

    # Find all numbers
    numberLocations: List[NumberLocation] = locateNumbers(lines)

    # Remove any that aren't next to a symbol
    filteredNumbers: List[NumberLocation] = filterNumbers(lines, numberLocations)

    # Convert the remaining numbers to actual numbers
    validNumbers: List[int] = [int(n) for n, _, _ in filteredNumbers]

    # Print the sum of all valid numbers
    print(sum(validNumbers))
