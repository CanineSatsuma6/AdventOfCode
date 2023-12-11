import sys

EMPTY_COL_CONVERSION_NUM = 1000000

def parseInput():
    file = sys.argv[1]

    with open(file, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]

    return grid

def findExpansionPoints(grid):

    # find row expansion points first
    rowsToExpand = []

    for i, row in enumerate(grid):
        if '#' not in row:
            rowsToExpand.append(i)

    rowsToExpand.sort()

    # now do columns
    columnsToExpand = set([i for i in range(len(grid[0]))])
    colsWithGalaxies = set([col for row in grid for col, char in enumerate(row) if char == '#'])
    columnsToExpand -= colsWithGalaxies

    columnsToExpand = list(columnsToExpand)

    columnsToExpand.sort()

    return (rowsToExpand, columnsToExpand)

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

def expandGalaxies(rows, columns, galaxies):
    for i, (y, x) in enumerate(galaxies):
        numExpandingRowsBeforeCurGalaxy = len([True for row in rows if row < y])
        numExpandingColsBeforeCurGalaxy = len([True for col in columns if col < x])

        galaxies[i] = (y + ((EMPTY_COL_CONVERSION_NUM - 1) * numExpandingRowsBeforeCurGalaxy), x + ((EMPTY_COL_CONVERSION_NUM - 1) * numExpandingColsBeforeCurGalaxy))


if __name__ == "__main__":
    grid = parseInput()

    rows, columns = findExpansionPoints(grid)
    galaxies = findGalaxies(grid)

    expandGalaxies(rows, columns, galaxies)

    distances = findDistances(galaxies)

    print(sum(distances))
