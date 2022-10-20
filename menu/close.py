from .box import Box


class Close(Box):

    def __init__(self, **kwargs):
        super().__init__("Continue", **kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent.parent.close_window()
        return super().on_touch_down(touch)
