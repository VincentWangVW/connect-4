import pygame
import sys
from constants import *
from connect4 import Connect4
from ai import Connect4AI

class Connect4GUI:
    """
    Connect4GUI class that handles the graphical user interface for the Connect 4 game.
    It initializes the game, draws the board, handles user input, and displays game results.
    This class uses Pygame for rendering the game board and pieces, and it provides
    functionality to play against an AI opponent.
    """
    def __init__(self) -> None:
        """
        Initializes the Connect4GUI with Pygame, sets up the game window,
        initializes the game logic and AI, and draws the initial game board.
        :return: None
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Connect 4 - Unbeatable AI")
        self.font = pygame.font.SysFont("monospace", 75)
        self.button_font = pygame.font.SysFont("monospace", 20)
        self.game = Connect4()
        self.ai = Connect4AI(depth=5)  # Change this for "difficulty"
        self.show_play_again = False
        self.play_again_rect = None
        self.draw_board()

    def draw_board(self) -> None:
        """
        Draws the game board and pieces on the Pygame screen.
        :return: None
        """
        # Clear the screen first
        self.screen.fill(BLACK)

        # Draw the blue board background
        for col in range(BOARD_WIDTH):
            for row in range(BOARD_HEIGHT):
                pygame.draw.rect(self.screen, BLUE,
                                 (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE,
                                  SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(self.screen, BLACK,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   RADIUS)

        # Draw the pieces - Flipped to show board right-side up
        for col in range(BOARD_WIDTH):
            for row in range(BOARD_HEIGHT):
                if self.game.board[row][col] == PLAYER_PIECE:
                    pygame.draw.circle(self.screen, RED,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                        (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       RADIUS)
                elif self.game.board[row][col] == AI_PIECE:
                    pygame.draw.circle(self.screen, YELLOW,
                                       (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                                        (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       RADIUS)

        pygame.display.update()

    def show_message(self, text, color) -> None:
        """
        Displays a message at the top of the game window indicating the game result.
        :param text: The message text to display (e.g., "You win!", "AI wins!", "Draw!").
        :param color: The color of the text to display.
        :return: None
        """
        # Clear the top area
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))

        # Show the game result message
        label = self.font.render(text, 1, color)
        label_rect = label.get_rect(center=(WIDTH // 2, SQUARE_SIZE // 2 - 20))
        self.screen.blit(label, label_rect)

        # Show play again button
        self.show_play_again = True
        self.draw_play_again_button()

        pygame.display.update()

    def draw_play_again_button(self) -> None:
        """
        Draws the "Play Again" button on the screen when the game is over.
        :return: None
        """
        if self.show_play_again:
            # Button dimensions and position
            button_width = 200
            button_height = 50
            button_x = (WIDTH - button_width) // 2
            button_y = SQUARE_SIZE + 20

            # Store button rectangle for click detection
            self.play_again_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            # Draw button background
            pygame.draw.rect(self.screen, WHITE, self.play_again_rect)
            pygame.draw.rect(self.screen, BLACK, self.play_again_rect, 3)

            # Draw button text
            button_text = self.button_font.render("Play Again", True, BLACK)
            text_rect = button_text.get_rect(center=self.play_again_rect.center)
            self.screen.blit(button_text, text_rect)

    def reset_game(self) -> None:
        """
        Resets the game state to allow for a new game to be played.
        :return: None
        """
        self.game.reset()
        self.show_play_again = False
        self.play_again_rect = None
        self.draw_board()

    def run(self) -> None:
        """
        Main game loop that handles events, updates the game state, and renders the game board.
        :return: None
        """
        clock = pygame.time.Clock()  # Add clock for better performance

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION and not self.game.game_over:
                    pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                    posx = event.pos[0]
                    if 0 <= posx < WIDTH:  # Ensure mouse is within bounds
                        pygame.draw.circle(self.screen, RED, (posx, SQUARE_SIZE // 2), RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if play again button was clicked
                    if self.show_play_again and self.play_again_rect and self.play_again_rect.collidepoint(event.pos):
                        self.reset_game()
                        continue

                    # Regular game play
                    if not self.game.game_over:
                        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                        posx = event.pos[0]
                        col = posx // SQUARE_SIZE

                        # Ensure column is within valid range
                        if 0 <= col < BOARD_WIDTH:
                            if self.game.play_move(col):
                                self.draw_board()

                                if self.game.game_over:
                                    if self.game.winner == PLAYER_PIECE:
                                        self.show_message("You win!", RED)
                                    elif self.game.winner == AI_PIECE:
                                        self.show_message("AI wins!", YELLOW)
                                    else:
                                        self.show_message("Draw!", WHITE)
                                else:
                                    # AI's turn
                                    ai_move = self.ai.get_best_move(self.game)
                                    if ai_move is not None and 0 <= ai_move < BOARD_WIDTH:
                                        self.game.play_move(ai_move)
                                        self.draw_board()

                                        if self.game.game_over:
                                            if self.game.winner == PLAYER_PIECE:
                                                self.show_message("You win!", RED)
                                            elif self.game.winner == AI_PIECE:
                                                self.show_message("AI wins!", YELLOW)
                                            else:
                                                self.show_message("Draw!", WHITE)

            clock.tick(160)  # Limit to 60 FPS


if __name__ == "__main__":
    # Play the game!!!!
    gui = Connect4GUI()
    gui.run()