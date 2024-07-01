from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.uix.label import Label
from kivy.core.window import Window

from ChessKivy import ChessGameWidget


class ChessApp(App):
    def build(self):
        # iPhone 14 Pro Max aspect ratio: 19.5:9
        screen_width = 350
        screen_height = int(screen_width * 19.5 / 9)
        Window.size = (screen_width, screen_height)
        # Window.size = (self.root.width, self.root.height)
        layout = BoxLayout(orientation='vertical')
        
        chess_game_widget = ChessGameWidget(board_width=screen_width*2, board_height=screen_width*2)  # Square board with full width
        layout.add_widget(chess_game_widget)
        
        
        return layout


if __name__ == "__main__":
    ChessApp().run()
