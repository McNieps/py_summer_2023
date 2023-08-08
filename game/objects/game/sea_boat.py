from isec.app import Resource

from isec.environment import Entity, Pos, Sprite


class SeaBoat(Entity):
    def __init__(self) -> None:
        position = Pos(position=(190, 205))
        sprite = Sprite(Resource.image["game"]["boat"],
                        "static")

        super().__init__(position, sprite)
