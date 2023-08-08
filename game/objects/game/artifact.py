from isec.app import Resource
from isec.environment import Entity, Pos
from isec.environment.sprite import AnimatedSprite


class Artifact(Entity):
    def __init__(self):
        self.position = Pos((556, 200))
        self.animated_sprite = AnimatedSprite([Resource.image["game"][f"artifact_{i+1}"] for i in range(8)],
                                              [0.2 for _ in range(8)])

        super().__init__(self.position, self.animated_sprite)

        print(Artifact.__name__)
