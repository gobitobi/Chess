import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# Colors (RGB)
WHITE = (238,238,210)
BLACK = (118,150,86)


CELL_SIZE = SCREEN_WIDTH // 8

PIECES = {
    'pD': pygame.image.load('assets/pD.png'),
    'pL': pygame.image.load('assets/pL.png'),
    'rD': pygame.image.load('assets/rD.png'),
    'rL': pygame.image.load('assets/rL.png'),
    'nD': pygame.image.load('assets/nD.png'),
    'nL': pygame.image.load('assets/nL.png'),
    'bD': pygame.image.load('assets/bD.png'),
    'bL': pygame.image.load('assets/bL.png'),
    'qD': pygame.image.load('assets/qD.png'),
    'qL': pygame.image.load('assets/qL.png'),
    'kD': pygame.image.load('assets/kD.png'),
    'kL': pygame.image.load('assets/kL.png'),
}
# Resize piece images to fit the tiles
for key in PIECES:
    PIECES[key] = pygame.transform.scale(PIECES[key], (CELL_SIZE, CELL_SIZE))

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chess')



def draw_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            color = WHITE if (i + j) % 2 == 0 else BLACK
            rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

def draw_pieces(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != '--':
                piece = board[i][j]
                screen.blit(PIECES[piece], (j * CELL_SIZE, i * CELL_SIZE))


### HELPERS ###
def convert_coordinates_to_indices(coor):
    return coor[0] // CELL_SIZE, coor[1] // CELL_SIZE

def init_board():
    return np.array([
        ['rD', 'nD', 'bD', 'qD', 'kD', 'bD', 'nD', 'rD'],
        ['pD', 'pD', 'pD', 'pD', 'pD', 'pD', 'pD', 'pD'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['pL', 'pL', 'pL', 'pL', 'pL', 'pL', 'pL', 'pL'],
        ['rL', 'nL', 'bL', 'qL', 'kL', 'bL', 'nL', 'rL']
    ])
    
def display_valid_moves(moves):
    pass

def calculate_valid_moves(board, piece, position):
    row, col = position
    piece_type = piece[0]
    color = piece[1]
    directions = []
    valid_moves = []

    if piece_type == 'p':  # Pawn
        if color == 'D':  # Dark pawns move down
            if row + 1 < 8 and board[row + 1][col] == '--':
                valid_moves.append((row + 1, col))
                if row == 1 and board[row + 2][col] == '--':  # Initial two-square move
                    valid_moves.append((row + 2, col))
            if row + 1 < 8 and col + 1 < 8 and board[row + 1][col + 1] != '--' and board[row + 1][col + 1][1] == 'L':
                valid_moves.append((row + 1, col + 1))  # Capture move
            if row + 1 < 8 and col - 1 >= 0 and board[row + 1][col - 1] != '--' and board[row + 1][col - 1][1] == 'L':
                valid_moves.append((row + 1, col - 1))  # Capture move
        else:  # Light pawns move up
            if row - 1 >= 0 and board[row - 1][col] == '--':
                valid_moves.append((row - 1, col))
                if row == 6 and board[row - 2][col] == '--':  # Initial two-square move
                    valid_moves.append((row - 2, col))
            if row - 1 >= 0 and col + 1 < 8 and board[row - 1][col + 1] != '--' and board[row - 1][col + 1][1] == 'D':
                valid_moves.append((row - 1, col + 1))  # Capture move
            if row - 1 >= 0 and col - 1 >= 0 and board[row - 1][col - 1] != '--' and board[row - 1][col - 1][1] == 'D':
                valid_moves.append((row - 1, col - 1))  # Capture move

    elif piece_type == 'r':  # Rook
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    elif piece_type == 'b':  # Bishop
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]

    elif piece_type == 'q':  # Queen
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    elif piece_type == 'k':  # King
        king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for move in king_moves:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == '--' or board[new_row][new_col][1] != color:
                    valid_moves.append((new_row, new_col))

    elif piece_type == 'n':  # Knight
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for move in knight_moves:
            new_row, new_col = row + move[0], col + move[1]
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if board[new_row][new_col] == '--' or board[new_row][new_col][1] != color:
                    valid_moves.append((new_row, new_col))

    # Handle rook, bishop, and queen moves
    for direction in directions:
        new_row, new_col = row + direction[0], col + direction[1]
        while 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == '--':
                valid_moves.append((new_row, new_col))
            elif board[new_row][new_col][1] != color:
                valid_moves.append((new_row, new_col))
                break
            else:
                break
            new_row += direction[0]
            new_col += direction[1]

    return valid_moves



# Clock object to control the frame rate
clock = pygame.time.Clock()


# Main game loop
def main():
    running = True
    selected_piece = None
    selected_pos = None
    valid_moves = None
    # player_turn = False
    turn = 'L' # D for dark, L for light
    
    board = init_board()
    print(board)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = np.array([
                        ['rD', 'nD', 'bD', 'qD', 'kD', 'bD', 'nD', 'rD'],
                        ['pD', 'pD', 'pD', 'pD', 'pD', 'pD', 'pD', 'pD'],
                        ['--', '--', '--', '--', '--', '--', '--', '--'],
                        ['--', '--', '--', '--', '--', '--', '--', '--'],
                        ['--', '--', '--', '--', '--', '--', '--', '--'],
                        ['--', '--', '--', '--', '--', '--', '--', '--'],
                        ['pL', 'pL', 'pL', 'pL', 'pL', 'pL', 'pL', 'pL'],
                        ['rL', 'nL', 'bL', 'qL', 'kL', 'bL', 'nL', 'rL']
                    ])
            if event.type == pygame.MOUSEBUTTONUP:
                print('SELECTED PIECE: ', selected_piece)
                y, x = convert_coordinates_to_indices(event.pos)
                if selected_piece:
                    # Attempt to move the selected piece
                    if (x, y) != selected_pos and (x, y) in valid_moves:  # Ensure not the same position
                        print('piece put DOWN')
                        piece = board[selected_pos[0]][selected_pos[1]]
                        # if player_turn:  # Ensure it's the correct player's turn
                        board[selected_pos[0]][selected_pos[1]], board[x][y] = '--', piece
                        # player_turn = not player_turn  # Switch turn
                        turn = 'L' if turn == 'D' else 'D'
                        print('piece moved!')
                        print(board)
                        
                    selected_piece = None
                    selected_pos = None
                    valid_moves = None
                else:
                    # Select a piece
                    if board[x][y] != '--' and board[x][y][1] == turn:
                        print('piece picked UP')
                        selected_piece = board[x][y]
                        selected_pos = (x, y)
                        print('selected_piece: ', selected_piece)
                        print('selected_pos: ', selected_pos)
                        valid_moves = calculate_valid_moves(board, selected_piece, selected_pos)
                        print('Valid moves: ', valid_moves)

        # Game logic goes here

        # Drawing code goes here
        draw_board(board)
        draw_pieces(board)
        
        # Highlight selected piece
        if selected_piece:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(selected_pos[1] * CELL_SIZE, selected_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
        
        # Flip the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)
    
    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



"""
- user clicks on a piece
- calculate valid moves
- initial position is stored
- user clicks on new cell
- move piece if new cell is in valid moves

Check each turn:
- is my King in check
- are there any pins
- did castling already happen
- is castling available
- how many of the valid moves lead to check
- did en passant happen
- is en passant available
"""