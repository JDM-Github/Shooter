from kivy.uix.image import Image

from configuration import BULLET_HEIGHT, BULLET_WIDTH, WINDOW_HEIGHT


class Ammulation(Image):

    def __init__(self, user, root, side, **kwargs):
        super().__init__(**kwargs)
        self.root = root
        self.user = user
        self.side = side
        self.dependencies()
        self.attributes()

    def dependencies(self):
        self.size = (BULLET_WIDTH, BULLET_HEIGHT)
        self.center = self.user.center

    def attributes(self):
        self.range = self.x + 400
        self.range_ = self.x
        self.damage = 50
        self.speed = 8
        self.dx = self.calc_slope() if self.side != "player" else 0
        self.dy = self.speed

    def update(self):
        self.update_position()

    def update_position(self):
        if self.side == "player":
            self.y += self.speed * self.root.time_factor
            self.range_ += self.speed * self.root.time_factor
            if self.y >= WINDOW_HEIGHT or self.range_ >= self.range or self.check_if_hit():
                self.parent.remove_widget(self)
        elif self.side == "enemy":
            self.x += self.dx * self.root.time_factor
            self.y -= self.speed * self.root.time_factor
            self.range_ += self.speed * self.root.time_factor
            if self.top <= 0 or self.range_ >= self.range or self.check_if_hit():
                self.parent.remove_widget(self)

    def calc_slope(self):
        y = self.user.y - self.root.player.center_y
        x = self.user.x - self.root.player.center_x
        result = -(x / y) if -(x / y) <= 5 else 0
        if abs((self.x + result) - self.root.player.x) < abs(self.x - self.root.player.x) and abs(y) > 50:
            return result
        return 0

    def check_if_hit(self) -> bool:
        if self.side == "player":
            for enemy in self.root.all_enemy.children:
                if enemy.collide_point(*self.center):
                    enemy.main_health -= self.damage * self.user.bullet_damage_mul
                    if enemy.main_health <= 0:
                        enemy.drop_on_dead()
                    enemy.hurt_animation()
                    return True
        elif self.side == "enemy":
            player = self.root.player
            if player in self.root.player_parent.children:
                if player.collide_point(*self.center):
                    player.check_if_can_damage(
                        self.damage * self.user.bullet_damage_mul)
                    return True
        return False
