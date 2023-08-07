import pygame
import random
import math

from isec.app import Resource
from isec.environment import Entity, Sprite, Pos


class PlayerSpotlight(Entity):
    def __init__(self,
                 player_position: Pos,
                 collision_map: list[list[bool]],
                 tile_size: int) -> None:

        self.collision_map = collision_map
        self.tile_size = tile_size

        self.number_of_points = 50
        self.radius = 150
        self.opening_angle = 50
        self.max_bulb_size = 10
        self.min_bulb_size = 6

        self.surface_size = (self.radius*2 + self.max_bulb_size*2,
                             self.radius*2 + self.max_bulb_size*2)
        self.surface_half = self.surface_size[0]/2

        self.light_bulb_size = [random.randint(self.min_bulb_size, self.max_bulb_size)
                                for _ in range(self.number_of_points+1)]

        sprite_surface = pygame.Surface(self.surface_size)
        sprite_surface.fill((0, 0, 0))
        sprite_surface.set_colorkey((0, 0, 0))
        self.sprite = Sprite(surface=sprite_surface,
                             blit_flag=pygame.BLEND_ADD,
                             rendering_technique="static")

        super().__init__(position=player_position, sprite=self.sprite)

    def update(self,
               delta: float) -> None:

        super().update(delta)
        self.create_spotlight_surface()

    @property
    def surface(self):
        return self.sprite.surface

    @surface.setter
    def surface(self, value):
        self.sprite.surface = value

    def create_spotlight_boundaries(self) -> tuple[list[pygame.Vector2], list[float]]:

        vec_ray_start = pygame.Vector2(self.position.position[0], self.position.position[1])/self.tile_size

        coordinates = [pygame.Vector2(0, 0)]
        hit_strength = [0.0]

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
            max_distance = self.radius / self.tile_size
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

                y_floor = math.floor(vec_map_check[1])
                x_floor = math.floor(vec_map_check[0])

                if any((x_floor < 0,
                        y_floor < 0,
                        x_floor >= len(self.collision_map[0]),
                        y_floor >= len(self.collision_map))):

                    tile_found = True
                    current_distance = max_distance

                if self.collision_map[y_floor][x_floor]:
                    tile_found = True

            if tile_found:
                current_distance += self.light_bulb_size[i+1]/15
            strength = 1 - current_distance / max_distance
            strength = 2 * strength if strength < 0.5 else 1
            hit_strength.append(strength)
            coordinates.append(vec_ray_dir * min(max_distance, current_distance))

        for i in range(len(coordinates)):
            coordinates[i] *= self.tile_size
            coordinates[i] += (self.surface_half, self.surface_half)

        return coordinates, hit_strength

    def create_spotlight_surface(self) -> None:
        coordinates, hit_strength = self.create_spotlight_boundaries()
        self.surface.fill((0, 0, 0))
        pygame.draw.polygon(self.surface, Resource.data["color"]["list"][-4], coordinates)

        for i, coord in enumerate(coordinates):
            if diam := int(hit_strength[i]*self.light_bulb_size[i]):
                bulb_rect = pygame.Rect((0, 0), (diam, diam))
                bulb_rect.center = coord
                pygame.draw.ellipse(self.surface, Resource.data["color"]["list"][-5], bulb_rect)

        self.surface.blit(Resource.image["game"]["spotlight_mask"], (0, 0), special_flags=pygame.BLEND_MULT)
        self.surface = pygame.transform.box_blur(self.surface, 1)
