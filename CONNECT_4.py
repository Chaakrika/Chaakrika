import numpy as np
import random

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
ROW_COUNT = 6
COLUMN_COUNT = 7
WINNING_LENGTH = 4

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, row, col, player):
    board[row][col] = player

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, player):
    for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
        for r in range(ROW_COUNT):
            if np.all(board[r, c:c + WINNING_LENGTH] == player):
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
            if np.all(board[r:r + WINNING_LENGTH, c] == player):
                return True

    for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
        for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
            if np.all(np.diagonal(board[r:r + WINNING_LENGTH, c:c + WINNING_LENGTH]) == player):
                return True

    for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
        for r in range(WINNING_LENGTH - 1, ROW_COUNT):
            if np.all(np.diagonal(board[r - WINNING_LENGTH + 1:r + 1, c:c + WINNING_LENGTH]) == player):
                return True

def print_board(board):
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            print(board[r][c], end=" ")
        print()
    print()

def evaluate_window(window, player):
    score = 0
    opp_player = PLAYER_X if player == PLAYER_O else PLAYER_O

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_player) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, player):
    score = 0

    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(player)
    score += center_count * 3

    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
            window = row_array[c:c + WINNING_LENGTH]
            score += evaluate_window(window, player)

    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
            window = col_array[r:r + WINNING_LENGTH]
            score += evaluate_window(window, player)

    for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
            window = [board[r + i][c + i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, player)

    for r in range(ROW_COUNT - (WINNING_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINNING_LENGTH - 1)):
            window = [board[r + 3 - i][c + i] for i in range(WINNING_LENGTH)]
            score += evaluate_window(window, player)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_X) or winning_move(board, PLAYER_O) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, PLAYER_O):
                return None, -100000000000
            elif winning_move(board, PLAYER_X):
                return None, 100000000000
            else:  
                return None, 0
        else:  
            return None, score_position(board, PLAYER_O)

    if maximizing_player:
        value = -np.Inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_X)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:  
        value = np.Inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_O)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def main():
    board = create_board()
    print_board(board)
    game_over = False

    while not game_over:
        while True:
            try:
                column = int(input("Enter your move (0-6): "))
                if 0 <= column < COLUMN_COUNT and is_valid_location(board, column):
                    break
                else:
                    print("Invalid move. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 6.")

        row = get_next_open_row(board, column)
        drop_piece(board, row, column, PLAYER_O)
        print_board(board)

        if winning_move(board, PLAYER_O):
            print("Congratulations! You win!")
            game_over = True
            break

        if len(get_valid_locations(board)) == 0:
            print("It's a tie!")
            game_over = True
            break

        column, _ = minimax(board, 5, True)  
        row = get_next_open_row(board, column)
        drop_piece(board, row, column, PLAYER_X)
        print_board(board)

        if winning_move(board, PLAYER_X):
            print("Sorry, the computer wins!")
            game_over = True
            break

        if len(get_valid_locations(board)) == 0:
            print("It's a tie!")
            game_over = True
            break

if __name__ == "__main__":
    main()

