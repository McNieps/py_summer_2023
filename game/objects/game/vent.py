from isec.app import Resource
from isec.environment import Entity, Pos, Sprite

from game.objects.game.bubble import Bubble


class Vent(Entity):
    def __init__(self,
                 position: tuple[float, float],
                 angle: float,
                 strength: float,
                 pattern: list[float],
                 offset: float) -> None:

        position = Pos(position=position,
                       a=angle)
        sprite = Sprite(Resource.image["game"]["vent"], rendering_technique="cached")

        super().__init__(position, sprite)
