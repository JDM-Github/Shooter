from .box import Box


class Shop(Box):

    def __init__(self, **kwargs):
        super().__init__("Shop", **kwargs)
