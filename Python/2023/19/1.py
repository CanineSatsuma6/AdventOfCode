import sys
import re

def parseInput() -> tuple[dict[str, list[tuple[str, str]]], list[tuple[int, int, int, int]]]:
    file: str = sys.argv[1]

    with open(file, 'r') as f:
        raw = f.read()

    rawWorkflows, rawParts = raw.split('\n\n')

    workflows, parts = {}, []

    for rawWorkflow in rawWorkflows.splitlines():
        name = rawWorkflow.split('{')[0]
        rawSteps = rawWorkflow.split('{')[1][:-1].split(',')
        steps = []
        for rawStep in rawSteps:
            if ':' in rawStep:
                expression, destination = rawStep.split(':')
            else:
                expression = 'True'
                destination = rawStep
            steps.append((expression, destination))
        workflows[name] = steps

    for rawPart in rawParts.splitlines():
        m = re.match(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", rawPart)
        parts.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))

    return workflows, parts

def evaluatePart(workflows: dict[str, list[tuple[str, str]]], x, m, a, s):

    curWorkflow = workflows['in']

    while True:
        for expression, destination in curWorkflow:
            if eval(expression):
                match destination:
                    case 'R':
                        return False
                    case 'A':
                        return True
                    case _:
                        curWorkflow = workflows[destination]
                        break

if __name__ == "__main__":
    workflows, parts = parseInput()

    keeperRatings = [x + m + a + s for x, m, a, s in parts if evaluatePart(workflows, x, m, a, s)]

    print(sum(keeperRatings))

    # for name, steps in workflows.items():
    #     print(name)
    #     for step in steps:
    #         print('\t' + str(step))

    # print()

    # for x, m, a, s in parts:
    #     print(x, m, a, s)
