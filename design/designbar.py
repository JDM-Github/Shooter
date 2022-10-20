from kivy.uix.image import Image

from configuration import BAR_SIZE


class DesignBar(Image):

    def __init__(self, size, **kwargs):
        super().__init__(**kwargs)
        self.size = (BAR_SIZE*size[0], BAR_SIZE*size[1])
