import TicTacToe_AI


def AI_best_move(board):
    best_score = float('-inf')
    best_move = [-1, -1]
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minimax(board, 0, False)
                board[i][j] = 0
                if score > best_score:
                    best_score = score
                    best_move = [i, j]
    return best_move


def minimax(board, depth, is_maximizing):
    result = AI_check_win(board)
    if result != -2:
        return result

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                # Check for available spot
                if board[i][j] == 0:
                    board[i][j] = 2
                    score = minimax(board, depth + 1, False)
                    board[i][j] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                # Check for available spot
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = minimax(board, depth + 1, True)
                    board[i][j] = 0
                    best_score = min(score, best_score)
        return best_score


def AI_check_win(board):
    scores = [0, -1, 1]
    # Horizontal
    for i in range(3):
        if board[i][0] != 0 and board[i][0] == board[i][1] == board[i][2]:
            return scores[board[i][0]]
    # Vertical
    for i in range(3):
        if board[0][i] != 0 and board[0][i] == board[1][i] == board[2][i]:
            return scores[board[0][i]]
    # Diagonal
    if board[0][0] != 0 and board[0][0] == board[1][1] == board[2][2]:
        return scores[board[0][0]]
    if board[2][0] != 0 and board[2][0] == board[1][1] == board[0][2]:
        return scores[board[2][0]]

    # Check for draw
    open_spots = 0
    for row in board:
        for element in row:
            if element == 0:
                open_spots += 1

    if open_spots == 0:
        return 0
    else:
        return -2


def fast_check_win(board, mark):
    return ((board[0][0] == mark and board[0][1] == mark and board[0][2] == mark) or  # top
            (board[1][0] == mark and board[1][1] == mark and board[1][2] == mark) or  # middle
            (board[2][0] == mark and board[2][1] == mark and board[2][2] == mark) or  # bottom
            (board[0][0] == mark and board[1][0] == mark and board[2][0] == mark) or  # left
            (board[0][1] == mark and board[1][1] == mark and board[2][1] == mark) or  # centre
            (board[0][2] == mark and board[1][2] == mark and board[2][2] == mark) or  # right
            (board[0][0] == mark and board[1][1] == mark and board[2][2] == mark) or  # LR diagonal
            (board[0][2] == mark and board[1][1] == mark and board[2][0] == mark))  # RL diagonal


def AI_draw_XO(window, grid, x, y, AI_object, board, locked_positions):
    index = 3 * x + y
    field = grid[index]
    if AI_object == 'cross':
        TicTacToe_AI.draw_X(window, field)
        next_object = 'circle'
        TicTacToe_AI.update_board(board, locked_positions, index, 1)
    else:
        TicTacToe_AI.draw_O(window, field)
        next_object = 'cross'
        TicTacToe_AI.update_board(board, locked_positions, index, 2)
    return next_object
