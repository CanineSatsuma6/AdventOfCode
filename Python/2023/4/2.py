import re
import sys

from re import Match
from typing import List, Tuple

# Type definitions

# Contains   game number, winning numbers, my numbers
Game = Tuple[int, List[int], List[int]] 

"""
This function parses a single line from the puzzle input file and parses out the necessary
information. The information needed is:
- The Game ID
- The list of winning numbers
- The list of my numbers

This function returns EITHER:
- None, if the necessary information can't be parse from the line
- A "Game" object, which is a tuple containing all of the necessary information from above
"""
def parseInputLine(line: str) -> Game:
    # Game strings should be in a very specific format. Parse out the different sections
    # using regular expressions
    match: Match[str] = re.search(r'Card\s+(\d+):\s+([^\|]+)\s+\|\s+(.*)\s*', line)
    result: Game = None

    # If the input line is in the correct format, pull out the different parts into
    # their own variables
    if match is not None:
        gameId = int(match.group(1))
        winningNumbers = [int(n) for n in match.group(2).split()]
        myNumbers = [int(n) for n in match.group(3).split()]

        # Create the "Game" object
        result = (gameId, winningNumbers, myNumbers)

    return result

"""
This function calculates how many future cards need to be duplicated, then duplicates them.
This is monitored by the "results" variable, which contains the total counts for each scratch card game ID

This function updates the "results" variable passed to it. It does not return any value
"""
def duplicateGameWinners(game: Game, results: List[int]) -> None:
    gameNum, winningNumbers, myNumbers = game

    # Build a list that contains all of the numbers that exist in both the winning number list
    # and my number list
    winners = [n for n in winningNumbers if n in myNumbers]

    # Iterate through every scratch card ID that needs to be duplicated
    for i in range(gameNum, gameNum + len(winners)):

        # The current card is duplicated once for every instance of the current card. For example
        # if there are 2 instances of card 1 and card 1 needs to duplicate card 2, we'll end up with
        # 3 instances of card 2:
        # - 1 original card 2
        # - 2 duplicates of card 2
        #
        # In practice, this means that we need to add the count of the current card to the count
        # of the corresponding winner.
        #
        # The results list is 0-indexed, but the game IDs are 1-indexed. We account for this discrepancy
        # on the cards that need to be duplicated in the for loop above, but we need to subtract 1 on the
        # current card's game ID to account for this
        results[i] += results[gameNum - 1]

"""
Main function
"""
if __name__ == "__main__":
    file: str = sys.argv[1]
    games: List[Game] = []

    # Read all of the games out of the puzzle input file
    with open(file, 'r') as f:
        games = [game for game in [parseInputLine(line.strip()) for line in f if len(line) > 0] if game is not None]

    # Keep a list of numbers of scratch cards. Each index in the list represents a single scratch card ID. The value at
    # that list index is the number of scratch cards of that index.
    #
    # For example, a list with a value of [1, 2, 4] means there is 1 game 1 scrach card, 2 game 2 scratch cards, and 4 game 3 scratch cards
    results = [1 for _ in games]

    # Iterate through all games and duplicate the winning cards as per the rules
    for game in games:
        duplicateGameWinners(game, results)

    # Since results is a list of numbers where each number is the count of a unique scratch card number, we just
    # need to add up all the elements in results to get the total number of scratch cards
    print(sum(results))
