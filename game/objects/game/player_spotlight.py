import pygame
import math

from isec.app import Resource
from isec.environment import Entity, Sprite, Pos


class PlayerSpotlight(Entity):
    def __init__(self, player_position: Pos) -> None:
        self.number_of_points = 50
        self.radius = 125
        self.opening_angle = 45

        self.sprite = Sprite(self.create_spotlight_surface(),
                             blit_flag=pygame.BLEND_ADD,
                             rendering_technique="rotated")

        super().__init__(position=player_position, sprite=self.sprite)

    # I want to make a spotlight using raycasting
    def create_polygon_spotlight(self,
                                 tilemap: list[list[int]],
                                 tile_size: int) -> pygame.Surface:

        pass


    def create_spotlight_surface(self) -> pygame.Surface:

        if self.number_of_points < 3:
            raise ValueError("Number of points must be at least 3.")

        surface = pygame.Surface((self.radius * 2, self.radius * 2))
        surface.set_colorkey((0, 0, 0))
        polygon_points = [(self.radius, self.radius)]

        for i in range(self.number_of_points):
            angle = -self.opening_angle/2 + self.opening_angle/self.number_of_points * i
            x = self.radius + self.radius * math.cos(math.radians(angle))
            y = self.radius + self.radius * math.sin(math.radians(angle))
            polygon_points.append((x, y))
        pygame.draw.polygon(surface, Resource.data["color"]["list"][-4], polygon_points)

        return surface
