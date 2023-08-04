import pygame
import numpy
import math

from isec.app import Resource
from isec.environment.base.scene import Scene, Camera


class TilemapScene(Scene):
    EMPTY_TILE = -1

    def __init__(self,
                 tilemap: list[list[int]],
                 tileset: dict[int, pygame.Surface],
                 surface: pygame.Surface = None) -> None:

        super().__init__(surface)

        self.tilemap = tilemap
        self.tilemap_size = len(tilemap[0]), len(tilemap)
        self.tileset = tileset
        self.tile_size = self.tileset[0].get_size()[0]
        self._inter_tile_distance = 0

        if not self._check_tileset_validity():
            raise ValueError("Invalid tileset")

    def _check_tileset_validity(self) -> bool:
        return all(tile in self.tileset for row in self.tilemap for tile in row)

    @property
    def inter_tile_distance(self):
        return self._inter_tile_distance

    @inter_tile_distance.setter
    def inter_tile_distance(self, value) -> None:
        self._inter_tile_distance = value
        self.tile_size = self.tileset[0].get_size()[0] + self.inter_tile_distance
        if self.tile_size <= 0:
            self.tile_size = 1

    def render(self,
               camera: Camera = None) -> None:

        if camera is None:
            camera = self.camera

        camera_pos = pygame.Vector2(math.floor(camera.position.position[0]), math.floor(camera.position.position[1]))
        start_x = max(0, math.floor(camera_pos[0]/self.tile_size))
        end_x = min(math.ceil((camera_pos[0]+self.rect.width)/self.tile_size), self.tilemap_size[0])
        start_y = max(0, math.floor(camera_pos[1]/self.tile_size))
        end_y = min(math.ceil((camera_pos[1]+self.rect.height)/self.tile_size), self.tilemap_size[1])

        pos_x = numpy.arange(end_x)*self.tile_size - camera_pos[0]
        pos_y = numpy.arange(end_y)*self.tile_size - camera_pos[1]

        self.surface.fblits([(self.tileset[self.tilemap[y][x]], (pos_x[x], pos_y[y]))
                             for x in range(start_x, end_x)
                             for y in range(start_y, end_y)
                             if self.tilemap[y][x] != -1])

        """
        for y in range(start_y, end_y):
            coord_y = pos_y[y]
            for x in range(start_x, end_x):
                if (tile := self.tilemap[y][x]) != self.EMPTY_TILE:
                    self.surface.blit(self.tileset[tile],
                                      (pos_x[x], coord_y))
        """

        return

    def update(self, delta):
        pass


if __name__ == '__main__':
    def draw_circle(_tilemap: list[list[int]],
                    x: int,
                    y: int,
                    radius: int,
                    tile: int) -> None:

        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                if numpy.sqrt((x - i) ** 2 + (y - j) ** 2) <= radius:
                    _tilemap[j][i] = tile

    tile_map = [[TilemapScene.EMPTY_TILE for _ in range(100)] for _ in range(100)]
    draw_circle(tile_map, 50, 50, 16, 0)
    tile_set = {0: pygame.Surface((32, 32), pygame.SRCALPHA)}
    pygame.draw.circle(tile_set[0], (255, 255, 255), (16, 16), 16)
