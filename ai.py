import math
from constants import *

class Connect4AI:
    """
    Connect4AI class that implements the Minimax algorithm with alpha-beta pruning
    to determine the best move for the AI player in a Connect 4 game.
    It evaluates the game state and scores potential moves to find the optimal play.
    This class can be used with any Connect 4-like board configuration, not just the standard one.
    It provides methods to get valid moves, check for terminal states, evaluate board positions,
    and find the best move using the Minimax algorithm.
    """
    def __init__(self, depth=8) -> None:
        """
        Initializes the AI with a specified depth for the Minimax algorithm.
        :param depth: The depth of the search tree for the Minimax algorithm.
        """
        self.depth = depth

    def get_valid_moves(self, board) -> list:
        """
        Returns a list of valid columns where a piece can be dropped in the current board state.
        :param board: The current game board represented as a 2D list.
        :return: A list of column indices where a piece can be dropped.
        """
        return [col for col in range(BOARD_WIDTH) if board[0][col] == EMPTY]

    def is_terminal_node(self, board) -> bool:
        """
        Checks if the game is over, either by a win for either player or if the board is full.
        :param board: The current game board represented as a 2D list.
        :return: True if the game is over (win or draw), False otherwise.
        """
        cond1 = self.winning_move(board, PLAYER_PIECE)
        cond2 = self.winning_move(board, AI_PIECE)
        cond3 = all(board[0][col] != EMPTY for col in range(BOARD_WIDTH))
        return cond1 or cond2 or cond3

    def winning_move(self, board, piece) -> bool:
        """
        Checks if the specified piece has a winning move on the given board.
        :param board: The current game board represented as a 2D list.
        :param piece: The piece to check for a winning move (PLAYER_PIECE or AI_PIECE).
        :return: True if the piece has a winning move, False otherwise.
        """
        # Same logic as Connect4 class but works on any board
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH - 3):
                if all(board[row][col + i] == piece for i in range(WINDOW_LENGTH)):
                    return True
        for col in range(BOARD_WIDTH):
            for row in range(BOARD_HEIGHT - 3):
                if all(board[row + i][col] == piece for i in range(WINDOW_LENGTH)):
                    return True
        for row in range(BOARD_HEIGHT - 3):
            for col in range(BOARD_WIDTH - 3):
                if all(board[row + i][col + i] == piece for i in range(WINDOW_LENGTH)):
                    return True
        for row in range(3, BOARD_HEIGHT):
            for col in range(BOARD_WIDTH - 3):
                if all(board[row - i][col + i] == piece for i in range(WINDOW_LENGTH)):
                    return True
        return False

    def evaluate_window(self, window, piece) -> int:
        """
        Evaluates a window (a segment of the board) for scoring based on the presence of pieces.
        :param window: A list representing a segment of the board (horizontal, vertical, or diagonal).
        :param piece: The piece to evaluate (PLAYER_PIECE or AI_PIECE).
        :return: An integer score for the window based on the pieces present.
        """
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
        score = 0

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, piece) -> int:
        """
        Scores the current board position for the specified piece.
        :param board: The current game board represented as a 2D list.
        :param piece: The piece to score (PLAYER_PIECE or AI_PIECE).
        :return: An integer score representing the board position for the piece.
        """
        score = 0

        # Score center column
        center_array = [board[row][BOARD_WIDTH // 2] for row in range(BOARD_HEIGHT)]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score horizontal
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH - 3):
                window = [board[row][col + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        # Score vertical
        for col in range(BOARD_WIDTH):
            for row in range(BOARD_HEIGHT - 3):
                window = [board[row + i][col] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        # Score diagonals
        for row in range(BOARD_HEIGHT - 3):
            for col in range(BOARD_WIDTH - 3):
                window = [board[row + i][col + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for row in range(BOARD_HEIGHT - 3):
            for col in range(3, BOARD_WIDTH):
                window = [board[row + i][col - i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player) -> tuple:
        """
        The Minimax algorithm with alpha-beta pruning to find the best move for the AI.
        :param board: 2D list representing the current game board state.
        :param depth: Integer representing the remaining depth to explore in the game tree.
        :param alpha: Best already explored option along the path to the root for the maximizer.
        :param beta: Best already explored option along the path to the root for the minimizer.
        :param maximizing_player: Boolean indicating whether the current turn is the AI's (True) or the player's (False).
        :return: Tuple (best_column, score) — the column index to play and the corresponding score.
        """
        valid_moves = self.get_valid_moves(board)
        is_terminal = self.is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, AI_PIECE):
                    return (None, 100000000)
                elif self.winning_move(board, PLAYER_PIECE):
                    return (None, -100000000)
                else:
                    return (None, 0)
            else:
                return (None, self.score_position(board, AI_PIECE))

        if maximizing_player:
            value = -math.inf
            column = valid_moves[0]
            for col in valid_moves:
                row = self.get_next_open_row(board, col)
                board_copy = board.copy()
                self.drop_piece(board_copy, row, col, AI_PIECE)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
            value = math.inf
            column = valid_moves[0]
            for col in valid_moves:
                row = self.get_next_open_row(board, col)
                board_copy = board.copy()
                self.drop_piece(board_copy, row, col, PLAYER_PIECE)
                new_score = self.minimax(board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_next_open_row(self, board, col) -> int:
        """
        Finds the next available row in the specified column where a piece can be dropped.
        :param board: 2D list representing the current game board state.
        :param col: Integer representing the column to check for the next open row.
        :return: Integer representing the row index of the next available spot, or -1 if the column is full.
        """
        for row in range(BOARD_HEIGHT - 1, -1, -1):
            if board[row][col] == EMPTY:
                return row
        return -1

    def drop_piece(self, board, row, col, piece) -> None:
        """
        Places a game piece in the specified location on the board.
        :param board: 2D list representing the current game board state.
        :param row: Integer representing the row index to place the piece.
        :param col: Integer representing the column index to place the piece.
        :param piece: Integer representing the piece (PLAYER_PIECE or AI_PIECE).
        :return: None
        """
        board[row][col] = piece

    def get_best_move(self, game) -> int:
        """
        Determines the best column to play for the AI using the minimax algorithm.
        :param game: Object representing the current game state, which includes the board.
        :return: Integer representing the best column index for the AI to play.
        """
        board = game.board.copy()
        move, _ = self.minimax(board, self.depth, -math.inf, math.inf, True)
        return move
