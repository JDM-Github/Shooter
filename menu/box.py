from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.metrics import sp


class Box(Image):

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text_label = text
        self.color = get_color_from_hex("039dfc")
        self.display_label()
        self.bind(size=self.update_box, pos=self.update_box)

    def display_label(self):
        self.label = Label(text=self.text_label)
        self.label.font_size = sp(32)
        self.add_widget(self.label)

    def update_box(self, *_):
        self.label.size = self.size
        self.label.pos = self.pos
