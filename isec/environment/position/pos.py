from collections.abc import Iterable

import pygame


class Pos:
    """
    An abstract position class
    """

    __slots__ = ["position", "speed", "accel", "damping", "a", "va", "aa", "a_damping"]

    def __init__(self,
                 position: Iterable = (0, 0),
                 speed: Iterable = (0, 0),
                 accel: Iterable = (0, 0),
                 damping: float = 1,
                 a: float = 0,
                 va: float = 0,
                 aa: float = 0,
                 a_damping: float = 1) -> None:

        self.position: pygame.Vector2 = pygame.Vector2(*position)
        self.speed: pygame.Vector2 = pygame.Vector2(*speed)
        self.accel: pygame.Vector2 = pygame.Vector2(*accel)
        self.damping = damping

        self.a = a
        self.va = va
        self.aa = aa
        self.a_damping = a_damping

    def update(self,
               delta: float) -> None:
        pass
