import sys

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

def rollNorth(grid, mirrors):
    for i, mirror in enumerate(mirrors):
        mirrors[i] = rollIndividualMirrorNorth(grid, mirror)

    mirrors.sort()

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

if __name__ == "__main__":
    grid = parseInput()

    mirrors = findMirrors(grid)

    rollNorth(grid, mirrors)

    scores = scoreMirrors(grid, mirrors)

    print(sum(scores))
