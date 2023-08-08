import pygame

from isec.app import Resource

from isec.environment import Entity, Pos
from isec.environment.sprite import AnimatedSprite


class SeaTop(Entity):
    def __init__(self) -> None:
        position = Pos(position=(200, 187.5))

        top_size = (400, 75)

        # Only get the top half of the images
        surfaces = []
        for i in range(4):
            surfaces.append(pygame.Surface(top_size))
            surfaces[-1].blit(Resource.image["game"][f"sea_{i+1}"],
                              (0, 0))

        sprite = AnimatedSprite(surfaces,
                                [0.5, 0.5, 0.5, 0.5],
                                True,
                                "static")

        super().__init__(position, sprite)
