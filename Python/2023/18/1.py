import sys

def parseInput():
    file: str = sys.argv[1]

    with open(file, 'r') as f:
        steps = [(line.split()[0], int(line.split()[1]), line.split()[2][2:-1]) for line in f.readlines()]

    return steps

def getPoints(steps):
    points = {(0, 0)}

    curX, curY = 0, 0

    for dir, n, _ in steps:
        match dir:
            case 'R':
                for _ in range(1, n + 1):
                    curX += 1
                    points.add((curX, curY))
            case 'L':
                for _ in range(1, n + 1):
                    curX -= 1
                    points.add((curX, curY))
            case 'U':
                for _ in range(1, n + 1):
                    curY -= 1
                    points.add((curX, curY))
            case 'D':
                for _ in range(1, n + 1):
                    curY += 1
                    points.add((curX, curY))

    return points

def printGrid(points, minX, maxX, minY, maxY):
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            print('#' if (x, y) in points else '.', end='')
        print()

def findFirstInsideCell(points, minX):
    leftEdgePoints = [(x, y) for x, y in points if x == minX and (x + 1, y) not in points]
    x, y = leftEdgePoints[0]
    return (x + 1, y)

def floodFill(points, start):
    q = [start]
    flooded = set()

    while len(q) > 0:
        x, y = q.pop(0)

        flooded.add((x, y))

        for neighbor in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if neighbor not in points and neighbor not in flooded and neighbor not in q:
                q.append(neighbor)

    points.update(flooded)

if __name__ == "__main__":
    steps = parseInput()

    points = getPoints(steps)

    minX = min(x for x, _ in points)
    maxX = max(x for x, _ in points)
    minY = min(y for _, y in points)
    maxY = max(y for _, y in points)

    inside = findFirstInsideCell(points, minX)

    floodFill(points, inside)

    print(len(points))
