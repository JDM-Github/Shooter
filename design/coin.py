
from random import randint
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex


class Coin(Image):

    def __init__(self, pos, value=50, **kwargs):
        super().__init__(**kwargs)
        self.x, self.y = pos
        self.size = 10, 10
        self.color = get_color_from_hex("fc7b03") if value <= 99 else (
            get_color_from_hex("a1a1a1") if value <= 299 else (
                get_color_from_hex("f7b90c") if value <= 999 else get_color_from_hex("ffffff")))
        self.value = value

    def update(self):
        if self.parent.parent.player.collide_point(*self.center):
            self.parent.parent.coin_bar.value += self.value
            self.parent.remove_widget(self)
