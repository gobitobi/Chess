from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

import os
import chess
from ChessBoard import ChessBoard


class ChessGameWidget(Widget):
    def __init__(self, board_width, board_height, **kwargs):
        super(ChessGameWidget, self).__init__(**kwargs)
        self.board_width = board_width
        self.board_height = board_height
        self.chessboard = ChessBoard()
        self.selected_square = None
        self.is_valid_moves_showing = False
        self.is_flipped = False

        self.COLORS = {
            "WHITE": (238/255, 238/255, 210/255, 1), 
            "BLACK": (118/255, 150/255, 86/255, 1), 
            "HIGHLIGHT_COLOR": (186/255, 202/255, 68/255, 1), 
            "GRAY": (100/255, 100/255, 100/255, 1)
        }

        self.piece_images = self.load_images()
        self.bind(size=self.update_board, pos=self.update_board)

    def load_images(self):
        pieces = ['P', 'R', 'N', 'B', 'Q', 'K', 'p', 'r', 'n', 'b', 'q', 'k']
        images = {}
        for piece in pieces:
            piece_color = "white" if piece.isupper() else "black"
            images[piece] = f"assets/{piece_color}/{piece}.png"
        return images

    def update_board(self, *args):
        self.canvas.clear()
        with self.canvas:
            for row in range(8):
                for col in range(8):
                    x, y = self.get_tile_coordinates(row, col)
                    Color(*self.COLORS["WHITE"] if (row + col) % 2 == 0 else self.COLORS["BLACK"])
                    Rectangle(pos=(x, y), size=(self.board_width / 8, self.board_height / 8))
                    if self.selected_square and chess.square(col, row) == self.selected_square:
                        Color(*self.COLORS["HIGHLIGHT_COLOR"])
                        Rectangle(pos=(x, y), size=(self.board_width / 8, self.board_height / 8))
                    piece = self.chessboard.board.piece_at(chess.square(col, row))
                    if piece:
                        image_path = self.piece_images[piece.symbol()]
                        Rectangle(source=image_path, pos=(x, y), size=(self.board_width / 8, self.board_height / 8))

            if self.is_valid_moves_showing:
                self.draw_valid_moves()

    def get_tile_coordinates(self, row, col):
        if self.is_flipped:
            row, col = 7 - row, 7 - col
        return col * self.board_width / 8, row * self.board_height / 8

    def on_touch_down(self, touch):
        row = int(touch.y // (self.board_height / 8))
        col = int(touch.x // (self.board_width / 8))
        if self.is_flipped:
            row, col = 7 - row, 7 - col
        try:
            square = chess.square(col, row)
            player_color = self.chessboard.current_turn_color()
            if self.selected_square is None:
                if self.chessboard.board.piece_at(square) is not None and self.chessboard.board.turn == self.chessboard.board.piece_at(square).color:
                    self.selected_square = square
                    self.is_valid_moves_showing = True
            else:
                promotion_piece = None
                if self.chessboard.board.piece_at(self.selected_square).piece_type == chess.PAWN and (chess.square_rank(square) == 0 or chess.square_rank(square) == 7):
                    promotion_piece = chess.QUEEN  # Default to queen for simplicity

                move = chess.Move(self.selected_square, square, promotion=promotion_piece)
                if move in self.chessboard.board.legal_moves:
                    self.chessboard.board.push(move)
                    if self.chessboard.is_opponent_piece(square, player_color):
                        print("Move captures an opponent's piece!")
                    if self.chessboard.board.is_stalemate():
                        print("STALEMATE")
                    if self.chessboard.board.is_checkmate():
                        print("CHECKMATE")

                self.selected_square = None
                self.is_valid_moves_showing = False
        except Exception as e:
            print(e)
        else:
            self.update_board()

    def draw_valid_moves(self):
        legal_moves = [str(move) for move in self.chessboard.get_legal_moves(self.selected_square)]
        with self.canvas:
            for move in legal_moves:
                move = move[2:]
                col = 'abcdefgh'.index(move[0])
                row = int(move[1]) - 1
                # if self.is_flipped:
                #     row, col = 7 - row, 7 - col
                x, y = self.get_tile_coordinates(row, col)
                Color(*self.COLORS["GRAY"])
                Ellipse(pos=(x + self.board_width / 16 - 10, y + self.board_height / 16 - 10), size=(20, 20))


