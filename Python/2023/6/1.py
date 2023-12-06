import sys

def getDistance(raceTime, timeHeld):
    speed = timeHeld
    timeRacing = raceTime - timeHeld
    return speed * timeRacing

def parseInput():
    file = sys.argv[1]

    times = []
    distances = []

    lines = []

    with open(file, 'r') as f:
        lines = f.readlines()
    
    lines = [l.strip() for l in lines]

    times = [int(n) for n in lines[0].split()[1:]]
    distances = [int(n) for n in lines[1].split()[1:]]

    return zip(times, distances)

if __name__ == "__main__":
    races = parseInput()

    numWays = 1

    for time, distance in races:
        numWays *= len([True for i in range(time) if getDistance(time, i) > distance])

    print(numWays)
