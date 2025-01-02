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
# essentially, each digit of the permutation has its own specified base, and all of them are then combined

# the aim is to order the permutations of similar scenarios
# this allows saying '0th tic-tac-toe game' or '5398th tic-tac-toe game' - indexing of permutations
# this gives a general way of going through every single permutation

# there are 9 outcomes of the first turn, 8 outcomes of the second turn and so on before no free spaces is left
# assume the game doesn't end before all spaces are filled
outcome_numbers = [9, 8, 7, 6, 5, 4, 3, 2, 1]

# find the total number of permutations by multiplying together the outcome # of each independent event
def get_total_permutations(outcome_numbers):
    total_permutations = 1
    for number in outcome_numbers:
        total_permutations *= number
    return total_permutations

# find the weights of each permutation digit
# e.g., in binary they are [1, 2, 4, 8, 16, ...]
def get_outcome_weights(outcome_numbers):
    outcome_weights = [1] * len(outcome_numbers)
    for i in range(1, len(outcome_weights)):
        outcome_weights[i] = outcome_numbers[i - 1] * outcome_weights[i - 1]
    return outcome_weights

# weights allow to convert between the permutation and permutation index
# ... where:
# permutation       - of a form '123500110'_[987654321]
# permutation index – number between 0 and the total number of permutations (excl. it), referring to a specific one

def get_permutation(permutation_index, outcome_weights):
    permutation = [0] * len(outcome_weights)
    r = permutation_index
    for i in range(len(outcome_weights)):
        index = -1 - i
        outcome = r // outcome_weights[index]
        permutation[index] = outcome
        r -= outcome * outcome_weights[index]
    return permutation

def get_permutation_index(permutation, outcome_weights):
    index = 0
    for i in range(len(outcome_weights)):
        index += permutation[i] * outcome_weights[i]
    return index

# get_permutation_index(get_permutation(a, [1, 2, 4, 8]), [1, 2, 4, 8])) == a

total_permutations = get_total_permutations(outcome_numbers)
outcome_weights = get_outcome_weights(outcome_numbers)

print(f"Total number of ways to fill a tic-tac-toe board is {total_permutations}") # 362880 = 9!
print(f"Weights of each event are: {outcome_weights}") # 1, 1 * 8, 1 * 8 * 7, 1 * 8 * 7 * 6 ... 

print(f"972nd game of tic-tac-toe is: {get_permutation(972, outcome_weights)}")
# . . .  . . o  . . o  . . o  x . o  x o o  x o o  x o o  x o o
# . x .  . x .  . x .  o x .  o x .  o x .  o x x  o x x  o x x
# . . .  . . .  . x .  . x .  . x .  . x .  . x .  o x .  o x x
# ... which is, conveniently, a win for x on the last turn

# where else is this useful?

# consider representing a game state with a text string
# in the game we will have:
# - a lever on the map (0 - 1)
# - player's gold (0 - 255)
# - player's level (1 - 20)
# - number of items in inventory (0 - 3)
# ... instead of saving it with a string (i.e., "1255203"), or a contracted one with HEX (i.e., "1FF203"),
# ... it can be saved as an integer - the permutation # of the four properties

outn = [2, 256, 20, 4] #p's level is stored (0 - 19) and then converted to (1 - 20)
prms = get_total_permutations(outn) # 40960
outw = get_outcome_weights(outn)

print(get_permutation_index([1, 255, 19, 3], outw)) # this is one less than total permutations - highest values

# this compresses the previous number 0x1FF203 to 0x9FFF
# it is the most efficient way to store the game state!