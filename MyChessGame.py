import pygame
import chess
import os

class ChessBoard():
    def __init__(self):
        self.board = chess.Board()
        self.undone_moves_stack = []

    def reset(self):
        self.board.reset()
        self.undone_moves_stack.clear()

    def make_move(self, move_uci, promotion_piece=None):
        move = chess.Move.from_uci(move_uci)
        if move in self.board.legal_moves:
            if promotion_piece and self.board.piece_at(move.from_square).piece_type == chess.PAWN and (chess.square_rank(move.to_square) in [0, 7]):
                move = chess.Move(move.from_square, move.to_square, promotion=promotion_piece)
            self.board.push(move)
            self.undone_moves_stack.clear()
            return True
        return False

    def undo_last_move(self):
        if self.board.move_stack:
            last_move = self.board.pop()
            self.undone_moves_stack.append(last_move)
            return last_move
        return None

    def redo_last_move(self):
        if self.undone_moves_stack:
            move = self.undone_moves_stack.pop()
            self.board.push(move)
            return move
        return None

    def is_game_over(self):
        return self.board.is_game_over()

    def get_legal_moves(self, square=None):
        if square:
            return [move for move in self.board.legal_moves if move.from_square == square]
        return list(self.board.legal_moves)

    def get_fen(self):
        return self.board.fen()

    def set_fen(self, fen):
        self.board.set_fen(fen)

    def __str__(self):
        return str(self.board)

