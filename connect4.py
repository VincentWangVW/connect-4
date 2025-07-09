import numpy as np
from constants import *

class Connect4:
    """
    Connect4 game logic class that manages the game state, board, and player turns.
    It provides methods to reset the game, drop pieces, check for valid moves,
    determine winning conditions, and play moves.
    """
    def __init__(self) -> None:
        """
        Initializes the Connect4 game with an empty board, sets the game state,
        and defines the starting player.
        :return: None
        """
        self.board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        self.game_over = False
        self.turn = PLAYER_PIECE
        self.winner = None

    def reset(self) -> None:
        """
        Resets the game state to start a new game.
        :return: None
        """
        self.board = np.zeros((BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        self.game_over = False
        self.winner = None
        self.turn = PLAYER_PIECE

    def drop_piece(self, row, col, piece) -> None:
        """
        Drops a piece into the specified column and row on the board.
        :param row: The row index where the piece will be placed.
        :param col: The column index where the piece will be placed.
        :param piece: The piece to be placed (PLAYER_PIECE or AI_PIECE).
        :return: None
        """
        self.board[row][col] = piece

    def is_valid_location(self, col) -> bool:
        """
        Checks if the specified column is a valid location for dropping a piece.
        :param col: The column index to check for validity.
        :return: True if the column is valid (not full), False otherwise.
        """
        return self.board[0][col] == EMPTY

    def get_next_open_row(self, col) -> int:
        """
        Finds the next open row in the specified column.
        :param col: The column index to check for the next open row.
        :return: The row index of the next open row, or -1 if no open row exists.
        """
        for row in range(BOARD_HEIGHT - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                return row
        return -1

    def winning_move(self, piece) -> bool:
        """
        Checks if the specified piece has a winning move on the board.
        :param piece: The piece to check for a winning move (PLAYER_PIECE or AI_PIECE).
        :return: True if the piece has a winning move, False otherwise.
        """
        # Check horizontal
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH - 3):
                if all(self.board[row][col + i] == piece for i in range(WINDOW_LENGTH)):
                    return True

        # Check vertical
        for col in range(BOARD_WIDTH):
            for row in range(BOARD_HEIGHT - 3):
                if all(self.board[row + i][col] == piece for i in range(WINDOW_LENGTH)):
                    return True

        # Check positive diagonals
        for row in range(BOARD_HEIGHT - 3):
            for col in range(BOARD_WIDTH - 3):
                if all(self.board[row + i][col + i] == piece for i in range(WINDOW_LENGTH)):
                    return True

        # Check negative diagonals
        for row in range(3, BOARD_HEIGHT):
            for col in range(BOARD_WIDTH - 3):
                if all(self.board[row - i][col + i] == piece for i in range(WINDOW_LENGTH)):
                    return True

        return False

    def is_board_full(self) -> bool:
        """
        Checks if the board is full (no more valid moves available).
        :return: True if the board is full, False otherwise.
        """
        return all(self.board[0][col] != EMPTY for col in range(BOARD_WIDTH))

    def play_move(self, col) -> bool:
        """
        Plays a move by dropping a piece into the specified column.
        :param col: The column index where the piece will be dropped.
        :return: bool: True if the move was successful, False if the column is invalid or the game is over.
        """
        if not self.game_over and self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.drop_piece(row, col, self.turn)

            if self.winning_move(self.turn):
                self.game_over = True
                self.winner = self.turn
            elif self.is_board_full():
                self.game_over = True
            else:
                self.turn = AI_PIECE if self.turn == PLAYER_PIECE else PLAYER_PIECE
            return True
        return False