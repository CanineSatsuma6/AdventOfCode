import sys

def scoreGame(game):
    gameNum, winningNums, myNums = game

    winners = [n for n in winningNums if n in myNums]

    return int(2 ** (len(winners) - 1) // 1)

if __name__ == "__main__":
    file = sys.argv[1]

    games = []

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()

            gameNum = int(line.split(':')[0].replace('Card ', ''))

            winningNums = [int(n.strip()) for n in line.split(':')[1].split('|')[0].split()]
            myNums = [int(n.strip()) for n in line.split(':')[1].split('|')[1].split()]
            games.append((gameNum, winningNums, myNums))

    print(sum([scoreGame(game) for game in games]))