import sys
import re

def traverse(instructions, nodes, start, target):

    curInstructionIndex = 0
    curNode = start
    numSteps = 0

    while curNode != target:
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

if __name__ == "__main__":
    instructions, nodes = parseInput()

    print(traverse(instructions, nodes, 'AAA', 'ZZZ'))
