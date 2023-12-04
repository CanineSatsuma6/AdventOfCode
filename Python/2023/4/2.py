import sys

def getNumCards(game):
    gameNum, winningNumbers, myNumbers = game
    winners = [n for n in winningNumbers if n in myNumbers]

    for i in range(gameNum + 1, gameNum + 1 + len(winners)):
        results[i - 1] += results[gameNum - 1]

if __name__ == "__main__":
#    file = r'C:\Users\crm11\source\repos\AdventOfCode\Python\2023\4\example.txt'
    file = sys.argv[1]

    games = []

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()

            gameNum = int(line.split(':')[0].replace('Card ', ''))

            winningNums = [int(n.strip()) for n in line.split(':')[1].split('|')[0].split()]
            myNums = [int(n.strip()) for n in line.split(':')[1].split('|')[1].split()]
            games.append((gameNum, winningNums, myNums))

    results = [1 for _ in games]

    for game in games:
        getNumCards(game)

    print(sum(results))
