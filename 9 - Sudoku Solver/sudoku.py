# consider the case when there are two cells with notes [3, 7], [3, 7] in a square
# you can't tell where exactly 3 or 7 will be, but it must be in one of those two cells
# so neither 3 nor 7 could appear in other cells in the square
# ... this information will solve the square further and eventually resolve the locations of 3 and 7
# ... but I don't know yet how to formalise this rule; it can also take many weird forms

# another example: [3, 4], [3, 7], [4, 7]
# 3, 4 and 7 must be in these three cells; no matter the possibilities outside

# it could be easier to consider the recursive one-at-the-time changes of the state

start = [0, 4, 5,  0, 2, 0,  0, 0, 0,
         0, 0, 0,  0, 0, 1,  0, 0, 5,
         0, 0, 0,  0, 8, 0,  3, 0, 0,

         2, 1, 0,  0, 0, 0,  0, 8, 0,
         0, 7, 0,  0, 0, 0,  0, 1, 0,
         0, 0, 0,  0, 0, 0,  6, 9, 3,

         0, 0, 1,  9, 0, 6,  0, 0, 0,
         6, 0, 0,  0, 0, 0,  0, 0, 0,
         9, 0, 0,  3, 0, 0,  0, 0, 8]

# board = [{i for i in range(1, 10)} for i in range(81)]
# for pos in range(81):
#     number = start[pos]
#     if number == 0: continue
#     board[pos] = {number}

# def solve_9(positions):
#     change = False
#     # not implemented
#     return change

# def solve_square(square):
#     sp = (square % 3) * 3 + (square // 3) * 3 * 9
#     positions = tuple(sp + i % 3 + (i // 3) * 9 for i in range(9))
#     return solve_9(positions)

# def solve_row(row):
#     rp = row * 9
#     positions = tuple(rp + i for i in range(9))
#     return solve_9(positions)

# def solve_column(column):
#     positions = tuple(column + i * 9 for i in range(9))
#     return solve_9(positions)

# changed = True
# while changed:
#     changed = False
#     for i in range(9):
#         changed = changed or solve_row(i) or solve_column(i) or solve_square(i)

# for i in range(9):
#     print(board[i * 9 : i * 9 + 9])

# .........

notes = [0]
notes.extend(1 << i for i in range(9))
notes[0] = sum(notes)
single_notes = frozenset(notes[i] for i in range(1, 10))

board = [notes[0] for i in range(81)]

def print_board(board):
    for row in range(9):
        for note in board[row * 9 : row * 9 + 9]:
            print(format(note, '09b'), end=" ")
        print()

def is_single(note):
    return note == (note & (-note))

# to remove the possibility of a number 5 from {1, ..., 9}: bin(numbers[0] & ~numbers[5])
def set_single_note(note, pos, board):
    h = pos % 9
    v = pos // 9
    row = pos - h
    for c in range(9):
        sub_single_note(note, row + c, board)
    col = pos - v * 9
    for c in range(9):
        sub_single_note(note, col + c * 9, board)
    box = pos - (h % 3) - (v % 3) * 9
    for c in range(9):
        sub_single_note(note, box + (c % 3) + (c // 3) * 9, board)
    board[pos] = note

def sub_single_note(note, pos, board):
    if is_single(board[pos]): return
    board[pos] &= ~note
    if is_single(board[pos]):
        set_single_note(board[pos], pos, board)

for pos in range(81):
    number = start[pos]
    if number != 0:
        set_single_note(notes[number], pos, board)

# board[36] = 0b000000011
# board[44] = 0b000000111
# set_single_note(notes[1], 40, board)
print_board(board)