import sys

def parseInput():
    file: str = sys.argv[1]

    with open(file, 'r') as f:
        steps = f.read().strip().split(',')

    return steps

def hash(string):
    curHash = 0

    for c in string:
        ascii = ord(c)
        curHash += ascii
        curHash *= 17
        curHash %= 256

    return curHash

if __name__ == "__main__":
    steps = parseInput()

    print(sum(hash(s) for s in steps))
