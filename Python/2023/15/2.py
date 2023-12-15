import sys

def parseInput():
    file: str = sys.argv[1]

    with open(file, 'r') as f:
        rawSteps = f.read().strip().split(',')

    steps = [(step.split('=')[0], '=', int(step.split('=')[1])) if '=' in step else (step.split('-')[0], '-') for step in rawSteps]

    return steps

def hash(string):
    curHash = 0

    for c in string:
        ascii = ord(c)
        curHash += ascii
        curHash *= 17
        curHash %= 256

    return curHash

def evaluateStep(boxes, step):
    if len(step) == 3:
        label, _, num = step

        labelHash = hash(label)

        box = boxes[labelHash]

        indices = [i for i, (l, _) in enumerate(box) if l == label]

        if len(indices) == 0:
            box.append((label, num))

        else:
            box[indices[0]] = (label, num)

    else:
        label, _ = step

        labelHash = hash(label)

        box = boxes[labelHash]

        indices = [i for i, (l, _) in enumerate(box) if l == label]

        if len(indices) == 1:
            box.pop(indices[0])

def getFocusingPower(boxes):
    power = 0

    for boxNum, box in boxes.items():
        for i, (_, focalLength) in enumerate(box):
            power += (boxNum + 1) * (i + 1) * (focalLength)

    return power

if __name__ == "__main__":
    boxes = {i: [] for i in range(256)}

    steps = parseInput()

    for step in steps:
        evaluateStep(boxes, step)

    print(getFocusingPower(boxes))
