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
    '2': 0,
    '3': 1,
    '4': 2,
    '5': 3,
    '6': 4,
    '7': 5,
    '8': 6,
    '9': 7,
    'T': 8,
    'J': 9,
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
