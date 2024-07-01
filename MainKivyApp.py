from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button


from ChessGameWidget import ChessGameWidget

class CustomButton(Button):
    def __init__(self, **kwargs):
        super(CustomButton, self).__init__(**kwargs)
        self.font_size = 20
        self.color = (0, 0, 0, 1)  # White text color
        self.background_normal = ''  # Remove the default background image
        self.background_color = (0.3, 0.3, 0.3, 1) 
        self.size_hint = (1, None)
        self.height = 200

class ChessApp(App):
    def build(self):
        # iPhone 14 Pro Max aspect ratio: 19.5:9
        screen_width = 350
        screen_height = int(screen_width * 19.5 / 9)
        Window.size = (screen_width, screen_height)
        # Window.size = (self.root.width, self.root.height)
        main_layout = BoxLayout(orientation='vertical')
        buttons_layout = BoxLayout(orientation='horizontal')
        
        # Widgets to be added to layout
        back_button = CustomButton(text="<<")
        forward_button = CustomButton(text=">>")
        chess_game_widget = ChessGameWidget(board_width=screen_width*2, board_height=screen_width*2)  # Square board with full width
        
        buttons_layout.add_widget(back_button)
        buttons_layout.add_widget(forward_button)
        
        # Adding the widgets to the main layout
        main_layout.add_widget(chess_game_widget)
        main_layout.add_widget(buttons_layout)
        
        return main_layout


if __name__ == "__main__":
    ChessApp().run()
