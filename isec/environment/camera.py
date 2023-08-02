import pygame

from collections.abc import Iterable

from isec.environment.position import StaticPos


class Camera:
    def __init__(self,
                 position: Iterable = None) -> None:

        if position is None:
            self.position = StaticPos()
        else:
            self.position = StaticPos(*position)

    def get_offset(self,
                   position: StaticPos) -> pygame.math.Vector2:

        return position.position - self.position.position

    def get_coordinates_from_screen(self,
                                    screen_coordinates: pygame.math.Vector2) -> pygame.math.Vector2:

        return screen_coordinates + self.position.position
