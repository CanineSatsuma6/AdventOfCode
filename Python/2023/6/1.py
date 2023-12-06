import sys

from math import floor, ceil
from typing import Iterator, Tuple, List

# Type definitions
Race = Tuple[int, int]

"""
This function calculates the number of options available
that will allow me to win the race if I hold down the button
according to the rules.

Results are found by solving the inequality:

raceTime * timeHeld - timeHeld^2 > distance

Roots are found using the "complete the square" method, to make the
math slightly nicer. Then, any integer between the roots (exclusive)
is taken into account

This function returns the number of discrete millisecond increments
I can hold the button for and still win the race
"""
def getNumWinningTimes(time: int, distance: int) -> int:
    # Calculate constants for "completing the square". Overall formula is:
    #
    # -timeHeld^2 + raceTime * heldTime = distance
    #
    # OR
    #
    # timeHeld = (raceTime / 2) +- sqrt((raceTime / 2)^2 - distance)
    halfTime: float = time / 2.0
    root: float = ((halfTime) ** 2 - distance) ** 0.5

    # Calculate roots of the inequality
    leftRoot: float = halfTime - root
    rightRoot: float = halfTime + root

    # The value we want to use is the next root inside the parabola (right of the left root,
    # or left of the right root). If the roots are integers, we still want to slide inward
    minHoldTime: int = int(leftRoot  + 1) if leftRoot.is_integer()  else ceil(leftRoot)
    maxHoldTime: int = int(rightRoot - 1) if rightRoot.is_integer() else floor(rightRoot)

    # Find the difference
    return maxHoldTime - minHoldTime + 1

"""
This function parses the input text file and returns the information
necessary to complete the problem.

This function returns a "zip" object. Iterating over this zip object
will give a tuple that contains the time and distance for a single race
"""
def parseInput() -> Iterator[Race]:
    file: str = sys.argv[1]

    times: List[int] = []
    distances: List[int] = []
    lines: List[str] = []

    # Read all the input lines, trim whitespace
    with open(file, 'r') as f:
        lines = [l.strip() for l in f.readlines()]

    # Parse out times and distances
    times = [int(n) for n in lines[0].split()[1:]]
    distances = [int(n) for n in lines[1].split()[1:]]

    # Combine the times and distances for each respective race
    return zip(times, distances)

"""
Main function
"""
if __name__ == "__main__":
    # Get input
    races: Iterator[Race] = parseInput()

    numWays: int = 1

    # Iterate over all races, get the number of ways to win,
    # and multiply it by the numbers of ways to win the other
    # races
    for time, distance in races:
        numWays *= getNumWinningTimes(time, distance)

    print(numWays)
