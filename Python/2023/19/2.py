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

def invertExpression(expression: str):
    if '>' in expression:
        expression = expression.replace('>', '<=')
    elif '<' in expression:
        expression = expression.replace('<', '>=')

    return expression

def getPaths(workflows: dict[str, list[tuple[str, str]]], start: str, condition: str) -> list[list[tuple[str, str]]]:
    workflow = workflows[start]

    paths = []

    curExpression = ''

    for expression, destination in workflow:
        if expression == 'True':
            expressionToUse = curExpression
        else:
            expressionToUse = curExpression + (' and ' if len(curExpression) > 0 else '') + expression

        match destination:
            case 'R':
                paths.append([(condition, start), (expressionToUse, 'R')])
            case 'A':
                paths.append([(condition, start), (expressionToUse, 'A')])
            case _:
                for path in getPaths(workflows, destination, expressionToUse):
                    paths.append([(condition, start)] + path)

        curExpression = curExpression + (' and ' if len(curExpression) > 0 else '') + (invertExpression(expression) if expression != 'True' else '')

    return paths

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

def filterBadPaths(paths: list[list[tuple[str, str]]]):
    filtered = []

    for path in paths:
        _, destination = path[-1]
        if destination == 'A':
            filtered.append(path)

    return filtered

def getCompoundConditions(filtered: list[list[tuple, str, str]]):
    return [' and '.join(expression for expression, _ in path[1:]) for path in filtered]

def groupConditionsByAttribute(compoundConditions: list[str]):
    groups = []

    for path in compoundConditions:
        parts = path.split(' and ')
        s = [expression for expression in parts if expression.startswith('s')]
        x = [expression for expression in parts if expression.startswith('x')]
        a = [expression for expression in parts if expression.startswith('a')]
        m = [expression for expression in parts if expression.startswith('m')]

        groups.append((' and '.join(s), ' and '.join(x), ' and '.join(a), ' and '.join(m)))

    return groups

def getNumSuccessful(groupedConditions: list[tuple[str, str, str, str]]):
    return [(
        getNumSuccessfulForOneAttribute(s, 's'),
        getNumSuccessfulForOneAttribute(x, 'x'),
        getNumSuccessfulForOneAttribute(a, 'a'),
        getNumSuccessfulForOneAttribute(m, 'm')
        ) for s, x, a, m in groupedConditions]

def getNumSuccessfulForOneAttribute(condition: str, var: str):
    condition = condition.replace(var, 'i')
    if var == 'a':
        condition = condition.replace('ind', 'and')
    if len(condition) > 0:
        return len([i for i in range(1, 4001) if eval(condition)])
    else:
        return 4000

def getNumCombinations(numSuccessful: list[tuple[int, int, int, int]]):
    return [s * x * a * m for s, x, a, m in numSuccessful]

if __name__ == "__main__":
    workflows, parts = parseInput()

    paths = getPaths(workflows, 'in', '')

    filtered = filterBadPaths(paths)

    compoundConditions = getCompoundConditions(filtered)

    groupedConditions = groupConditionsByAttribute(compoundConditions)

    numSuccessful = getNumSuccessful(groupedConditions)

    # for path in filtered:
    #     print(' → '.join(str(tup) for tup in path))

    # for group in groupedConditions:
    #     print(group)

    # for num in numSuccessful:
    #     print(num)

    numCombinations = getNumCombinations(numSuccessful)

    print(sum(numCombinations))

    # keeperRatings = [x + m + a + s for x, m, a, s in parts if evaluatePart(workflows, x, m, a, s)]

    # print(sum(keeperRatings))

    # for name, steps in workflows.items():
    #     print(name)
    #     for step in steps:
    #         print('\t' + str(step))

    # print()

    # for x, m, a, s in parts:
    #     print(x, m, a, s)
