import typing

from isec.app import Resource
from isec.environment import Entity, Sprite
from isec.environment.position import PymunkPos

from game.objects.game.collision_types import CollisionTypes


class Rock(Entity):
    def __init__(self,
                 rock_type: typing.Literal["tiny", "small", "medium", "big"],
                 position: tuple[float, float],
                 speed: tuple[float, float] = None,
                 angle: float = 0) -> None:

        rock_surface = Resource.image["game"][f"{rock_type}_rock"]
        sprite = Sprite(rock_surface, rendering_technique="cached")

        position = PymunkPos(position=position,
                             speed=speed,
                             a=angle,
                             shape_collision_type=CollisionTypes.ROCK)

        radius_dict = {"tiny": 0.5,
                       "small": 0.75,
                       "medium": 1.75,
                       "big": 3.5}

        position.create_circle_shape(radius_dict[rock_type])

        super().__init__(position, sprite)
