import pygame

from isec.app import Resource

from isec.environment import Entity, Pos
from isec.environment.sprite import AnimatedSprite


class SeaBottom(Entity):
    def __init__(self) -> None:
        bottom_offset = 150+75
        bottom_size = (400, 225)
        position = Pos(position=(200, bottom_offset+bottom_size[1]/2))

        # Only get the top half of the images
        surfaces = []
        for i in range(4):
            surfaces.append(pygame.Surface(bottom_size))
            surfaces[-1].blit(Resource.image["game"][f"sea_{i+1}"],
                              (0, -75))
            surfaces[-1].set_colorkey((0, 0, 0))

        sprite = AnimatedSprite(surfaces,
                                [0.5, 0.5, 0.5, 0.5],
                                True,
                                "static")

        super().__init__(position, sprite)
