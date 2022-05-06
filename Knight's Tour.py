past_pos = []
visited_squares = 0
sequence = 1


class OutOfBoundsError(Exception):
    pass


def check_start_inputs():
    while True:
        dimensions_size = str(input('Enter your board dimensions: '))
        size = [int(num) for num in dimensions_size.split() if num.isdigit()]
        try:
            if len(size) > 2 or len(size) < 2 or size[0] < 0 or size[1] < 0 or size[0] < 1 or size[1] < 1:
                raise OutOfBoundsError
        except OutOfBoundsError:
            print('Invalid dimensions!')
            check_start_inputs()

        else:
            while True:
                starting_pos = str(input("Enter the knight's starting position: "))
                pos = [int(num) for num in starting_pos.split() if num.isdigit()]
                try:
                    if len(pos) > 2 or len(pos) < 2:
                        raise OutOfBoundsError
                    elif not 0 < pos[0] < size[0] + 1 or not 0 < pos[1] < size[1] + 1:
                        raise OutOfBoundsError

                except OutOfBoundsError:
                    print('Invalid position!')
                else:
                    board = create_board(size)
                    ask_player(size, board, pos)
                    break
        break


def ask_player(size, board, pos):
    user = str(input('Do you want to try the puzzle? (y/n):'))
    try:
        if user != 'y' and user != 'n':
            raise OutOfBoundsError
    except OutOfBoundsError:
        print('Invalid input!')
        ask_player(size, board, pos)
    else:
        if user == 'y':
            puzzle_solution(size, board, 1, pos)
        else:
            puzzle_solution(size, board, 0, pos)


def check_input(size, board, valid):
    while True:
        if valid:
            new_pos = str(input('\nEnter your next move: '))
            pos = [int(num) for num in new_pos.split() if num.isdigit()]
        else:
            new_pos = str(input('Invalid move! Enter your next move: '))
            pos = [int(num) for num in new_pos.split() if num.isdigit()]
        try:
            if len(pos) > 2 or len(pos) < 2:
                raise OutOfBoundsError
            elif not 0 < pos[0] < size[0] + 1 or not 0 < pos[1] < size[1] + 1:
                raise OutOfBoundsError
            elif pos == past_pos:
                raise OutOfBoundsError
            elif check_l_shape_move(pos):
                raise OutOfBoundsError

        except OutOfBoundsError:
            check_input(size, board, False)
        else:
            edit_board(pos, size, board, 0,  None)
            break


def create_board(dimensions_size):
    board = [[' ' for _ in range(dimensions_size[0])] for _ in range(dimensions_size[1])]
    return board


def puzzle_solution(size, board, option, pos):
    try:
        if size[0] == size[1] and 1 < size[0] < 5 and 1 < size[0] < 5:
            raise OutOfBoundsError
        if size[0] < 3 or size[1] < 3 and size[0] != 1 and size[1] != 1 and size:
            raise OutOfBoundsError
    except OutOfBoundsError:
        print('No solution exists!')
    else:
        if option == 1:
            edit_board(pos, size, board, 0, None)
            while not check_win(board, size, 1):
                check_input(size, board, True)
        else:
            edit_board([0, 0], size, board, 1, False)
            if puzzle_solver(size, board, [0, 0]):
                print_board(board, size)


def puzzle_solver(size, board, last_pos):
    if check_win(board, size, 0):
        return True
    next_pos = Warnsdorffs_rule(board, last_pos, 1)
    best_possible_move = (0, 0, size[1])
    if len(next_pos) == 0:
        edit_board(last_pos, size, board, 1, True)
        for i in range(size[1]):
            for j in range(size[0]):
                if board[i][j] == str(sequence):
                    next_pos = Warnsdorffs_rule(board, [i, j], size)
                    break
        for i in next_pos:
            if i[2] >= last_pos[2] and i != last_pos:
                best_possible_move = i
        edit_board(best_possible_move, size, board, 1, False)
        return puzzle_solver(size, board, best_possible_move)
    for i in next_pos:
        if i[2] <= best_possible_move[2]:
            best_possible_move = i
    edit_board(best_possible_move, size, board, 1, False)
    return puzzle_solver(size, board, best_possible_move)


