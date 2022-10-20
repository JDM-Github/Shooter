from configuration import BAR_SIZE, WINDOW_WIDTH
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout


class LiveBar(Widget):

    def __init__(self, live, **kwargs):
        super().__init__(**kwargs)
        self.size = BAR_SIZE*live, BAR_SIZE
        if self.width >= WINDOW_WIDTH / 2:
            self.width = WINDOW_WIDTH / 2
        self.live = live
        self.pos = WINDOW_WIDTH - self.width - 10, 10
        self.display_life()

    def display_life(self):
        self.grid = GridLayout(rows=1, cols=self.live)
        self.grid.size = self.size
        self.grid.pos = self.pos
        self.grid.spacing = self.width * 0.01
        self.all_live = list()
        for i in range(self.live):
            self.all_live.append(Image(color=(.5, .7, 1)))
            self.grid.add_widget(self.all_live[i])
        self.add_widget(self.grid)

    def update(self, live):
        if live < self.live:
            self.all_live[live].color = (.2, .2, .2)