class MyChessGameUI():
    def __init__(self, screen_width, screen_height, board):
        pygame.init()
        pygame.font.init()
        self.FONT = pygame.font.SysFont('Arial', 30)
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen_width, screen_height
        self.BOARD_WIDTH, self.BOARD_HEIGHT = 800, 800
        self.TILE_SIZE = self.BOARD_WIDTH // 8
        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        
        self.is_game_running = True
        
        self.board = board
        self.selected_square = None
        self.game_end_screen = False
        self.is_valid_moves_showing = False
        
        self.COLORS = {
            "WHITE": (238,238,210), 
            "BLACK": (118,150,86), 
            "HIGHLIGHT_COLOR": (186, 202, 68), 
            "RED": (255, 0, 0), 
            "GREEN": (0, 255, 0), 
            "BLUE": (0, 0, 255), 
            "GRAY": (100, 100, 100), 
        }
        
        self.images = self.load_images()

    def load_images(self):
        pieces = ['P', 'R', 'N', 'B', 'Q', 'K', 'p', 'r', 'n', 'b', 'q', 'k']
        images = {}
        for piece in pieces:
            piece_color = "white" if piece.isupper() else "black"
            images[piece] = pygame.image.load(os.path.join("Chess", f"assets/{piece_color}/{piece}.png"))
        
        for key in images:
            images[key] = pygame.transform.scale(images[key], (self.TILE_SIZE, self.TILE_SIZE))
        
        return images

    def draw_board(self):
        self.SCREEN.fill(self.COLORS["WHITE"])
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    pygame.draw.rect(self.SCREEN, self.COLORS["BLACK"], (col * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                if self.selected_square and chess.square(col, row) == self.selected_square:
                    pygame.draw.rect(self.SCREEN, self.COLORS["HIGHLIGHT_COLOR"], (col * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.board.piece_at(chess.square(col, row))
                if piece:
                    piece_image = self.images[piece.symbol()]
                    self.SCREEN.blit(piece_image, (col * self.TILE_SIZE, row * self.TILE_SIZE))

    def draw_text(self):
        moves = list(self.board.board.move_stack)
        if moves:
            white_moves = [move for index, move in enumerate(moves) if index % 2 == 0]
            black_moves = [move for index, move in enumerate(moves) if index % 2 == 1]

            # display white label
            text_surface = self.FONT.render("White", False, (255, 255, 255))
            self.SCREEN.blit(text_surface, (800 + (400 // 3), 10))
            
            # display black label
            text_surface = self.FONT.render("Black", False, (255, 255, 255))
            self.SCREEN.blit(text_surface, (800 + (400 * 2 // 3), 10))

            for i, move in enumerate(white_moves):
                text_surface = self.FONT.render(str(move), False, (255, 255, 255))
                self.SCREEN.blit(text_surface, (800 + (400 // 3), 50 + i * 40))
                
            for i, move in enumerate(black_moves):
                text_surface = self.FONT.render(str(move), False, (255, 255, 255))
                self.SCREEN.blit(text_surface, (800 + (400 * 2 // 3), 50 + i * 40))

    def get_square_under_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        x, y = mouse_pos
        row = y // self.TILE_SIZE
        col = x // self.TILE_SIZE 
        return chess.square(col, row)

    def draw_game_end_screen(self):
        if self.game_end_screen:
            s = pygame.Surface((self.BOARD_WIDTH, self.BOARD_HEIGHT), pygame.SRCALPHA)
            s.fill((150,150,150,128))
            self.SCREEN.blit(s, (0,0))

    def draw_valid_moves(self):
        legal_moves = [str(move) for move in self.board.get_legal_moves(self.selected_square)]   
            
        # Mapping of files ('a' to 'h') to indices (0 to 7)
        cols = {letter: index for index, letter in enumerate('abcdefgh')}

        # Mapping of ranks ('1' to '8') to indices (0 to 7)
        rows = {str(index + 1): index for index in range(8)}
            
        moves = []
        for move in legal_moves:
            move = move[2:]
            letter, num_str = move[0],  move[1]
            x, y = cols[letter] * self.TILE_SIZE + (self.TILE_SIZE // 2), rows[num_str] * self.TILE_SIZE + (self.TILE_SIZE // 2)
            index = (x, y)
            moves.append(index)
        
        for pos in moves:
            pygame.draw.circle(self.SCREEN, self.COLORS["GRAY"], pos, 10)

    def handle_user_interaction(self, event):
        self.handle_key_down(event)
        self.handle_mouse_click(event)
        
    def handle_key_down(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.board.reset()
                self.game_end_screen = False
            if event.key == pygame.K_u:
                self.board.undo_last_move()
            if event.key == pygame.K_m:
                self.draw_valid_moves()
            if event.key == pygame.K_LEFT:
                self.board.undo_last_move()
            if event.key == pygame.K_RIGHT:
                self.board.redo_last_move()
                
    def handle_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            square = self.get_square_under_mouse()
            if self.selected_square is None:
                if self.board.board.piece_at(square) is not None and self.board.board.turn == self.board.board.piece_at(square).color:
                    self.selected_square = square
                    self.is_valid_moves_showing = True
            else:
                promotion_piece = None
                if self.board.board.piece_at(self.selected_square).piece_type == chess.PAWN and (chess.square_rank(square) == 0 or chess.square_rank(square) == 7):
                    promotion_piece = chess.QUEEN  # Default to queen for simplicity

                move = chess.Move(self.selected_square, square, promotion=promotion_piece)
                if move in self.board.board.legal_moves:
                    self.board.board.push(move)
                    
                    if self.board.board.is_stalemate():
                        print("STALEMATE")
                        self.game_end_screen = True
                    if self.board.board.is_checkmate():
                        print("CHECKMATE")
                        self.game_end_screen = True
                        
                self.selected_square = None
                self.is_valid_moves_showing = False
                
    def draw(self):
        self.draw_board()
        pygame.draw.rect(self.SCREEN, self.COLORS["BLACK"], pygame.Rect(self.BOARD_WIDTH, 0, self.SCREEN_WIDTH-self.BOARD_WIDTH, self.SCREEN_HEIGHT))
        self.draw_pieces()
        self.draw_text()
        if self.is_valid_moves_showing:
            self.draw_valid_moves()
        self.draw_game_end_screen()
        
    def run(self):
        while self.is_game_running:
            self.CLOCK.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_running = False
                self.handle_user_interaction(event)
            self.draw()
            pygame.display.update()

if __name__ == "__main__":
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
    board = ChessBoard()
    game = MyChessGameUI(SCREEN_WIDTH, SCREEN_HEIGHT, board)
    game.run()