def check_l_shape_move(pos):
    if past_pos[0] + 2 == pos[0] or past_pos[0] - 2 == pos[0]:
        if past_pos[1] + 1 == pos[1] or past_pos[1] - 1 == pos[1]:
            return False
    elif past_pos[1] + 2 == pos[1] or past_pos[1] - 2 == pos[1]:
        if past_pos[0] + 1 == pos[0] or past_pos[0] - 1 == pos[0]:
            return False
    else:
        return True


def edit_board(knight_pos, size, board, mode, backtrack):
    global past_pos, visited_squares, sequence
    if mode == 0:
        pos_x, pos_y = knight_pos[1], knight_pos[0]
        visited_squares += 1
        board[-pos_x][pos_y-1] = 'X'
        for i in range(size[1]):
            for j in range(size[0]):
                if board[i][j] != 'X' and board[i][j] != '*':
                    board[i][j] = ' '
        if len(past_pos) > 0:
            board[-past_pos[1]][past_pos[0] - 1] = '*'
        past_pos = [pos_y, pos_x]
        Warnsdorffs_rule(board, knight_pos, mode)
        print_board(board, size)
    else:
        if backtrack:
            if board[knight_pos[0]][knight_pos[1]] != ' ':
                board[knight_pos[0]][knight_pos[1]] = ' '
                sequence -= 1
        else:
            if board[knight_pos[0]][knight_pos[1]] == ' ':
                board[knight_pos[0]][knight_pos[1]] = str(sequence)
                sequence += 1


def Warnsdorffs_rule(board, pos, mode):
    new_positions = []
    moves = [[2, 1], [-2, 1], [2, -1], [-2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2]]
    next_pos = []
    for possible_pos in moves:
        try:
            if mode == 0:
                x = -pos[1] + possible_pos[0]
                y = pos[0] - 1 + possible_pos[1]
                if x < 0 and y >= 0:
                    if board[x][y] == ' ':
                        new_positions.append((x, y))
            else:
                x = pos[0] + possible_pos[0]
                y = pos[1] + possible_pos[1]
                if x >= 0 and y >= 0:
                    if board[x][y] == ' ':
                        new_positions.append((x, y))
        except IndexError:
            continue
    for xy in new_positions:
        count = 0
        for possible_pos in moves:
            try:
                if board[xy[0] + possible_pos[0]][xy[1] + possible_pos[1]] == ' ':
                    if abs(xy[0] - possible_pos[0]) > 0 and xy[1] + possible_pos[1] >= 0:
                        count += 1
            except IndexError:
                continue
        next_pos.append((xy[0], xy[1], count))
        if mode == 0:
            board[xy[0]][xy[1]] = str(count)
    return next_pos


def check_win(board, size, mode):
    global visited_squares
    gap = False
    if mode == 1:
        for i in range(size[1]):
            for j in range(size[0]):
                if board[i][j].isdigit():
                    return False
                if board[i][j] == ' ':
                    gap = True
        if gap:
            print('\nNo more possible moves!')
            print(f'Your knight visited {visited_squares} squares!')
            return True
        print('\nWhat a great tour! Congratulations!')
        return True
    elif mode == 0:
        for i in range(size[1]):
            for j in range(size[0]):
                if board[i][j] == ' ':
                    return False
        print("Here's the solution!")
        return True


def print_board(board, size):
    x, y = size[1], size[0]
    n = x
    cell_size = len(str(y*x))
    border_lenght = y * (cell_size + 1) + 3
    line = f'{n}|'
    last_line = '   '
    for i in range(1, y + 1):
        last_line += f'{i} ' + (cell_size - 1) * ' '
    print(' ' + '-' * border_lenght)
    for i in range(x):
        for j in range(y):
            if board[i][j] != ' ':
                if sequence >= 10:
                    if len(board[i][j]) == 1:
                        line += ' '
                        line += ' ' * (cell_size-1) + board[i][j]
                    else:
                        line += ' ' * (cell_size-1) + board[i][j]
                else:
                    line += ' ' * cell_size + board[i][j]
            else:
                line += ' ' + '_' * cell_size
            if j == y - 1:
                line += ' |'
        print(line)
        n -= 1
        line = f'{n}|'
    print(' ' + '-' * border_lenght)
    print(last_line)


check_start_inputs()
