import pygame
import math

from isec.app import Resource
from isec.environment import Entity, Sprite, Pos


def sign(n):
    return (n > 0) - (n < 0)


class PlayerSpotlight(Entity):
    def __init__(self, player_position: Pos) -> None:
        self.number_of_points = 50
        self.radius = 125
        self.opening_angle = 45

        self.sprite = Sprite(self.create_spotlight_surface(),
                             blit_flag=pygame.BLEND_ADD,
                             rendering_technique="rotated")

        super().__init__(position=player_position, sprite=self.sprite)

    def create_spotlight_youtube(self,
                                 tilemap: list[list[int]],
                                 tile_size: int) -> list[pygame.Vector2]:

        vec_ray_start = pygame.Vector2(self.position.position[0], self.position.position[1])/tile_size

        coordinates = [vec_ray_start]

        for i in range(self.number_of_points):
            angle = -self.position.a - self.opening_angle/2 + i * self.opening_angle/(self.number_of_points - 1)
            vec_ray_dir = pygame.Vector2(1, 0).rotate(angle)
            vec_start_cell = pygame.Vector2(math.floor(vec_ray_start[0]),
                                            math.floor(vec_ray_start[1]))

            if vec_ray_dir[0] == 0:
                dir_y_over_x = float('+inf')
            else:
                dir_y_over_x = vec_ray_dir[1] / vec_ray_dir[0]

            if vec_ray_dir[1] == 0:
                dir_x_over_y = float('+inf')
            else:
                dir_x_over_y = vec_ray_dir[0] / vec_ray_dir[1]

            vec_ray_unit_step_size = pygame.Vector2(math.sqrt(1 + dir_y_over_x ** 2), math.sqrt(1 + dir_x_over_y ** 2))
            vec_map_check = vec_start_cell.copy()

            vec_ray_length_1d = pygame.Vector2(0, 0)
            vec_step = pygame.Vector2(0, 0)

            if vec_ray_dir[0] < 0:
                vec_step[0] = -1
                vec_ray_length_1d[0] = (vec_ray_start[0] - vec_start_cell[0]) * vec_ray_unit_step_size[0]

            else:
                vec_step[0] = 1
                vec_ray_length_1d[0] = (vec_start_cell[0] + 1 - vec_ray_start[0]) * vec_ray_unit_step_size[0]

            if vec_ray_dir[1] < 0:
                vec_step[1] = -1
                vec_ray_length_1d[1] = (vec_ray_start[1] - vec_start_cell[1]) * vec_ray_unit_step_size[1]

            else:
                vec_step[1] = 1
                vec_ray_length_1d[1] = (vec_start_cell[1] + 1 - vec_ray_start[1]) * vec_ray_unit_step_size[1]

            tile_found = False
            max_distance = self.radius / tile_size
            current_distance = 0

            while not tile_found and current_distance < max_distance:
                if vec_ray_length_1d[0] < vec_ray_length_1d[1]:
                    vec_map_check[0] += vec_step[0]
                    current_distance = vec_ray_length_1d[0]
                    vec_ray_length_1d[0] += vec_ray_unit_step_size[0]

                else:
                    vec_map_check[1] += vec_step[1]
                    current_distance = vec_ray_length_1d[1]
                    vec_ray_length_1d[1] += vec_ray_unit_step_size[1]

                if tilemap[math.floor(vec_map_check[1])][math.floor(vec_map_check[0])] > -1:
                    tile_found = True

            if tile_found:
                # calculate the intersection
                coordinates.append(vec_ray_start + vec_ray_dir * current_distance)

            else:
                coordinates.append(vec_ray_start + vec_ray_dir * max_distance)

        for i in range(len(coordinates)):
            coordinates[i] *= tile_size

        return coordinates

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
