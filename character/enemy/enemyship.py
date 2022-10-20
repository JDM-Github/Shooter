from random import randint
from ammulation import NormalBullet
from configuration import WORLD_HEIGHT, WORLD_WIDTH
from entity import EntityShip


class EnemyShip(EntityShip):

    def __init__(self, root, **kwargs):
        super().__init__("enemy", root, **kwargs)
        self.small_chance = 10
        self.big_chance = 30
        self.jackpot_chance = 100
        self.small_value = 50
        self.big_value = 100
        self.jackpot_value = 200
        self.pos = (randint(0, WORLD_WIDTH-self.width), WORLD_HEIGHT)

    def attack(self):
        if (self.current_cooldown <= 0 and self.y + 200 > self.root.player.y
                and self.root.player in self.root.player_parent.children):
            self.current_cooldown = self.main_cooldown
            self.root.enemy_all_bullet.add_widget(
                self.generate_bullet())
        self.current_cooldown -= self.root.delta_time

    def update_position(self):
        self.speed = self.main_speed
        self.y -= self.speed * self.root.time_factor
        if self.top <= 0:
            self.parent.remove_widget(self)

    def generate_bullet(self):
        if self.type_of_ammunination == "normal_bullet":
            return NormalBullet(self, self.root, self.side)

    def drop_on_dead(self):
        if randint(0, self.jackpot_chance) == self.jackpot_chance:
            self.root.drop_on_dead(self.center, self.jackpot_value)
        elif randint(0, self.big_chance) == self.big_chance:
            self.root.drop_on_dead(self.center, self.big_chance)
        elif randint(0, self.small_chance) == self.small_chance:
            self.root.drop_on_dead(self.center, self.small_value)
        self.parent.remove_widget(self)
