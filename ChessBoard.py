import chess

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

    def is_opponent_piece(self, square, player_color):
        piece = self.board.piece_at(square)
        if piece is not None and piece.color != player_color:
            return True
        return False

    def current_turn_color(self):
        return chess.WHITE if self.board.turn else chess.BLACK

    def __str__(self):
        return str(self.board)
