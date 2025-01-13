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

start = [0, 9, 0,  7, 0, 0,  8, 0, 0,
         0, 0, 7,  0, 5, 0,  3, 0, 0,
         5, 0, 4,  0, 0, 0,  0, 0, 0,

         0, 0, 0,  5, 0, 0,  0, 0, 4,
         6, 4, 0,  0, 9, 0,  0, 0, 2,
         0, 3, 0,  1, 0, 0,  0, 0, 6,

         0, 0, 0,  0, 0, 0,  0, 0, 0,
         0, 6, 0,  9, 0, 0,  1, 0, 0,
         0, 7, 0,  0, 0, 2,  0, 0, 3]

# start = [0, 7, 0,  0, 0, 5,  2, 9, 6,
#          0, 0, 0,  0, 0, 6,  0, 8, 1,
#          0, 0, 6,  8, 0, 0,  0, 0, 3,

#          0, 2, 0,  9, 0, 3,  0, 0, 0,
#          0, 8, 0,  2, 0, 0,  9, 1, 0,
#          0, 1, 0,  0, 0, 0,  0, 0, 0,

#          0, 0, 0,  0, 7, 0,  8, 6, 0,
#          5, 0, 0,  0, 0, 2,  0, 7, 0,
#          0, 6, 4,  5, 0, 0,  0, 2, 0]

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
        valid &= validate_9(i + row * 9 for i in range(9))
    for col in range(9):
        valid &= validate_9(col + i * 9 for i in range(9))
    for box in range(9):
        bpos = (box % 3) * 3 + (box // 3) * 27
        valid &= validate_9(bpos + (i % 3) + (i // 3) * 9 for i in range(9))
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

def row_positions(row):
    return (i + row * 9 for i in range(9))

def col_positions(col):
    return (col + i * 9 for i in range(9))

def box_positions(box):
    bpos = (box % 3) * 3 + (box // 3) * 27
    return (bpos + i + o * 9 for i in range(3) for o in range(3))

# to remove the possibility of a number 5 from {1, ..., 9}: bin(numbers[0] & ~numbers[5])
def set_note(note, pos):
    if board[pos] == note: return
    board[pos] = note
    if not is_single(note): return
    h = pos % 9
    v = pos // 9
    for c in row_positions(v):
        if c != pos: sub_single_note(note, c)
    for c in col_positions(h):
        if c != pos: sub_single_note(note, c)
    for c in box_positions((h // 3) + (v // 3) * 3):
        if c != pos: sub_single_note(note, c)

def sub_single_note(note, pos):
    if not is_single(note): print('🤨🤨🤨')
    set_note(board[pos] & (~note), pos)

def get_single_notes(note):
    single_note = 1
    for i in range(9):
        if single_note & note != 0:
            yield single_note
        single_note <<= 1

def solve_9(positions):
    cell_single_notes = tuple(tuple(get_single_notes(board[pos])) for pos in positions)
    cell_note_lengths = tuple(len(sn) for sn in cell_single_notes)
    cell_note_indexes = [0] * 9
    cell_notes = [0] * 9
    combs = [0] * 10
    while cell_note_indexes[0] < cell_note_lengths[0]:
        valid = True
        for i in range(9):
            note = cell_single_notes[i][cell_note_indexes[i]]
            if combs[i] & note > 0:
                valid = False
                break
            combs[i + 1] = combs[i] | note
        if valid:
            for i in range(9):
                cell_notes[i] |= cell_single_notes[i][cell_note_indexes[i]]
        for o in range(8, -1, -1):
            cell_note_indexes[o] += 1
            if cell_note_indexes[o] < cell_note_lengths[o] or o == 0: break
            cell_note_indexes[o] = 0
    update = False
    for i in range(9):
        pos = positions[i]
        note = cell_notes[i]
        if board[pos] != note:
            update = True
            set_note(note, pos)
    return update
        
def solve_row(row):
    return solve_9(tuple(i + row * 9 for i in range(9)))

def solve_col(col):
    return solve_9(tuple(col + i * 9 for i in range(9)))

def solve_box(box):
    bpos = (box % 3) * 3 + (box // 3) * 27
    return solve_9(tuple(bpos + i + o * 9 for o in range(3) for i in range(3)))

for pos in range(81):
    number = start[pos]
    if number != 0:
        set_note(notes[number], pos)

def solve():
    update = True
    while update:
        update = False
        for i in range(9):
            update = update or solve_row(i) or solve_col(i) or solve_box(i)

# board[36] = 0b000000011
# board[44] = 0b000000111
# set_single_note(notes[1], 40, board)
print_board(board)
print()
solve()
print_board(board)
print_numbers(board)
validate_board(board)

# 2nd example, best
# 000000100 100000000 000100000 001000000 000001011 000001001 010000000 000001010 000010000 
# 010000011 010000011 001000000 010101010 000010000 110101001 000000100 100101010 100000001 
# 000010000 010000011 000001000 010100110 010100111 110100101 000100010 101100010 101000001 
# 111000011 010000011 110000011 000010000 011100110 011100100 101000000 000000101 000001000 
# 000100000 000001000 010010001 010000100 100000000 011000100 001010000 000000101 000000010 
# 101000010 000000100 100010010 000000001 001001010 001001000 101010000 010000000 000100000 
# 110001011 000010000 110000111 010101100 011101101 011101101 000101010 101101010 111000000 
# 010001010 000100000 010000110 100000000 011001100 000010000 000000001 001001010 011000000 
# 110001001 001000000 110000001 010101000 010101001 000000010 000101000 000010000 000000100 