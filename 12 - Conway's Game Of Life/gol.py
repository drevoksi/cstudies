w = 30
h = 15

def get_board(val):
    return [[val for y in range(h)] for x in range(w)]
def print_board(board):
    for y in range(len(board[0])):
        for x in range(len(board)):
            print('██' if board[x][y] else '  ', end="")
        print()

board = get_board(False)

# A live cell dies if it has fewer than two live neighbors.
# A live cell with two or three live neighbors lives on to the next generation.
# A live cell with more than three live neighbors dies.
# A dead cell will be brought back to live if it has exactly three live neighbors.
# ... therefore:
# new cell is dead by default
# if it has 2 neighbours, its state is the same as previous generation
# if it has 3 neigbours, it will be alive
def iterate():
    counts = get_board(0)
    for x, y in ((x, y) for y in range(h) for x in range(w)):
        if not board[x][y]: continue
        for dx, dy in ((dx, dy) for dy in range(-1, 2) for dx in range(-1, 2)):
            if (dy | dx) != 0:
                cx = x + dx
                cy = y + dy
                if cx >= 0 and cx < len(counts) and cy >= 0 and cy < len(counts[0]):
                    counts[cx][cy] += 1
    for x, y in ((x, y) for y in range(h) for x in range(w)):
        count = counts[x][y]
        n_cell = False
        if count == 2: n_cell = board[x][y]
        if count == 3: n_cell = True
        board[x][y] = n_cell

board[0][1] = True
board[2][0] = True
board[2][1] = True
board[2][2] = True
board[1][2] = True

i = 0
while(True):
    print('iteration', i)
    print_board(board)
    input()
    iterate()
    i += 1