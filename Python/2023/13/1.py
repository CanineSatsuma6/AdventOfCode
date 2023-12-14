import sys

def parseInput() -> list[list[str]]:
    file: str = sys.argv[1]

    with open(file, 'r') as f:
        raw = f.read()

    rawGrids = raw.split('\n\n')

    grids = [line.splitlines() for line in rawGrids]

    return grids

def findReflection(grid) -> tuple[int, bool]:
    # search rows first
    numBefore = 0
    isVertical = False
    found = False

    for i in range(len(grid) - 1):
        top = grid[i]
        bottom = grid[i + 1]

        # potential mirror, check others
        if top == bottom:
            isMirror = True

            # check others
            for j in range(1, len(grid)):
                if i - j < 0 or i + j + 1 >= len(grid):
                    break

                top = grid[i - j]
                bottom = grid[i + j + 1]

                if top != bottom:
                    isMirror = False
                    break

            if isMirror:
                numBefore = i + 1
                isVertical = False
                found = True
                break

    # then search columns
    if not found:
        for i in range(len(grid[0]) - 1):
            left = ''.join(line[i] for line in grid)
            right = ''.join(line[i + 1] for line in grid)

            # potential mirror, check others
            if left == right:
                isMirror = True

                # check others
                for j in range(len(grid[0])):
                    if i - j < 0 or i + j + 1 >= len(grid[0]):
                        break

                    left = ''.join(line[i - j] for line in grid)
                    right = ''.join(line[i + j + 1] for line in grid)

                    if left != right:
                        isMirror = False
                        break

                if isMirror:
                    numBefore = i + 1
                    isVertical = True
                    found = True
                    break

    assert(found)

    return (numBefore, isVertical)

def scoreGrid(grid):
    index, isVertical = findReflection(grid)
    return index * (1 if isVertical else 100)

if __name__ == "__main__":
    grids = parseInput()

    print(sum(scoreGrid(grid) for grid in grids))
