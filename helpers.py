import pygame
import chess
import os

pygame.init()
pygame.font.init() # you have to call this at the start, 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
BOARD_WIDTH, BOARD_HEIGHT = 800, 800

# Colors
WHITE = (238,238,210)
BLACK = (118,150,86)
HIGHLIGHT_COLOR = (186, 202, 68)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

def load_images():
    pieces = ['P', 'R', 'N', 'B', 'Q', 'K', 'p', 'r', 'n', 'b', 'q', 'k']
    images = {}
    for piece in pieces:
        if piece.isupper():
            
            images[piece] = pygame.image.load(os.path.join("Chess", f"assets/white/{piece}.png"))
        else:
            images[piece] = pygame.image.load(os.path.join("Chess", f"assets/black/{piece}.png"))
    
    for key in images:
        tile_size = BOARD_WIDTH // 8
        images[key] = pygame.transform.scale(images[key], (tile_size, tile_size))
    
    return images
    

def draw_board(win, selected_square):
    win.fill(WHITE)
    tile_size = BOARD_WIDTH // 8
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                pygame.draw.rect(win, BLACK, (col * tile_size, row * tile_size, tile_size, tile_size))
            if selected_square and chess.square(col, row) == selected_square:
                pygame.draw.rect(win, HIGHLIGHT_COLOR, (col * tile_size, row * tile_size, tile_size, tile_size))

def draw_pieces(win, board, images):
    tile_size = BOARD_WIDTH // 8
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, row))
            # piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_image = images[piece.symbol()]
                win.blit(piece_image, (col * tile_size, row * tile_size))
                
def draw_text(win, board):
    """
    - 2 columns
    - first row is label (white/black)
    - each row is one move
        - left is white
        - right is black
    """
    moves = list(board.move_stack)
    # moves = [board.san(move) for move in moves]
    if moves:
        white_moves = [move for index, move in enumerate(moves) if index % 2 == 0]
        black_moves = [move for index, move in enumerate(moves) if index % 2 == 1]

        # display white label
        text_surface = my_font.render("White", False, (255, 255, 255))
        win.blit(text_surface, (800 + (400 // 3), 10))
        
        # display black label
        text_surface = my_font.render("Black", False, (255, 255, 255))
        win.blit(text_surface, (800 + (400 * 2 // 3), 10))

        for i, move in enumerate(white_moves):

            text_surface = my_font.render(str(move), False, (255, 255, 255))
            win.blit(text_surface, (800 + (400 // 3), 50 + i * 40))
            
        for i, move in enumerate(black_moves):
            text_surface = my_font.render(str(move), False, (255, 255, 255))
            win.blit(text_surface, (800 + (400 * 2 // 3), 50 + i * 40))

def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos
    tile_size = BOARD_WIDTH // 8 # BOARD_WIDTH == BOARD_HEIGHT
    
    row = y // tile_size
    col = x // tile_size 
    
    return chess.square(col, row) # 0 - 63

def draw_game_end_screen(win, game_end_screen):
    if game_end_screen:
        s = pygame.Surface((BOARD_WIDTH,BOARD_HEIGHT), pygame.SRCALPHA)   # per-pixel alpha
        s.fill((150,150,150,128))                         # notice the alpha value in the color
        win.blit(s, (0,0))
        
        
################################################################################################        
def draw_valid_moves(win, board, move=None):
    print(board.legal_moves)
    legal_moves = [str(move) for move in list(board.legal_moves)]
    print(legal_moves)
    """
    a8 = 0, 0
    a7 = 1, 0
    b8 = 0, 1
    """
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    b = {}
    for i, letter in enumerate(a):
        b[letter] = i
    aa = ['1', '2', '3', '4', '5', '6', '7', '8']
    bb = {}
    for i, num_str in enumerate(aa):
        bb[num_str] = i    
        
        
    moves = []
    for move in legal_moves:
        move = move[2:]
        letter = move[0]
        num_str = move[1]
        tile_size = BOARD_WIDTH // 8
        x = b[letter] * tile_size + (tile_size // 2)
        y = bb[num_str] * tile_size + (tile_size // 2)
        index = (x, y)
        moves.append(index)
        # print(index)
    
    for pos in moves:
        pygame.draw.circle(win, (100, 100, 100), pos, 10)