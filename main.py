import pygame
import chess
import os
from helpers import *

# Initialize Pygame
pygame.init()
pygame.font.init() # you have to call this at the start, 
my_font = pygame.font.SysFont('Comic Sans MS', 30)
# Set up the display
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
BOARD_WIDTH, BOARD_HEIGHT = 800, 800
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Game")


# Colors
WHITE = (238,238,210)
BLACK = (118,150,86)
HIGHLIGHT_COLOR = (186, 202, 68)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)




def main():
    run = True
    clock = pygame.time.Clock()
    board = chess.Board()
    images = load_images()
    selected_square = None
    game_end_screen = False
    is_valid_moves_showing = False
    # flipped = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board.reset()
                    game_end_screen = False
                if event.key == pygame.K_u:
                    if board.move_stack:
                        board.pop()
                if event.key == pygame.K_m:
                    draw_valid_moves(WIN, board)

            
            if event.type == pygame.MOUSEBUTTONDOWN:
                square = get_square_under_mouse()
                print(board)
                if selected_square is None:
                    if board.piece_at(square) is not None:
                        selected_square = square
                        is_valid_moves_showing = True
                        # draw_valid_moves(WIN, board)
                else:
                    move = chess.Move(selected_square, square)
                    # print(move.uci())
                    if move in board.legal_moves:
                        board.push(move)
                        # board.push_san((str(move)))
                        
                        if board.is_stalemate():
                            print("STALEMATE")
                            game_end_screen = True
                        if board.is_checkmate():
                            print("CHECKMATE")
                            game_end_screen = True
                        # flipped = not flipped 
                    selected_square = None
                    is_valid_moves_showing = False
        
        
        draw_board(WIN, selected_square)
        pygame.draw.rect(WIN, (0, 0, 0), pygame.Rect(BOARD_WIDTH, 0, SCREEN_WIDTH-BOARD_WIDTH, SCREEN_HEIGHT))
        draw_pieces(WIN, board, images)
        draw_text(WIN, board)
        if is_valid_moves_showing:
            draw_valid_moves(WIN, board)
        draw_game_end_screen(WIN, game_end_screen)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()


