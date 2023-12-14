import sys

def parseInput() -> list[list[str]]:
    # file: str = sys.argv[1]
    file = r'C:\Users\crm11\source\repos\AdventOfCode\Python\2023\13\input.txt'

    with open(file, 'r') as f:
        raw = f.read()

    rawGrids = [grid.splitlines() for grid in raw.split('\n\n')]
    grids = [[list(line) for line in grid] for grid in rawGrids]

    return grids

def findReflection(grid, doPrint = False, origIndex = None, origIsVert = None) -> tuple[bool, int, bool]:
    # search rows first
    numBefore = 0
    isVertical = False
    found = False

    for i in range(len(grid) - 1):
        top = ''.join(grid[i])
        bottom = ''.join(grid[i + 1])

        # if (doPrint):
        #     print(top)
        #     print(bottom)
        #     print()

        # potential mirror, check others
        if top == bottom:
            isMirror = True

            # if doPrint:
            #     print('potential mirror')

            # check others
            for j in range(1, len(grid)):
                if i - j < 0 or i + j + 1 >= len(grid):
                    break

                top = ''.join(grid[i - j])
                bottom = ''.join(grid[i + j + 1])

                if top != bottom:
                    # if doPrint:
                    #     print('not a mirror')
                    isMirror = False
                    break

            if isMirror and ((i + 1, False) != (origIndex, origIsVert)):
                # if doPrint:
                #     print('confirmed mirror')
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

                if isMirror and ((i + 1, True) != (origIndex, origIsVert)):
                    numBefore = i + 1
                    isVertical = True
                    found = True
                    break

    return (found, numBefore, isVertical)

def scoreGrid(grid):
    _, origIndex, origVert = findReflection(grid)

    # print('\n'.join(''.join(line) for line in grid))
    # print("Original index:", origIndex)
    # print("Original vertical:", origVert, "\n")

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            grid[row][col] = '.' if grid[row][col] == '#' else '#'
            # if (row, col) == (11, 6):
            #     print('\n'.join(''.join(line) for line in grid) + '\n')
            found, index, isVertical = findReflection(grid, (row, col) == (2, 2), origIndex, origVert)


            if found and ((origIndex, origVert) != (index, isVertical)):
                break

            grid[row][col] = '.' if grid[row][col] == '#' else '#'

        if found and ((origIndex, origVert) != (index, isVertical)):
            break

    # print('\n'.join(''.join(line) for line in grid))
    # print("New index:", index)
    # print("New vertical:", isVertical, "\n")

    assert(found)

    return index * (1 if isVertical else 100)

if __name__ == "__main__":
    grids = parseInput()

    print(sum(scoreGrid(grid) for grid in grids))
