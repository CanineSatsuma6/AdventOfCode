import sys
import re
import math
from functools import reduce

def traverse(instructions, nodes, start):

    curInstructionIndex = 0
    curNode = start
    numSteps = 0

    while not curNode.endswith('Z'):
        instruction = instructions[curInstructionIndex]
        left, right = nodes[curNode]
        curNode = left if instruction == 'L' else right
        curInstructionIndex = (curInstructionIndex + 1) % len(instructions)
        numSteps += 1

    return numSteps

def parseInput():
    file = sys.argv[1]

    with open(file, 'r') as f:
        raw = f.read()

    instructions, nodeList = raw.split('\n\n')

    instructions = instructions.strip()

    nodes = {}

    for line in nodeList.splitlines():
        match = re.search(r'(\w{3}) = \((\w{3}), (\w{3})\)', line)

        nodes[match.group(1)] = (match.group(2), match.group(3))

    return instructions, nodes

def lcm(arr):
    return reduce(lambda x, y: (x * y) // math.gcd(x, y), arr)

if __name__ == "__main__":
    instructions, nodes = parseInput()

    starts = [node for node in nodes if node.endswith('A')]

    shortestPaths = [traverse(instructions, nodes, start) for start in starts]

    print(lcm(shortestPaths))
