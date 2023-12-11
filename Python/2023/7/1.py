import sys

# Constants for the "ranks" of individual hands. Higher number hands
# are more valuable
FIVE_OF_A_KIND:  int = 7
FOUR_OF_A_KIND:  int = 6
FULL_HOUSE:      int = 5
THREE_OF_A_KIND: int = 4
TWO_PAIR:        int = 3
ONE_PAIR:        int = 2
HIGH_CARD:       int = 1

# A lookup table for the value of an individual card
CARD_VALUES: dict[str, int] = {
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

"""
This function calculates which "rank" (i.e. "four of a kind", "full house", etc) a
hand receives. The result is calculated based on the number of unique cards in a hand
and how many times each unique card appears.

This function returns the "rank" of the provided hand
"""
def scoreHand(hand: str) -> int:
    # Create a list of tuples. Each tuple contains a unique card and the number of times
    # that card appears in the hand
    cards: list[tuple[str, int]] = [(c, hand.count(c)) for c in set(card for card in hand)]

    result: int = HIGH_CARD

    match len(cards):
        # five of a kind
        case 1:
            result = FIVE_OF_A_KIND

        # four of a kind
        # full house
        case 2:
            result = FOUR_OF_A_KIND if max(count for _, count in cards) == 4 else FULL_HOUSE

        # three of a kind
        # two pair
        case 3:
            result = THREE_OF_A_KIND if max(count for _, count in cards) == 3 else TWO_PAIR

        # one pair
        case 4:
            result = ONE_PAIR

        # high card
        case 5:
            result = HIGH_CARD

    return result

"""
When sorting a list of hands to calculate the rank of each hand compared to its opponents,
we first sort by the result of the hand (i.e. "full house", "two pair", etc.), then by the
custom tiebreaker rules from the puzzle description.

This function calculates a key that can be used with the "sort" function to sort hands based
on the tiebreaker rules. The key is a bitwise composition of the values of each card in the
hand, in the order the cards appear in the hand.

This function returns a bitwise composition of the values of all the cards in the hand
"""
def getSortKey(hand: str) -> int:
    # start with all bits cleared
    key: int = 0

    # For each card, get its value and place it in its respective 4 bits of the resultant key
    for i in range(len(hand)):
        key |= CARD_VALUES[hand[len(hand) - 1 - i]] << (4 * i)

    return key

"""
This function returns an object containing all of the information necessary to complete the
puzzle.

This function returns a list of tuples. Each tuple contains an individual hand and the bid
that was made for that hand
"""
def parseInput() -> list[tuple[str, int]]:
    file: str = sys.argv[1]

    hands: list[tuple[str, int]] = []

    with open(file, 'r') as f:
        hands = [(hand, int(bid)) for hand, bid in [line.strip().split() for line in f]]

    return hands

"""
Main function
"""
if __name__ == "__main__":
    # Get all of the hands and their bids
    hands: list[tuple[str, int]] = parseInput()

    # Calculate the score of each hand
    scores: list[tuple[int, str, int]] = [(scoreHand(hand), hand, bid) for hand, bid in hands]

    # Sort all of the hands. First, sort by the "rank", then by the key built up using the custom
    # tiebreaker rules
    scores.sort(key=lambda item: (item[0], getSortKey(item[1])))

    # Calculate the winnings for each hand
    winnings: list[int] = [(i + 1) * tup[2] for i, tup in enumerate(scores)]

    # Print out the total winnings
    print(sum(winnings))
