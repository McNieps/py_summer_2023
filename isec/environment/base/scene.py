import pygame

from isec.environment.base.camera import Camera


class Scene:
    def __init__(self,
                 surface: pygame.Surface = None) -> None:

        if surface is None:
            surface = pygame.display.get_surface()

        self.camera = Camera()
        self.surface = surface
        self.rect = self.surface.get_rect()
