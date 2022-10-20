from entity import Ammulation


class NormalBullet(Ammulation):

    def __init__(self, user, root, side="player", **kwargs):
        super().__init__(user, root, side, **kwargs)
