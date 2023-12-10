import sys

from typing import List

def parseInput():
    file = sys.argv[1]

    with open(file, 'r') as f:
        grid: List[str] = [line.strip() for line in f.readlines()]

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

def evaluateDistances(loop):
    distances = [0 for _ in loop]

    for i in range(1, len(distances)):
        if (distances[i] != 0):
            break
        distances[i] = distances[i - 1] + 1
        distances[-i - 1] = distances[-i] + 1

    return distances


if __name__ == "__main__":
    grid, (y, x) = parseInput()

    loop = traverseLoop(grid, y, x)

    print(max(evaluateDistances(loop)))
