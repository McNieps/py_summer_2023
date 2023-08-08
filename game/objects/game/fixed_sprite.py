import pygame

from isec.app import Resource
from isec.environment import Entity, Pos, Sprite


class FixedSprite(Entity):
    def __init__(self,
                 position: tuple[float, float],
                 angle: float,
                 sprite_surface: list[str]) -> None:

        raw_surface = Resource.image
        for key in sprite_surface:
            raw_surface = raw_surface[key]

        surface = pygame.transform.rotate(Resource.image[sprite_surface[0]][sprite_surface[1]], angle)
        sprite = Sprite(surface, rendering_technique="static")
        position = Pos(position=position,
                       a=angle)

        super().__init__(position, sprite)
