import sys

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

def scoreHand(hand):
    cards = [(c, hand.count(c)) for c in set(card for card in hand)]

    jCounts = [count for char, count in cards if char == 'J']

    jCount = 0 if len(jCounts) == 0 else jCounts[0]

    cards = [(char, count) for char, count in cards if char != 'J']

    # only jokers
    if len(cards) == 0:
        return FIVE_OF_A_KIND

    cards.sort(key=lambda c: c[1], reverse=True)

    char, count = cards[0]

    cards[0] = (char, count + jCount)

    # five of a kind
    if len(cards) == 1:
        return FIVE_OF_A_KIND

    # four of a kind
    # full house
    if len(cards) == 2:
        if max(count for _, count in cards) == 4:
            return FOUR_OF_A_KIND
        else:
            return FULL_HOUSE

    # three of a kind
    # two pair
    if len(cards) == 3:
        if max(count for _, count in cards) == 3:
            return THREE_OF_A_KIND
        else:
            return TWO_PAIR

    # one pair
    if len(cards) == 4:
        return ONE_PAIR

    # high card
    if len(cards) == 5:
        return HIGH_CARD

cardVals = {
    'J': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'Q': 10,
    'K': 11,
    'A': 13
}

def getSortKey(hand):

    key = 0

    for i in range(len(hand)):
        key |= cardVals[hand[len(hand) - 1 - i]] << (4 * i)

    return key

def parseInput():
    file = sys.argv[1]

    with open(file, 'r') as f:
        hands = [(hand, int(bid)) for hand, bid in [line.strip().split() for line in f]]

    return hands

if __name__ == "__main__":
    hands = parseInput()

    scores = [(scoreHand(hand), hand, bid) for hand, bid in hands]

    scores.sort(key=lambda item: (item[0], getSortKey(item[1])))

    winnings = [(i + 1) * tup[2] for i, tup in enumerate(scores)]

    print(sum(winnings))
