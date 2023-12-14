import sys

from math import floor

def scoreMirrors(grid, mirrors):
    return [len(grid) - y for (y, x) in mirrors]

def rollIndividualMirrorNorth(grid, mirror) -> tuple[int, int]:
    y, x = mirror

    newY = y

    for i in range(y - 1, -1, -1):
        if grid[i][x] == '.':
            newY = i
        else:
            break

    grid[y][x] = '.'
    grid[newY][x] = 'O'

    return (newY, x)

def rollIndividualMirrorSouth(grid, mirror) -> tuple[int, int]:
    y, x = mirror

    newY = y

    for i in range(y + 1, len(grid)):
        if grid[i][x] == '.':
            newY = i
        else:
            break

    grid[y][x] = '.'
    grid[newY][x] = 'O'

    return (newY, x)

def rollIndividualMirrorWest(grid, mirror) -> tuple[int, int]:
    y, x = mirror

    newX = x

    for i in range(x - 1, -1, -1):
        if grid[y][i] == '.':
            newX = i
        else:
            break

    grid[y][x] = '.'
    grid[y][newX] = 'O'

    return (y, newX)

def rollIndividualMirrorEast(grid, mirror) -> tuple[int, int]:
    y, x = mirror

    newX = x

    for i in range(x + 1, len(grid[0])):
        if grid[y][i] == '.':
            newX = i
        else:
            break

    grid[y][x] = '.'
    grid[y][newX] = 'O'

    return (y, newX)

def rollNorth(grid, mirrors):
    mirrors.sort(key=lambda item: (item[0], item[1]))

    for i, mirror in enumerate(mirrors):
        mirrors[i] = rollIndividualMirrorNorth(grid, mirror)

def rollSouth(grid, mirrors):
    mirrors.sort(key=lambda item: (item[0], item[1]), reverse=True)

    for i, mirror in enumerate(mirrors):
        mirrors[i] = rollIndividualMirrorSouth(grid, mirror)

def rollWest(grid, mirrors):
    mirrors.sort(key=lambda item: (item[1], item[0]))

    for i, mirror in enumerate(mirrors):
        mirrors[i] = rollIndividualMirrorWest(grid, mirror)

def rollEast(grid, mirrors):
    mirrors.sort(key=lambda item: (item[1], item[0]), reverse=True)

    for i, mirror in enumerate(mirrors):
        mirrors[i] = rollIndividualMirrorEast(grid, mirror)

def cycle(grid, mirrors):
    rollNorth(grid, mirrors)
    rollWest(grid, mirrors)
    rollSouth(grid, mirrors)
    rollEast(grid, mirrors)

def findMirrors(grid) -> list[tuple[int, int]]:
    return sorted([(y, x) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == 'O'])

def parseInput() -> list[tuple[str, int]]:
    file: str = sys.argv[1]

    with open(file, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]

    return grid

def printGrid(grid):
    for line in grid:
        print(''.join(line))

def hashGrid(grid):
    return '\n'.join(''.join(line) for line in grid)

if __name__ == "__main__":
    MAX_CYCLE_NUM = 1000000000

    grid = parseInput()

    mirrors = findMirrors(grid)

    results = { }

    cycles = 0

    curHash = hashGrid(grid)

    while curHash not in results:
        results[curHash] = cycles

        cycle(grid, mirrors)
        cycles += 1
        curHash = hashGrid(grid)

    cycleLength = cycles - results[curHash]

    numCycles = floor((MAX_CYCLE_NUM - cycles) / cycleLength)

    cycleStop = cycles + (numCycles * cycleLength)

    newIndex = MAX_CYCLE_NUM - cycleStop + results[curHash]

    keys = list(results.keys())
    values = list(results.values())

    position = values.index(newIndex)
    key: str = keys[position]

    hashed = [list(line) for line in key.splitlines()]

    mirrors = findMirrors(hashed)

    scores = scoreMirrors(hashed, mirrors)

    print(sum(scores))
