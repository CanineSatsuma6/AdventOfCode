import sys

def getDifferenceList(arrs):
    arr = arrs[-1]

    differences = []

    for i in range(len(arr) - 1):
        left, right = arr[i], arr[i + 1]
        differences.append(right - left)

    arrs.append(differences)

    if any(n != 0 for n in differences):
        getDifferenceList(arrs)

    return arrs

def buildBackward(arrs):
    for i in range(len(arrs) - 2, -1, -1):
        top = arrs[i]
        bottom = arrs[i + 1]

        top.append(top[-1] + bottom[-1])

    return arrs[0]

def parseInput():
    file = sys.argv[1]

    with open(file, 'r') as f:
        histories = [[int(n) for n in line.strip().split()] for line in f.readlines()]

    return histories

if __name__ == "__main__":
    histories = parseInput()

    lasts = [buildBackward(getDifferenceList([history]))[-1] for history in histories]

    print(sum(lasts))
