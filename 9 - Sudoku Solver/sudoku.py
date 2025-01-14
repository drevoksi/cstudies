# taking it further: 
# - minimise recursion depth
# - generalise for n-sized sudoku, not just size 3

# consider the case when there are two cells with notes [3, 7], [3, 7] in a square
# you can't tell where exactly 3 or 7 will be, but it must be in one of those two cells
# so neither 3 nor 7 could appear in other cells in the square
# ... this information will solve the square further and eventually resolve the locations of 3 and 7
# ... but I don't know yet how to formalise this rule; it can also take many weird forms

# another example: [3, 4], [3, 7], [4, 7]
# 3, 4 and 7 must be in these three cells; no matter the possibilities outside

# it could be easier to consider the recursive one-at-the-time changes of the state

# edit with insert-mode extension (VSCode)
# start = [0, 0, 0,  0, 0, 0,  0, 0, 0,
#          0, 0, 0,  0, 0, 0,  0, 0, 0,
#          0, 0, 0,  0, 0, 0,  0, 0, 0,

#          0, 0, 0,  0, 0, 0,  0, 0, 0,
#          0, 0, 0,  0, 0, 0,  0, 0, 0,
#          0, 0, 0,  0, 0, 0,  0, 0, 0,

#          0, 0, 0,  0, 0, 0,  0, 0, 0,
#          0, 0, 0,  0, 0, 0,  0, 0, 0,
#          0, 0, 0,  0, 0, 0,  0, 0, 0]

# start = [0, 4, 5,  0, 2, 0,  0, 0, 0,
#          0, 0, 0,  0, 0, 1,  0, 0, 5,
#          0, 0, 0,  0, 8, 0,  3, 0, 0,

#          2, 1, 0,  0, 0, 0,  0, 8, 0,
#          0, 7, 0,  0, 0, 0,  0, 1, 0,
#          0, 0, 0,  0, 0, 0,  6, 9, 3,

#          0, 0, 1,  9, 0, 6,  0, 0, 0,
#          6, 0, 0,  0, 0, 0,  0, 0, 0,
#          9, 0, 0,  3, 0, 0,  0, 0, 8]

# start = [0, 9, 0,  7, 0, 0,  8, 0, 0,
#          0, 0, 7,  0, 5, 0,  3, 0, 0,
#          5, 0, 4,  0, 0, 0,  0, 0, 0,

#          0, 0, 0,  5, 0, 0,  0, 0, 4,
#          6, 4, 0,  0, 9, 0,  0, 0, 2,
#          0, 3, 0,  1, 0, 0,  0, 0, 6,

#          0, 0, 0,  0, 0, 0,  0, 0, 0,
#          0, 6, 0,  9, 0, 0,  1, 0, 0,
#          0, 7, 0,  0, 0, 2,  0, 0, 3]

# start = [0, 7, 0,  0, 0, 5,  2, 9, 6,
#          0, 0, 0,  0, 0, 6,  0, 8, 1,
#          0, 0, 6,  8, 0, 0,  0, 0, 3,

#          0, 2, 0,  9, 0, 3,  0, 0, 0,
#          0, 8, 0,  2, 0, 0,  9, 1, 0,
#          0, 1, 0,  0, 0, 0,  0, 0, 0,

#          0, 0, 0,  0, 7, 0,  8, 6, 0,
#          5, 0, 0,  0, 0, 2,  0, 7, 0,
#          0, 6, 4,  5, 0, 0,  0, 2, 0]

start = [2, 0, 0,  0, 0, 0,  0, 0, 7,
         0, 0, 3,  7, 4, 0,  0, 0, 1,
         9, 0, 0,  8, 0, 0,  0, 0, 4,

         0, 0, 0,  0, 2, 7,  0, 0, 0,
         0, 0, 2,  0, 0, 6,  8, 0, 0,
         6, 0, 0,  3, 0, 4,  5, 0, 0,

         0, 0, 0,  0, 0, 0,  0, 0, 0,
         0, 1, 0,  6, 0, 0,  0, 0, 8,
         3, 0, 0,  4, 0, 0,  9, 0, 0]

notes = [0]
notes.extend(1 << i for i in range(9))
notes[0] = sum(notes)
numbers = {1 << i : (i + 1) for i in range(9)}

board = [notes[0] for i in range(81)]

def print_board(board):
    for row in range(9):
        for note in board[row * 9 : row * 9 + 9]:
            print(format(note, '09b'), end=" ")
        print()

def print_numbers(board):
    for row in range(9):
        for col in range(9):
            note = board[col + row * 9]
            print(str(numbers.get(note, '*')) + (' ' if col % 3 == 2 else ''), end='')
        print()
        if row % 3 == 2: print()

def validate_board(board):
    valid = True
    for row in range(9):
        valid &= validate_9(row_positions(row))
    for col in range(9):
        valid &= validate_9(col_positions(col))
    for box in range(9):
        valid &= validate_9(box_positions(box))
    print("VALID" if valid else "NOT VALID")

def validate_9(positions):
    comb = 0
    for pos in positions:
        note = board[pos]
        if comb & note > 0: return False
        comb |= note
    return True

def is_single(note):
    return note == (note & (-note))

def get_single_notes(note):
    single_note = 1
    for i in range(9):
        if single_note & note != 0:
            yield single_note
        single_note <<= 1

def get_first_single_note(note):
    single_note = 1
    for i in range(9):
        if single_note & note != 0:
            return single_note
        single_note <<= 1
    return 0

def row_positions(row):
    return (i + row * 9 for i in range(9))

def col_positions(col):
    return (col + i * 9 for i in range(9))

def box_positions(box):
    bpos = (box % 3) * 3 + (box // 3) * 27
    return (bpos + i + o * 9 for i in range(3) for o in range(3))

# to remove the possibility of a number 5 from {1, ..., 9}: bin(numbers[0] & ~numbers[5])
def set_note(note, pos):
    if board[pos] == note and note != 0: return True
    board[pos] = note
    if note == 0:
        return False
    if not is_single(note): return True
    h = pos % 9
    v = pos // 9
    b = (h // 3) + (v // 3) * 3
    for c in row_positions(v):
        if c != pos and not sub_single_note(note, c):
            return False
    for c in col_positions(h):
        if c != pos and not sub_single_note(note, c):
            return False
    for c in box_positions(b):
        if c != pos and not sub_single_note(note, c):
            return False
    return True

def sub_single_note(note, pos):
    return set_note(board[pos] & (~note), pos)

def solve(pos = 0):
    global board
    while pos < 81 and is_single(board[pos]):
        pos += 1
    if pos == 81: return True
    while board[pos] != 0:
        single_note = get_first_single_note(board[pos])
        current_board = tuple(board)

        if set_note(single_note, pos) and solve(pos + 1):
            return True
        
        board = list(current_board)
        if not sub_single_note(single_note, pos):
            return False
    return False

def fill():
    for pos in range(81):
        number = start[pos]
        if number != 0:
            set_note(notes[number], pos)

from time import time
tstart = time()

# board[36] = 0b000000011
# board[44] = 0b000000111
# set_single_note(notes[1], 40, board)
fill()
solve()
print_board(board)
print_numbers(board)
validate_board(board)

tend = time()
print(f'execution: {tend - tstart:.3f}s')