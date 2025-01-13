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

update_rows = 0
update_cols = 0
update_boxes = 0

# to remove the possibility of a number 5 from {1, ..., 9}: bin(numbers[0] & ~numbers[5])
def set_note(note, pos):
    if board[pos] == note and note != 0: return True
    board[pos] = note
    if note == 0:
        print("BRO IS ZERO") 
        return False
    global update_rows
    global update_cols
    global update_boxes
    h = pos % 9
    v = pos // 9
    b = (h // 3) + (v // 3) * 3
    update_rows |= 1 << v
    update_cols |= 1 << h
    update_boxes |= 1 << b
    if not is_single(note): return True
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
    if not is_single(note): print('🤨🤨🤨')
    return set_note(board[pos] & (~note), pos)

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
    for i in range(9):
        if not set_note(cell_notes[i], positions[i]):
            return False
    return True
        
def solve_row(row):
    return solve_9(tuple(row_positions(row)))

def solve_col(col):
    return solve_9(tuple(col_positions(col)))

def solve_box(box):
    return solve_9(tuple(box_positions(box)))

def update():
    global update_rows
    global update_cols
    global update_boxes
    while update_rows != 0 or update_cols != 0 or update_boxes != 0:
        for i in range(9):
            p = 1 << i
            if update_rows & p != 0:
                update_rows &= ~p
                if not solve_row(i):
                    return False
            if update_cols & p != 0:
                update_cols &= ~p
                if not solve_col(i):
                    return False
            if update_boxes & p != 0:
                update_boxes &= ~p
                if not solve_box(i):
                    return False

def solve_note(note, pos):
    return set_note(note, pos) and update()

def solve(pos = 0):
    global board
    while pos < 81 and is_single(board[pos]):
        pos += 1
    if pos == 81: return True
    while board[pos] != 0:
        single_note = get_first_single_note(board[pos])
        current_board = tuple(board)

        if pos == 9:
            print_numbers(board)
        setnoteresult = set_note(single_note, pos)
        if setnoteresult and solve(pos + 1):
            return True
        
        board = list(current_board)
        sub_single_note(single_note, pos)
    return False


def fill():
    for pos in range(81):
        number = start[pos]
        if number != 0:
            set_note(notes[number], pos)
    # update = True
    # while update:
    #     update = False
    #     for i in range(9):
    #         update = update or solve_row(i) or solve_col(i) or solve_box(i)
    update()

from time import time
tstart = time()

# board[36] = 0b000000011
# board[44] = 0b000000111
# set_single_note(notes[1], 40, board)
fill()
solve()
# set_note(notes[1], 4)
# print_board(board)
# print("STEP START!!!")
# set_note(notes[8], 9)
# print("STEP END!!!")
print_board(board)
print_numbers(board)
validate_board(board)

tend = time()
print(f'execution: {tend - tstart:.3f}s')

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