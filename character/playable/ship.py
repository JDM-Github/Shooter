from configuration import BLOCK_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH, WORLD_HEIGHT, WORLD_WIDTH
from kivy.graphics import Ellipse, Color
from ammulation import NormalBullet
from entity import EntityShip


class Ship(EntityShip):

    def __init__(self, attribute, upgrade, name, root, **kwargs):
        super().__init__("player", root, **kwargs)
        self.root = root
        self.name_ship = name
        self.all_attr = attribute[name]
        self.upgrade_attr = upgrade[name]
        self.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

        self.all_level_var()
        self.change_attribute_variable()
        self.move_variable()
        self.display_shield()
        self.bind(pos=self.set_position)

    def all_level_var(self):
        self.health_l = self.upgrade_attr["health"]
        self.shied_d_l = self.upgrade_attr["shield_d"]
        self.damage_m_l = self.upgrade_attr["damage_m"]
        self.damage_l = self.upgrade_attr["damage"]
        self.regen_l = self.upgrade_attr["regen"]
        self.cooldown_l = self.upgrade_attr["cooldown"]

    def change_attribute_variable(self):
        self.main_revive_cooldown = 2
        self.main_lives = self.all_attr["live"] + 1
        self.main_health = self.all_attr["health"][self.health_l]
        self.main_shield_duration = self.all_attr["shield_d"][self.shied_d_l]
        self.bullet_damage_mul = self.all_attr["damage_m"][self.damage_m_l]
        self.main_damage = self.all_attr["damage"][self.damage_l]
        self.main_cooldown = self.all_attr["cooldown"][self.cooldown_l]
        self.regenaration = self.main_health * \
            self.all_attr["regen"][self.regen_l]

        self.main_speed = self.all_attr["speed"]
        self.main_boost_speed = self.all_attr["boost"]
        self.set_attribute()
        self.set_attribute2()

    def set_attribute2(self):
        self.shield_duration = self.main_shield_duration
        self.revive_cooldown = self.main_revive_cooldown

    def ship_revive(self):
        if not self.main_lives <= 0:
            if self.revive_cooldown <= 0:
                self.color_.a = 0.8
                self.revive_cooldown = self.main_revive_cooldown
                self.main_health = self.all_attr["health"][self.health_l]
                self.original_health = self.all_attr["health"][self.health_l]
                self.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
                self.shield_duration = self.main_shield_duration
                self.root.health_bar.color_bar.rgb = (0, 1, 0)
                self.parent_wid.add_widget(self)
            self.revive_cooldown -= self.root.delta_time

    def display_shield(self):
        if not hasattr(self, "shield_"):
            self.color_ = Color(rgba=(.2, .6, 1, .8))
            self.radius = BLOCK_SIZE
            self.shield_ = Ellipse()
            self.shield_.size = self.radius*2, self.radius*2
            self.shield_.pos = self.center_x - self.radius, self.center_y - self.radius
        self.canvas.add(self.color_)
        self.canvas.add(self.shield_)

    def update_shield(self):
        if self.shield_duration <= 0:
            self.color_.a = 0
        elif self.shield_duration / self.main_shield_duration <= 0.8:
            self.color_.a = self.shield_duration / self.main_shield_duration
        self.shield_duration -= self.root.delta_time

    def check_if_can_damage(self, damage):
        if self.shield_duration <= 0:
            self.main_health -= damage
            if self.main_health <= 0:
                self.main_lives -= 1
                self.root.live_bar.update(self.main_lives)
                self.parent_wid = self.parent
                self.parent.remove_widget(self)
            self.hurt_animation()

    def move_variable(self):
        self.move_attack = False
        self.move_boost = False
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False

    def attack(self):
        if self.move_attack and self.current_cooldown <= 0:
            self.current_cooldown = self.main_cooldown
            self.root.player_all_bullet.add_widget(
                self.generate_bullet())
        self.current_cooldown -= self.root.delta_time

    def update(self):
        self.update_shield()
        return super().update()

    def regen_health(self):
        if self.current_regen_cooldown <= 0:
            if self.main_health + self.regenaration <= self.original_health:
                self.main_health += self.regenaration
            self.current_regen_cooldown = self.regen_cooldown
        self.current_regen_cooldown -= self.root.delta_time

    def generate_bullet(self):
        if self.type_of_ammunination == "normal_bullet":
            return NormalBullet(self, self.root, self.side)

    def update_position(self):
        self.speed = self.main_boost_speed * self.root.time_factor \
            if self.move_boost else self.main_speed * self.root.time_factor
        if self.move_left and self.move_right is False:
            self.x -= self.speed
        elif self.move_right and self.move_left is False:
            self.x += self.speed
        if self.move_down and self.move_up is False:
            self.y -= self.speed
        elif self.move_up and self.move_down is False:
            self.y += self.speed
        self.move_limitation()

    def set_position(self, *_):
        if hasattr(self, "shield_"):
            self.shield_.pos = self.center_x - self.radius, self.center_y - self.radius

    def move_limitation(self):
        if self.x <= 0:
            self.x = 0
        elif self.right >= WORLD_WIDTH:
            self.right = WORLD_WIDTH
        if self.y <= 0:
            self.y = 0
        elif self.top >= WORLD_HEIGHT:
            self.top = WORLD_HEIGHT
