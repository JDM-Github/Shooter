from configuration import WINDOW_HEIGHT
from .designbar import DesignBar
from kivy.graphics import Rectangle, Color
from kivy.uix.image import Image
from kivy.animation import Animation


class HealthBar(DesignBar):

    def __init__(self, **kwargs):
        super().__init__(size=(10, 1), **kwargs)
        self.display_health()
        self.bind(pos=self.change_, size=self.change_)
        self.pos = 10, WINDOW_HEIGHT-self.height-10

    def display_health(self):
        self.background = Image(opacity=0.5, size=self.size, pos=self.pos)
        self.add_widget(self.background)
        with self.canvas:
            self.color_bar = Color(rgb=(0, 1, 0))
            self.health_bar = Rectangle(size=self.size, pos=self.pos)
        self.old_health = self.width

    def change_(self, *_):
        self.health_bar.size = self.background.size = self.size
        self.health_bar.pos = self.background.pos = self.pos

    def update_health(self, health, max_health):
        if health <= 0:
            self.health_bar.size = self.size
            self.color_bar.rgb = (0.2, 0.2, 0.2)
            self.old_health = 0
        else:
            health_result = self.width * (health / max_health)
            self.health_bar.size = health_result, self.height
            if self.old_health > health_result:
                self.hurt_animation()
            self.old_health = health_result

    def hurt_animation(self):
        anim = Animation(rgb=(1, 0, 0), d=0.05)
        anim += Animation(rgb=(0, 1, 0), d=0.05)
        anim.start(self.color_bar)
