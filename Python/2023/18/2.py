import sys

DIRS = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}

def parseInput():
    file: str = sys.argv[1]

    steps = []

    with open(file, 'r') as f:
        for line in f:
            color = line.strip().split()[2][2:-1]
            dir = DIRS[color[-1]]
            n = int(color[:-1], base=16)
            steps.append((dir, n))

    return steps

def getVertices(steps):
    vertices = [(0, 0)]

    x, y = 0, 0

    for dir, n in steps:
        match dir:
            case 'R':
                x += n
            case 'L':
                x -= n
            case 'U':
                y -= n
            case 'D':
                y += n

        vertices.append((x, y))

    # The shoelace algorithm requires coordinates to be positive
    minX = min(x for x, _ in vertices)
    minY = min(y for _, y in vertices)

    xToAdd = -minX if minX < 0 else 0
    yToAdd = -minY if minY < 0 else 0

    if xToAdd > 0 or yToAdd > 0:
        vertices = [(x + xToAdd, y + yToAdd) for x, y in vertices]

    return vertices

def getArea(vertices):

    area = 0

    for i in range(len(vertices) - 1):
        x1, y1 = vertices[i]
        x2, y2 = vertices[i + 1]

        area += (x1 * y2) - (x2 * y1)

        # our lines have widths, so add the length of each segment to the total area
        area += abs(x2 - x1) + abs(y2 - y1)

    return 1 + (area // 2)

if __name__ == "__main__":
    steps = parseInput()
    vertices = getVertices(steps)

    print(getArea(vertices))
