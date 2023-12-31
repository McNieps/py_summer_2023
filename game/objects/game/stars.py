from isec.app import Resource

from isec.environment import Entity, Pos, Sprite


class Stars(Entity):
    def __init__(self) -> None:
        position = Pos(position=(190, 78))
        sprite = Sprite(Resource.image["menu"]["stars"],
                        "static")

        super().__init__(position, sprite)
