import sys

def parseInput():
    file = sys.argv[1]

    with open(file, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]

    return grid

def expandGrid(grid):

    expanded = [row[:] for row in grid]

    # expand rows first
    indicesToAddAt = []

    for i, row in enumerate(grid):
        if '#' not in row:
            indicesToAddAt.append(i)

    indicesToAddAt.sort(reverse=True)

    for i in indicesToAddAt:
        expanded.insert(i, ['.' for _ in grid[0]])

    # now do columns
    indicesToAddAt = set([i for i in range(len(grid[0]))])
    colsWithGalaxies = set([col for row in expanded for col, char in enumerate(row) if char == '#'])
    indicesToAddAt -= colsWithGalaxies

    indicesToAddAt = list(indicesToAddAt)

    indicesToAddAt.sort(reverse=True)

    print(indicesToAddAt)

    for row in expanded:
        for i in indicesToAddAt:
            row.insert(i, '.')

    return expanded

def findGalaxies(grid):
    return [(y, x) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == '#']

def findDistances(galaxies):
    dists = []

    for i in range(len(galaxies) - 1):
        for j in range(i + 1, len(galaxies)):
            g1y, g1x = galaxies[i]
            g2y, g2x = galaxies[j]
            dists.append(abs(g2y - g1y) + abs(g2x - g1x))

    return dists

if __name__ == "__main__":
    grid = parseInput()

    expanded = expandGrid(grid)

    galaxies = findGalaxies(expanded)

    distances = findDistances(galaxies)

    print(sum(distances))
