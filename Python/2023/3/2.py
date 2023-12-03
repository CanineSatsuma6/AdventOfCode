import sys

from typing import List, Tuple

# Type definitions
NumberLocation = Tuple[str, int, int]
Gear = Tuple[int, int]

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
This function finds gears within the given grid. The returned list of
gears has been validated, i.e. all gears are adjacent to exactly 2 numbers
"""
def findGears(grid: List[str]) -> List[Gear]:
    gears: List[Gear] = []

    y: int = 0
    x: int = 0
    line: str = ""
    char: str = ""

    # Go through the grid one character at a time. Read left to right,
    # then top to bottom
    for y, line in enumerate(grid):
        for x, char in enumerate(line):

            # If we've found a potential gear, make sure it's valid. If
            # it is, add it to the list of gears in the grid
            if char == '*':
                gear: Gear = (y, x)
                if isValidGear(grid, gear):
                    gears.append(gear)

    return gears

"""
This function determines if a gear within the grid is adjacent
to EXACTLY 2 numbers.

This function returns True if the gear is adjacent to EXACTLY 2
numbers, otherwise it returns False.
"""
def isValidGear(grid: List[str], gear: Gear) -> bool:
    x: int = 0
    y: int = 0

    y, x = gear

    # Get all of the neighbors of the current gear's location
    neighbors: List[Tuple[int, int]] = [(row, column) for row in range(y - 1, y + 2) for column in range(x - 1, x + 2) if (row, column) != gear]

    # Filter out any neighbors outside the grid
    validNeighbors: List[Tuple[int, int]] = [(row, column) for (row, column) in neighbors if row >= 0 and column >= 0 and row < len(grid) and column < len(grid[0])]

    # The total count of numbers adjacent to the gear. Must be exactly 2 for a valid gear
    numNumericNeighbors: int = 0

    # Figure out which neighboring cells are in the row above the gear, and how many of them contain a number
    neighborsAbove: List[Tuple[int, int]] = [(row, column) for (row, column) in validNeighbors if row == y - 1]
    numNumericNeighborsAbove: int = len([(row, column) for (row, column) in neighborsAbove if grid[row][column].isdigit()])

    # Figure out which neighboring cells are in the row below the gear, and how many of them contain a number
    neighborsBelow: List[Tuple[int, int]] = [(row, column) for (row, column) in validNeighbors if row == y + 1]
    numNumericNeighborsBelow: int = len([(row, column) for (row, column) in neighborsBelow if grid[row][column].isdigit()])

    # There are at most 3 neighbors above the gear (up, up-left, and up-right)
    # If only one of those neighbors is a number, we have exactly one adjacent number.
    # If all three are numbers, we have one long number (i.e. with at least 3 digits) adjacent above the gear
    if numNumericNeighborsAbove in [1, 3]:
        numNumericNeighbors += 1

    # If two of the neighboring cells above the gear are numbers, there's two possible situations we could be in:
    # - The two numbers are adjacent to each other and therefore make up one number adjacent to the gear
    # - There's a space between the end of one number and the start of the next, so there's two numbers adjacent to the gear
    elif numNumericNeighborsAbove == 2:
        if grid[y - 1][x].isdigit():
            numNumericNeighbors += 1
        else:
            numNumericNeighbors += 2

    # Since numbers are only written horizontally, we have an adjacent number if the cell to the left of the gear
    # is in the grid and contains a number
    if (y, x - 1) in validNeighbors and grid[y][x - 1].isdigit():
        numNumericNeighbors += 1

    # Since numbers are only written horizontally, we have an adjacent number if the cell to the right of the gear
    # is in the grid and contains a number
    if (y, x + 1) in validNeighbors and grid[y][x + 1].isdigit():
        numNumericNeighbors += 1

    # There are at most 3 neighbors below the gear (down, down-left, and down-right)
    # If only one of those neighbors is a number, we have exactly one adjacent number.
    # If all three are numbers, we have one long number (i.e. with at least 3 digits) adjacent below the gear
    if numNumericNeighborsBelow in [1, 3]:
        numNumericNeighbors += 1


    # If two of the neighboring cells below the gear are numbers, there's two possible situations we could be in:
    # - The two numbers are adjacent to each other and therefore make up one number adjacent to the gear
    # - There's a space between the end of one number and the start of the next, so there's two numbers adjacent to the gear
    elif numNumericNeighborsBelow == 2:
        if grid[y + 1][x].isdigit():
            numNumericNeighbors += 1
        else:
            numNumericNeighbors += 2

    # The gear is "valid" only if there are EXACTLY 2 adjacent numbers
    return numNumericNeighbors == 2

"""
This function finds the "gear ratio" for a given gear. This function
assumes that the gear passed in is "valid" (i.e. it is adjacent to EXACTLY
2 numbers in the given grid).

This function returns an integer that represents the product of the two
numbers in the grid that are adjacent to the given gear, i.e. the "gear ratio"
"""
def findGearRatio(locations: List[NumberLocation], gear: Gear) -> int:
    y, x = gear

    # Filter out any numbers that are located too far away from the current gear.
    # For numbers that are close enough, convert them to actual numbers so we can
    # calculate the gear ratio correctly
    gearNumbers = [int(n) for (n, i, j) in locations if i >= y - 1 and i < y + 2 and j < x + 2 and j + len(n) >= x]

    # Assume there are only two numbers adjacent to the gear. Multiply them together
    return gearNumbers[0] * gearNumbers[1]

"""
Main function
"""
if __name__ == "__main__":
    file: str = sys.argv[1]
    lines: List[str] = []

    # Read the input file
    with open(file, 'r') as f:
        lines = [l.strip() for l in f if len(l) > 0]

    # Find all numbers
    numberLocations: List[NumberLocation] = locateNumbers(lines)

    # Find all gears
    gears: List[Gear] = findGears(lines)

    # Find all gear ratios
    gearRatios = [findGearRatio(numberLocations, gear) for gear in gears]

    # Print the sum of all gear ratios
    print(sum(gearRatios))
