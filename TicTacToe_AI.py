import pygame
import AI


def draw_grid(window):
    color = (255, 255, 255)
    grid = [(175 * y + 25, 175 * x + 25, 160, 160) for x in range(3) for y in range(3)]
    collision_grid = []
    for rectangle in grid:
        field = pygame.draw.rect(window, color, rectangle)
        collision_grid.append(field)
    pygame.display.update()

    return collision_grid


def reset_board():
    return [[0 for _ in range(3)] for _ in range(3)]


def reset_locked_positions():
    return [True for _ in range(3) for _ in range(3)]


def check_all_positions(board):
    for row in board:
        for element in row:
            if element == 0:
                return True
    return False


def turn_text(window, board, font, player, game_winner, color=(255, 255, 255)):
    sx = 435 // 2 - 35
    sy = 590
    pygame.draw.rect(window, (0, 0, 0), (sx, sy, 300, 50))
    if not game_winner:
        if check_all_positions(board):
            if player == 'cross':
                label = font.render('Human\'s turn', 1, color)
            else:
                label = font.render('AI\'s turn', 1, color)
        else:
            label = font.render('Draw', 1, color)
        window.blit(label, (sx, sy))
    else:
        if player == 'circle':
            label = font.render('X wins', 1, color)
        else:
            label = font.render('O wins', 1, color)
        window.blit(label, (sx, sy))

    pygame.display.update()


def reset_text(window, font, color=(255, 255, 255)):
    sx = 575
    sy = 450
    label_top = font.render('Press SPACE', True, color)
    label_bottom = font.render('to reset board', True, color)

    window.blit(label_top, (sx, sy))
    window.blit(label_bottom, (sx, sy + 50))


def draw_winning_line(window, grid, winning_line, sign):
    for i in range(9):
        if i in winning_line:
            if sign == 'cross':
                draw_X(window, grid[i], (255, 0, 0))
            else:
                draw_O(window, grid[i], (255, 0, 0))
    pygame.display.update()


def win_check(board, player):
    # Check rows
    query_field = 0
    for row in range(3):
        winning_line = []
        for field in range(3):
            if board[row][field] == player:
                winning_line.append(query_field)
            query_field += 1
        if len(winning_line) == 3:
            return True, winning_line

    # Check columns
    query_field, next_field = 0, 0
    for column in range(3):
        winning_line = []
        query_field = next_field
        next_field += 1
        for row in board:
            if row[column] == player:
                winning_line.append(query_field)
            query_field += 3
        if len(winning_line) == 3:
            return True, winning_line

    # Check diagonals
    query_field = 0
    winning_line = []
    for field in range(3):
        if board[field][field] == player:
            winning_line.append(query_field)
        query_field += 4
    if len(winning_line) == 3:
        return True, winning_line

    query_field = 2
    winning_line = []
    for field in range(3):
        if board[field][2 - field] == player:
            winning_line.append(query_field)
        query_field += 2
    if len(winning_line) == 3:
        return True, winning_line

    return False, [-1, -1, -1]


def update_board(board, locked_positions, update_field, value):
    current_field = 0
    for row in range(3):
        for field in range(3):
            if update_field == current_field:
                board[row][field] = value
            current_field += 1

    current_field = 0
    for query_position in range(9):
        if update_field == current_field:
            locked_positions[query_position] = False
        current_field += 1


def draw_X(window, field, color=(0, 0, 0)):
    x_start, y_start = field[0], field[1]
    x_start += 15
    y_start += 15
    start_point1 = (x_start, y_start)
    end_point1 = (x_start + 130, y_start + 130)
    pygame.draw.line(window, color, start_point1, end_point1, 10)
    start_point2 = (x_start, y_start + 130)
    end_point2 = (x_start + 130, y_start)
    pygame.draw.line(window, color, start_point2, end_point2, 10)

    pygame.display.update()


