# let each event have some number of possible outcomes
# e.g., if a regular coin is flipped multiple times, there are just two outcomes for each flip, and they are independent
# in that case each possible scenario can be represented with binary
# that is, '1011' will represent 'head, tail, head, head'
# it is easy to calculate the total number of possible scenarios and nth permutation, by converting n to binary
# same with rolls of dice - each scenario of multiple rolls can be represented by a number in base-6 (senary)
# this works because the # of outcomes of each independent event is the same

# try representing a tic-tac-toe game in a similar manner
# moves are not independent, but there is exactly one less choice (free cell) left each consequent turn
# so if the moves are ordered by their index from the top-left corner of the board, they can be seen as independent
# a game can then be reproduced from such list of move indexes – a number with variable base
# e.g., '0000000' represents the following game, with each turn occupying the first available square:

# x . .  x o .  x o x  x o x  x o x  x o x  x o x
# . . .  . . .  . . .  o . .  o x .  o x o  o x o
# . . .  . . .  . . .  . . .  . . .  . . .  x . .

# ... but going forward we'll be looking at each possible way of achieving any full board, rather than a legal game
# (since the games must stop after the victory)

# thus, the outcome number set is [9, 8, 7, 6, 5, 4, 3, 2, 1]
# and each game is represented as a number like '012343210'_[987654321], where the subscript describes the variable base
# essentially, each digit of the permutation # has its own specified base, and all of them are then combined

# the aim is to order the permutations of similar scenarios
# this allows saying '0th tic-tac-toe game' or '5398th tic-tac-toe game' - indexing of permutations
# this gives a general way of going through every single permutation

outcome_numbers = [9, 8, 7, 6, 5, 4, 3, 2, 1]

# find the total number of permutations by multiplying together the outcome # of each independent event
total_permutations = 1
for number in outcome_numbers:
    total_permutations *= number

# find the weights of each permutation # digit
# e.g., in binary they are [1, 2, 4, 8, 16, ...]
weights = [1] * len(outcome_numbers)
for i in range(1, len(weights)):
    weights[i] = outcome_numbers[i] * weights[i - 1]

# weights allow to convert between the permutation number and index
# ... where:
# permutation number - of a form '123500110'_[987654321]
# permutation index  – number between 0 and the total number of permutations, referring to a specific one