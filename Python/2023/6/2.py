import sys

def getDistance(raceTime, timeHeld):
    speed = timeHeld
    timeRacing = raceTime - timeHeld
    return speed * timeRacing

def parseInput():
    file = sys.argv[1]

    lines = []

    with open(file, 'r') as f:
        lines = f.readlines()
    
    lines = [l.strip() for l in lines]

    time = int(''.join([n for n in lines[0].split()[1:]]))
    distance = int(''.join([n for n in lines[1].split()[1:]]))

    return (time, distance)

if __name__ == "__main__":
    time, distance = parseInput()

    minTimeToBeat = 0
    maxTimeToBeat = 0

    for i in range(time):
        if getDistance(time, i) > distance:
            minTimeToBeat = i
            break

    for i in range(time, 0, -1):
        if getDistance(time, i) > distance:
            maxTimeToBeat = i
            break

    print(maxTimeToBeat - minTimeToBeat + 1)