def draw_O(window, field, color=(0, 0, 0)):
    x_center, y_center = field[0], field[1]
    x_center += 80
    y_center += 80
    radius = 65
    pygame.draw.circle(window, color, (x_center, y_center), radius, 7)

    pygame.display.update()


def statistic(window, record, color=(255, 255, 255)):
    font = pygame.font.SysFont('comicsans', 40, italic=True)
    sx = 550
    sy = 25
    pygame.draw.rect(window, color, (sx, sy, 335, 160), 3)
    pygame.draw.rect(window, (0, 0, 0), (sx + 5, sy + 5, 325, 150))
    label_X = font.render('Human:          ' + str(record[0]), True, color)
    label_draw = font.render('Draw:             ' + str(record[1]), True, color)
    label_O = font.render('AI:                 ' + str(record[2]), True, color)

    window.blit(label_X, (sx + 10, sy + 10))
    window.blit(label_draw, (sx + 10, sy + 60))
    window.blit(label_O, (sx + 10, sy + 110))

    pygame.display.update()


def draw_XO(window, grid, board, locked_positions, mouse_position, draw_object):
    query_field = 0
    for field, open_position in zip(grid, locked_positions):
        if field.collidepoint(mouse_position) and open_position:
            if draw_object == 'cross':
                draw_X(window, field)
                draw_object = 'circle'
                update_board(board, locked_positions, query_field, 1)
            else:
                draw_O(window, field)
                draw_object = 'cross'
                update_board(board, locked_positions, query_field, 2)
        query_field += 1
    return draw_object


def main():
    pygame.init()

    window_width, window_height = 900, 685
    game_window = pygame.display.set_mode((window_width, window_height))
    game_window.fill((0, 0, 0))
    pygame.display.set_caption("Tic Tac Toe")
    game_font = pygame.font.SysFont('comicsans', 60)

    game_board = reset_board()
    game_grid = draw_grid(game_window)

    # cross - human;    circle - AI
    current_object = 'cross'  # cross/circle

    run, winner = True, False
    game_locked_positions = reset_locked_positions()
    game_record = [0, 0, 0]
    change_record = True

    while run:
        pygame.time.delay(27)

        statistic(game_window, game_record)
        turn_text(game_window, game_board, game_font, current_object, winner)
        reset_text(game_window, game_font)

        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                run = False

            # Reset event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_board = reset_board()
                    game_locked_positions = reset_locked_positions()
                    run, winner = True, False
                    change_record = True
                    game_grid = draw_grid(game_window)

            if event.type == pygame.MOUSEBUTTONUP and current_object == 'cross' and check_all_positions(game_board):
                turn_text(game_window, game_board, game_font, current_object, winner)
                position = pygame.mouse.get_pos()

                if not winner:
                    current_object = draw_XO(game_window, game_grid, game_board, game_locked_positions, position,
                                             current_object)
            elif current_object == 'circle' and check_all_positions(game_board):
                turn_text(game_window, game_board, game_font, current_object, winner)
                position = AI.AI_best_move(game_board)
                if not winner:
                    current_object = AI.AI_draw_XO(game_window, game_grid, position[0], position[1], current_object,
                                                   game_board, game_locked_positions)

        win, win_line = win_check(game_board, 1)
        if win:
            winner = True
            draw_winning_line(game_window, game_grid, win_line, 'cross')
            current_object = 'circle'
            if change_record:
                game_record[0] += 1
                change_record = False
        win, win_line = win_check(game_board, 2)
        if win:
            winner = True
            draw_winning_line(game_window, game_grid, win_line, 'circle')
            current_object = 'cross'
            if change_record:
                game_record[2] += 1
                change_record = False

        if change_record:
            all_locked_positions = 0
            for locked_position in game_locked_positions:
                if locked_position:
                    break
                all_locked_positions += 1
            if all_locked_positions == 9:
                game_record[1] += 1
                change_record = False

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()
