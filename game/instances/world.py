import pygame
import pymunk
import time

from isec.app import Resource
from isec.instance import BaseInstance, LoopHandler
from isec.environment import TilemapScene, EntityScene
from isec.environment.base import Entity, Pos, Sprite
from isec.environment.sprite import PymunkSprite
from isec.environment.position import PymunkPos
from isec.environment.tile_utils import TileCollision

from game.objects.game.player import Player
from game.objects.game.player_spotlight import PlayerSpotlight


class World(BaseInstance):
    def __init__(self,
                 map_name: str = "test") -> None:

        super().__init__(fps=120)

        # Tilemap related
        self.tile_size = 8
        self.tile_map = Resource.data["maps"][map_name]
        self.tile_set = TilemapScene.create_tileset(Resource.image["tileset"]["tileset_1"],
                                                    self.tile_size,
                                                    0,
                                                    1)

        self.collision_map = TilemapScene.create_collision_map(self.tile_map,
                                                               [i+15*j for i in range(6) for j in range(10)])

        # Creation of scenes
        self.tilemap_scene = TilemapScene(self.tile_map,
                                          self.tile_set)

        self.entity_scene = EntityScene(120,
                                        camera=self.tilemap_scene.camera)

        self.entity_scene.space.damping = 0.2

        # Creation of entities
        self.player = Player(self.entity_scene)

        player_spotlight = PlayerSpotlight(self.player.position,
                                           self.collision_map,
                                           self.tile_size)

        tile_collision = TileCollision(self.collision_map,
                                       self.tile_size)

        self.entity_scene.add_entities(self.player, tile_collision, player_spotlight)

        # Callbacks
        self.player.add_control_callbacks(linked_instance=self)
        self.event_handler.register_buttonpressed_callback(2, self.move_camera)
        self.event_handler.register_buttondown_callback(4, self.increment_inter_tile)
        self.event_handler.register_buttonup_callback(5, self.decrement_inter_tile)
        self.event_handler.register_keyup_callback(pygame.K_ESCAPE, self.quit_instance)
        self.event_handler.register_keydown_callback(pygame.K_LALT, self.swap_velocity)

    async def loop(self) -> None:
        LoopHandler.fps_caption()
        self.window.fill(Resource.data["color"]["list"][-1])
        self.tilemap_scene.update(self.delta)
        self.entity_scene.update(self.delta)

        self.entity_scene.camera.position.position[0] = self.player.position.position[0] - 200
        self.entity_scene.camera.position.position[1] = self.player.position.position[1] - 150

        self.tilemap_scene.render()
        self.entity_scene.render()

        """
        spotlight_points = self.player_spotlight.create_spotlight_boundaries(self.collision_map, 8)
        for i in range(len(spotlight_points)):
            spotlight_points[i] = self.entity_scene.camera.get_offset_pos(Pos(position=spotlight_points[i]))

        for point in []:  # spotlight_points:
            pygame.draw.circle(self.window,
                               (255, 255, 255),
                               point,
                               2)

        pygame.draw.polygon(self.window,
                            Resource.data["color"]["list"][1],
                            spotlight_points)
        """

    async def move_camera(self) -> None:
        self.tilemap_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6
        self.tilemap_scene.camera.position.position -= pygame.math.Vector2(self.event_handler.mouse_rel) / 6

    async def increment_inter_tile(self) -> None:
        self.tilemap_scene.inter_tile_distance += 1

    async def decrement_inter_tile(self) -> None:
        self.tilemap_scene.inter_tile_distance -= 1

    async def quit_instance(self) -> None:
        LoopHandler.stop_instance(self)

    async def swap_velocity(self) -> None:
        if self.player.velocity == self.player.exploration_velocity:
            self.player.velocity = self.player.chase_velocity
            print('chase velocity')
            return

        self.player.velocity = self.player.exploration_velocity
        print('exploration velocity')
