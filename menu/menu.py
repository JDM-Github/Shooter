from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle

from configuration import BAR_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
from .box import Box
from .close import Close
from .shop import Shop
from .keybind import KeyBind


class MenuButton(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.already = False
        self.size = (BAR_SIZE, BAR_SIZE)
        self.pos = (WINDOW_WIDTH-self.width-10, WINDOW_HEIGHT-self.height-10)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.display_menu()
        return super().on_touch_down(touch)

    def display_menu(self):
        if self.already is False:
            self.show_menu()
        else:
            self.close_window()

    def show_menu(self):
        self.parent.pause_game = True
        self.already = True
        if not hasattr(self, "background"):
            self.bg_color = Color(rgba=(.2, .2, .2, .5))
            self.background = RoundedRectangle(size=(
                WINDOW_WIDTH*0.8, WINDOW_HEIGHT*0.8), pos=(
                WINDOW_WIDTH*0.1, WINDOW_HEIGHT*0.1))
            self.canvas.add(self.bg_color)

            self.grid = GridLayout(cols=1, rows=4, padding=20, spacing=10)
            self.grid.size = self.background.size
            self.grid.pos = self.background.pos
            self.grid_children()

        self.canvas.add(self.background)
        self.add_widget(self.grid)

    def grid_children(self):
        self.close = Close()
        self.shop = Shop()
        self.setting = Box("Setting")
        self.exit = KeyBind()

        self.grid.add_widget(self.close)
        self.grid.add_widget(self.shop)
        self.grid.add_widget(self.setting)
        self.grid.add_widget(self.exit)

    def close_window(self):
        self.parent.pause_game = False
        self.already = False
        self.canvas.remove(self.background)
        self.remove_widget(self.grid)
