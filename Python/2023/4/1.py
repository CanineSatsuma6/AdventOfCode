import re
import sys

from math import floor
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
This function calculates the score of a game.

This function returns the score of the given game.
"""
def scoreGame(game: Game) -> int:
    _, winningNums, myNums = game

    # Build a list that contains all of the numbers that exist in both the winning number list
    # and my number list
    winners: List[int] = [n for n in winningNums if n in myNums]

    # The score of a game can be written as 2^(the number of matching winning numbers - 1).
    # In the case where there are no matching winners, we'll end up with 2^-1 (i.e. 0.5), so
    # take the floor of the result to ensure we get 0 in that case
    return floor(2 ** (len(winners) - 1))

"""
Main function
"""
if __name__ == "__main__":
    file: str = sys.argv[1]
    games: List[Game] = []

    # Read all of the games out of the puzzle input file
    with open(file, 'r') as f:
        games = [game for game in [parseInputLine(line.strip()) for line in f if len(line) > 0] if game is not None]

    # Calculate the score of each game
    gameScores: List[int] = [scoreGame(game) for game in games]

    # Add up all of the game scores and print the sum
    print(sum(gameScores))
