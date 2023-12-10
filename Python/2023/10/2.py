import sys
import re

def parseInput():
    file = sys.argv[1]

    with open(file, 'r') as f:
        grid = [line.strip() for line in f.readlines()]

    y = [i for i, line in enumerate(grid) if 'S' in line][0]
    x = grid[y].index('S')

    return grid, (y, x)

def traverseLoop(grid, y, x):
    # find the two that are connected
    if y - 1 >= 0 and grid[y - 1][x] in ['|', '7', 'F']:
        curY, curX = (y - 1, x)
    elif y + 1 < len(grid) and grid[y + 1][x] in ['|', 'J', 'L']:
        curY, curX = (y + 1, x)
    elif x - 1 >= 0 and grid[y][x - 1] in ['-', 'F', 'L']:
        curY, curX = (y, x - 1)
    elif x + 1 < len(grid[0]) and grid[y][x + 1] in ['-', '7', 'J']:
        curY, curX = (y, x + 1)

    loop = [(y, x), (curY, curX)]

    lastY, lastX = y, x

    while (curY, curX) != (y, x):
        nextY, nextX = traverseOneStep(grid, curX, curY, lastX, lastY)
        lastY, lastX, curY, curX = curY, curX, nextY, nextX
        loop.append((curY, curX))

    return loop


def traverseOneStep(grid, x, y, prevX, prevY):
    # Moving right
    if (prevX, prevY) == (x - 1, y):
        if grid[y][x] == '-':
            return (y, x + 1)
        elif grid[y][x] == '7':
            return (y + 1, x)
        else:
            return (y - 1, x)

    # Moving left
    elif (prevX, prevY) == (x + 1, y):
        if grid[y][x] == '-':
            return (y, x - 1)
        elif grid[y][x] == 'L':
            return (y - 1, x)
        else:
            return (y + 1, x)

    # Moving down
    elif (prevX, prevY) == (x, y - 1):
        if grid[y][x] == '|':
            return (y + 1, x)
        elif grid[y][x] == 'J':
            return (y, x - 1)
        else:
            return (y, x + 1)

    # Moving up
    elif (prevX, prevY) == (x, y + 1):
        if grid[y][x] == '|':
            return (y - 1, x)
        elif grid[y][x] == '7':
            return (y, x - 1)
        else:
            return (y, x + 1)

    assert(False)

def clearGrid(grid, loop):

    # Make loop a set so it's faster to search for elements in for large loops
    loop = set(loop)

    cleared = [list(row[:]) for row in grid]

    for i, row in enumerate(cleared):
        for j, _ in enumerate(row):
            if (i, j) not in loop:
                cleared[i][j] = '.'

    return [''.join(l for l in row) for row in cleared]

def squashLine(line):
    line = re.sub(r'(?:F\-*7)|(?:L\-*J)', '', line)
    line = re.sub(r'(?:F\-*J)|(?:L\-*7)', '|', line)
    return line

def squashGrid(grid):
    return [squashLine(line) for line in grid]

def replaceStartToken(grid, y, loop):
    nextY, nextX = loop[1]
    prevY, prevX = loop[-2]

    token = "S"

    # in a vertical line
    if nextY == prevY:
        token = '|'
    # horizontal line
    elif nextX == prevX:
        token = '-'

    # Moving around a corner
    elif (prevX < nextX and prevY < nextY) or (nextX < prevX and nextY < prevY):
        token = '7'
    elif (prevX > nextX and prevY < nextY) or (nextX > prevX and nextY < prevY):
        token = 'F'
    elif (prevX < nextX and prevY > nextY) or (nextX < prevX and nextY > prevY):
        token = 'J'
    elif (prevX > nextX and prevY > nextY) or (nextX > prevX and nextY > prevY):
        token = 'L'

    grid[y] = grid[y].replace('S', token)

def countInteriorCells(grid):
    numInterior = 0

    for row in grid:
        inside = False
        for char in row:
            if char == '|':
                inside = not inside
            elif inside:
                numInterior += 1

    return numInterior

if __name__ == "__main__":
    grid, (y, x) = parseInput()

    loop = traverseLoop(grid, y, x)

    cleared = clearGrid(grid, loop)

    replaceStartToken(cleared, y, loop)

    squashed = squashGrid(cleared)

    print(countInteriorCells(squashed))
