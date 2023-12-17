import sys

def parseInput():
    file: str = sys.argv[1]

    with open(file, 'r') as f:
        grid = [list(line.strip()) for line in f.readlines()]

    return grid

def shootBeam(grid, y, x, direction, energized):
    match direction:
        case 'r':
            for i in range(x + 1, len(grid[0])):
                cell = (y, i, direction)

                if cell in energized:
                    break

                energized.add(cell)

                match grid[y][i]:
                    case '/':
                        shootBeam(grid, y, i, 'u', energized)
                        break
                    case '\\':
                        shootBeam(grid, y, i, 'd', energized)
                        break
                    case '|':
                        shootBeam(grid, y, i, 'u', energized)
                        shootBeam(grid, y, i, 'd', energized)
                        break
                    case _:
                        continue
        case 'l':
            for i in range(x - 1, -1, -1):
                cell = (y, i, direction)

                if cell in energized:
                    break

                energized.add(cell)

                match grid[y][i]:
                    case '/':
                        shootBeam(grid, y, i, 'd', energized)
                        break
                    case '\\':
                        shootBeam(grid, y, i, 'u', energized)
                        break
                    case '|':
                        shootBeam(grid, y, i, 'd', energized)
                        shootBeam(grid, y, i, 'u', energized)
                        break
                    case _:
                        continue
        case 'u':
            for i in range(y - 1, -1, -1):
                cell = (i, x, direction)

                if cell in energized:
                    break

                energized.add(cell)

                match grid[i][x]:
                    case '/':
                        shootBeam(grid, i, x, 'r', energized)
                        break
                    case '\\':
                        shootBeam(grid, i, x, 'l', energized)
                        break
                    case '-':
                        shootBeam(grid, i, x, 'r', energized)
                        shootBeam(grid, i, x, 'l', energized)
                        break
                    case _:
                        continue
        case 'd':
            for i in range(y + 1, len(grid)):
                cell = (i, x, direction)

                if cell in energized:
                    break

                energized.add(cell)

                match grid[i][x]:
                    case '/':
                        shootBeam(grid, i, x, 'l', energized)
                        break
                    case '\\':
                        shootBeam(grid, i, x, 'r', energized)
                        break
                    case '-':
                        shootBeam(grid, i, x, 'l', energized)
                        shootBeam(grid, i, x, 'r', energized)
                        break
                    case _:
                        continue

def printEnergized(grid, energized):
    symbols = {(y, x): [] for y, x, _ in energized}

    lookup = {
        'r': '>',
        'l': '<',
        'u': '^',
        'd': 'v'
    }

    for y, x, d in energized:
        symbols[(y, x)].append(lookup[d])

    print()
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            if grid[y][x] != '.':
                print(grid[y][x], end='')
            elif (y, x) in symbols:
                if len(symbols[(y,x)]) == 1:
                    print(symbols[(y,x)][0], end='')
                elif len(symbols[(y,x)]) > 1:
                    print(len(symbols[(y,x)]), end='')
                else:
                    print('.', end='')
            else:
                print('.', end='')
        print()
    print()

if __name__ == "__main__":
    grid = parseInput()

    startY, startX, startDirection = 0, -1, 'r'

    energized = set()

    shootBeam(grid, startY, startX, startDirection, energized)

    cells = list(set([(y, x) for y, x, _ in energized]))

    print(len(cells))
