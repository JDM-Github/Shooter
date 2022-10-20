from .enemyship import EnemyShip


class EnemyShip01(EnemyShip):

    def __init__(self, root,  **kwargs):
        super().__init__(root, **kwargs)
        self.change_attribute()

    def change_attribute(self):
        self.main_health = 100
        self.bullet_damage_mul = 1
        self.main_cooldown = 0.8
        self.set_attribute()
