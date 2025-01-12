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

# to remove the possibility of a number 5 from {1, ..., 9}: bin(numbers[0] & ~numbers[5])
def set_single_note(note, pos):
    h = pos % 9
    v = pos // 9
    row = pos - h
    for c in range(9):
        sub_single_note(note, row + c)
    col = pos - v * 9
    for c in range(9):
        sub_single_note(note, col + c * 9)
    box = pos - (h % 3) - (v % 3) * 9
    for c in range(9):
        sub_single_note(note, box + (c % 3) + (c // 3) * 9)
    board[pos] = note

def sub_single_note(note, pos):
    if is_single(board[pos]): return
    board[pos] &= ~note
    if is_single(board[pos]):
        set_single_note(board[pos], pos)

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
    single_updates = [None] * 9
    for i in range(9):
        pos = positions[i]
        note = cell_notes[i]
        if board[pos] != note:
            update = True
            if is_single(note): single_updates[i] = pos
        board[pos] = note
    for i in range(9):
        pos = single_updates[i]
        if pos != None:
            set_single_note(board[pos], pos)
    return update
        
def solve_row(row):
    return solve_9(tuple(i + row * 9 for i in range(9)))

def solve_col(col):
    return solve_9(tuple(col + i * 9 for i in range(9)))

def solve_box(box):
    bpos = (box % 3) * 3 + (box // 3) * 27
    return solve_9(tuple(bpos + i + o * 9 for i in range(3) for o in range(3)))

for pos in range(81):
    number = start[pos]
    if number != 0:
        set_single_note(notes[number], pos)

def solve():
    update = True
    while update:
        update = False
        for i in range(9):
            update = update or solve_row(i) or solve_col(i) or solve_box(i)

# board[36] = 0b000000011
# board[44] = 0b000000111
# set_single_note(notes[1], 40, board)
solve()
print_board(board)
print_numbers(board)
validate_board(board)