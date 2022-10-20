from kivy.animation import Animation
from kivy.uix.image import Image
from configuration import BLOCK_SIZE


class EntityShip(Image):

    def __init__(self, side, root, **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.size = (BLOCK_SIZE, BLOCK_SIZE)
        self.side = side
        self.attribute_variable()

    def attribute_variable(self):
        self.regenaration = 0
        self.bullet_damage_mul = 1
        self.main_health = 200
        self.main_damage = 50
        self.main_speed = 2
        self.main_cooldown = 1
        self.regen_cooldown = 1
        self.type_of_ammunination = "normal_bullet"
        self.set_attribute()

    def set_attribute(self):
        self.current_regen_cooldown = self.regen_cooldown
        self.original_health = self.main_health
        self.current_cooldown = self.main_cooldown

    def update(self):
        self.attack()
        self.update_position()
        self.regen_health()

    def regen_health(self):
        pass

    def attack(self):
        pass

    def update_position(self):
        pass

    def hurt_animation(self):
        anim = Animation(color=(1, 0, 0, 1), d=0.05)
        anim += Animation(color=(1, 1, 1, 1), d=0.05)
        anim.start(self)
