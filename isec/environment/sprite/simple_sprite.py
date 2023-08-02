import pygame
import typing

from collections.abc import Iterable

from isec.objects.cached_surface import CachedSurface
from isec.environment.sprite.rendering_techniques import RenderingTechniques


class SimpleSprite:
    __slots__ = ["surface", "rect", "effective_rect", "effective_surf", "_rendering_technique"]

    def __init__(self,
                 surface: pygame.Surface,
                 rendering_technique: typing.Literal["static", "rotated", "cached"]) -> None:
        """Initialize sprite."""

        self.surface = surface
        self.rect = self.surface.get_rect()
        self.rect.center = 0, 0

        self.effective_surf = self.surface.copy()
        self.effective_rect = self.rect.copy()

        self._rendering_technique = None
        self.set_rendering_technique(rendering_technique)

    def update(self,
               delta: float) -> None:
        """Update sprite."""

        pass

    def set_rendering_technique(self,
                                rendering_technique: typing.Literal["static", "rotated", "cached"]) -> None:
        """Set rendering technique."""

        if rendering_technique == "static":
            self._rendering_technique = RenderingTechniques.static

        elif rendering_technique == "rotated":
            self._rendering_technique = RenderingTechniques.rotated

        elif rendering_technique == "cached":
            if not isinstance(self.surface, CachedSurface):
                raise ValueError("Cached rendering technique requires cached surface.")
            self._rendering_technique = RenderingTechniques.cached

        else:
            raise ValueError("Invalid rendering technique.")

    def render(self,
               destination: pygame.Surface,
               destination_rect: pygame.Rect,
               offset: Iterable,
               angle: float) -> None:
        """Render sprite."""

        self._rendering_technique(self,
                                  destination,
                                  destination_rect,
                                  offset,
                                  angle)
