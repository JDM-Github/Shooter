from configuration import BAR_SIZE
from .designbar import DesignBar
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.properties import NumericProperty


class CoinBar(DesignBar):

    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__([1, 1], **kwargs)
        self.color = get_color_from_hex("f7b90c")
        self.pos = (10, 10)
        self.display_label()
        self.bind(value=self.update_text)

    def display_label(self):
        self.label = Label(
            text=f"{self.value}", valign="center", halign="left")
        self.label.bind(size=self.label.setter("text_size"))
        self.label.size = (10*BAR_SIZE, BAR_SIZE)
        self.label.pos = (self.right + 10, 10)
        self.add_widget(self.label)

    def update_text(self, *_):
        self.label.text = f"{self.value}"
        self.parent.game_progress["Coin"] = self.value
        self.parent.save_progress()
        # print(self.parent.game_progress)
